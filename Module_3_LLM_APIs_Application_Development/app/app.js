/**
 * app.js — AI Chat Application Logic
 * Module 3: LLM APIs & Application Development
 *
 * Features:
 *  - Google Gemini API integration (client-side)
 *  - Multi-turn conversation history management
 *  - Custom system instructions
 *  - Model parameter controls (temperature, max_tokens, model)
 *  - Token usage & cost tracking
 *  - Robust error handling with retry logic
 *  - Markdown rendering (code blocks, bold, lists)
 *  - Auto-resize textarea
 *  - Responsive sidebar toggle
 */

'use strict';

// ─────────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────────

const GEMINI_API_BASE = 'https://generativelanguage.googleapis.com/v1beta/models';

/** Pricing per 1M tokens (USD) — matches cost_tracker.py */
const PRICING = {
  'gemini-1.5-flash': { input: 0.075,  output: 0.30  },
  'gemini-1.5-pro':   { input: 3.50,   output: 10.50 },
  'gemini-1.0-pro':   { input: 0.50,   output: 1.50  },
};

const MAX_RETRIES    = 3;
const RETRY_DELAY_MS = 1500;

// ─────────────────────────────────────────────────────────────
// State
// ─────────────────────────────────────────────────────────────

const state = {
  apiKey:         '',
  model:          'gemini-1.5-flash',
  temperature:    0.7,
  maxTokens:      2048,
  systemPrompt:   '',
  history:        [],   // [{role: 'user'|'model', parts: [{text: '...'}]}]
  isStreaming:    false,
  stats: {
    calls:           0,
    totalTokens:     0,
    promptTokens:    0,
    completionTokens:0,
    costUsd:         0,
    turns:           0,
  },
};

// ─────────────────────────────────────────────────────────────
// DOM References
// ─────────────────────────────────────────────────────────────

const dom = {
  apiKeyInput:      document.getElementById('api-key-input'),
  toggleKeyBtn:     document.getElementById('toggle-key-btn'),
  systemPromptInput:document.getElementById('system-prompt-input'),
  modelSelect:      document.getElementById('model-select'),
  tempSlider:       document.getElementById('temperature-slider'),
  tempValue:        document.getElementById('temp-value'),
  maxTokensSelect:  document.getElementById('max-tokens-select'),
  clearBtn:         document.getElementById('clear-chat-btn'),
  sidebarToggle:    document.getElementById('sidebar-toggle'),
  sidebar:          document.getElementById('sidebar'),
  messagesContainer:document.getElementById('messages-container'),
  typingIndicator:  document.getElementById('typing-indicator'),
  userInput:        document.getElementById('user-input'),
  charCount:        document.getElementById('char-count'),
  sendBtn:          document.getElementById('send-btn'),
  modelBadge:       document.getElementById('model-badge'),
  toastContainer:   document.getElementById('toast-container'),
  welcomeTime:      document.getElementById('welcome-time'),
  statCalls:        document.getElementById('stat-calls'),
  statTokens:       document.getElementById('stat-tokens'),
  statCost:         document.getElementById('stat-cost'),
  statTurns:        document.getElementById('stat-turns'),
};

// ─────────────────────────────────────────────────────────────
// Initialisation
// ─────────────────────────────────────────────────────────────

function init() {
  dom.welcomeTime.textContent = formatTime(new Date());

  // Restore saved API key (sessionStorage only — never persisted to disk)
  const savedKey = sessionStorage.getItem('gemini_api_key');
  if (savedKey) {
    dom.apiKeyInput.value = savedKey;
    state.apiKey = savedKey;
    updateSendButton();
  }

  bindEvents();
}

// ─────────────────────────────────────────────────────────────
// Event Binding
// ─────────────────────────────────────────────────────────────

function bindEvents() {
  // API key
  dom.apiKeyInput.addEventListener('input', () => {
    state.apiKey = dom.apiKeyInput.value.trim();
    sessionStorage.setItem('gemini_api_key', state.apiKey);
    updateSendButton();
  });

  // Toggle key visibility
  dom.toggleKeyBtn.addEventListener('click', () => {
    const isPassword = dom.apiKeyInput.type === 'password';
    dom.apiKeyInput.type = isPassword ? 'text' : 'password';
  });

  // System prompt
  dom.systemPromptInput.addEventListener('input', () => {
    state.systemPrompt = dom.systemPromptInput.value.trim();
  });
  state.systemPrompt = dom.systemPromptInput.value.trim();

  // Model select
  dom.modelSelect.addEventListener('change', () => {
    state.model = dom.modelSelect.value;
    dom.modelBadge.textContent = state.model;
    showToast(`Model switched to ${state.model}`, 'info');
  });

  // Temperature slider
  dom.tempSlider.addEventListener('input', () => {
    state.temperature = parseFloat(dom.tempSlider.value);
    dom.tempValue.textContent = state.temperature.toFixed(2);
  });

  // Max tokens
  dom.maxTokensSelect.addEventListener('change', () => {
    state.maxTokens = parseInt(dom.maxTokensSelect.value, 10);
  });

  // Clear conversation
  dom.clearBtn.addEventListener('click', clearConversation);

  // Sidebar toggle
  dom.sidebarToggle.addEventListener('click', () => {
    dom.sidebar.classList.toggle('collapsed');
  });

  // User input
  dom.userInput.addEventListener('input', onUserInputChange);
  dom.userInput.addEventListener('keydown', onUserInputKeydown);

  // Send button
  dom.sendBtn.addEventListener('click', handleSend);
}

// ─────────────────────────────────────────────────────────────
// Input handlers
// ─────────────────────────────────────────────────────────────

function onUserInputChange() {
  const text   = dom.userInput.value;
  const length = text.length;
  const max    = 8000;

  // Auto-resize
  dom.userInput.style.height = 'auto';
  dom.userInput.style.height = Math.min(dom.userInput.scrollHeight, 160) + 'px';

  // Char count
  dom.charCount.textContent = `${length.toLocaleString()} / ${max.toLocaleString()}`;
  dom.charCount.classList.toggle('near-limit', length > max * 0.85 && length < max);
  dom.charCount.classList.toggle('at-limit',   length >= max);

  updateSendButton();
}

function onUserInputKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    if (!dom.sendBtn.disabled) handleSend();
  }
}

function updateSendButton() {
  const hasKey   = state.apiKey.length > 10;
  const hasText  = dom.userInput.value.trim().length > 0;
  const ready    = hasKey && hasText && !state.isStreaming;
  dom.sendBtn.disabled = !ready;
}

// ─────────────────────────────────────────────────────────────
// Send message
// ─────────────────────────────────────────────────────────────

async function handleSend() {
  const text = dom.userInput.value.trim();
  if (!text || state.isStreaming) return;
  if (!state.apiKey) {
    showToast('Please enter your Gemini API key in the sidebar.', 'error');
    return;
  }

  // Clear input
  dom.userInput.value = '';
  dom.userInput.style.height = 'auto';
  onUserInputChange();

  // Add user message to UI
  appendMessage('user', text);

  // Add to history
  state.history.push({ role: 'user', parts: [{ text }] });

  // Show typing indicator
  setStreaming(true);

  try {
    const response = await callGeminiWithRetry();
    const assistantText = extractText(response);

    // Track tokens
    const usage = response.usageMetadata || {};
    trackTokens(usage);

    // Add assistant message to UI
    appendMessage('assistant', assistantText, usage);

    // Add to history
    state.history.push({ role: 'model', parts: [{ text: assistantText }] });

    // Increment turns
    state.stats.turns++;
    updateStatsUI();

  } catch (err) {
    const errMsg = formatError(err);
    appendMessage('assistant', errMsg, null, true);
    showToast('API error — see message for details.', 'error');
    console.error('[GeminiChat] API Error:', err);
  } finally {
    setStreaming(false);
  }
}

// ─────────────────────────────────────────────────────────────
// Gemini API call with retry
// ─────────────────────────────────────────────────────────────

async function callGeminiWithRetry(attempt = 1) {
  try {
    return await callGeminiAPI();
  } catch (err) {
    if (attempt < MAX_RETRIES && isRetryableError(err)) {
      const delay = RETRY_DELAY_MS * Math.pow(2, attempt - 1);
      showToast(`Rate limited — retrying in ${delay / 1000}s… (${attempt}/${MAX_RETRIES})`, 'info');
      await sleep(delay);
      return callGeminiWithRetry(attempt + 1);
    }
    throw err;
  }
}

async function callGeminiAPI() {
  const url = `${GEMINI_API_BASE}/${state.model}:generateContent?key=${state.apiKey}`;

  const body = {
    contents: state.history,
    generationConfig: {
      temperature:      state.temperature,
      maxOutputTokens:  state.maxTokens,
      topP:             0.95,
      topK:             40,
    },
  };

  if (state.systemPrompt) {
    body.systemInstruction = {
      parts: [{ text: state.systemPrompt }],
    };
  }

  const res = await fetch(url, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify(body),
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    const message = errData?.error?.message || `HTTP ${res.status}`;
    const err     = new Error(message);
    err.status    = res.status;
    throw err;
  }

  return res.json();
}

function isRetryableError(err) {
  return err.status === 429 || err.status === 503 || err.status === 500;
}

function extractText(response) {
  try {
    return response.candidates?.[0]?.content?.parts?.[0]?.text || '(no response)';
  } catch {
    return '(could not parse response)';
  }
}

function formatError(err) {
  if (err.status === 400) return `❌ **Bad Request**: ${err.message}\n\nThis may be caused by an invalid API key or unsupported model.`;
  if (err.status === 401) return `❌ **Unauthorised**: Your API key is invalid or expired. Please check your API key in the sidebar.`;
  if (err.status === 403) return `❌ **Forbidden**: The model may not be available in your region, or the API key lacks permission.`;
  if (err.status === 429) return `❌ **Rate Limit Exceeded**: You've sent too many requests. Please wait a moment and try again.`;
  if (err.status === 503) return `❌ **Service Unavailable**: The Gemini API is temporarily unavailable. Please try again shortly.`;
  return `❌ **Error**: ${err.message}`;
}

// ─────────────────────────────────────────────────────────────
// Token tracking & cost
// ─────────────────────────────────────────────────────────────

function trackTokens(usage) {
  const promptTok    = usage.promptTokenCount     || 0;
  const completionTok= usage.candidatesTokenCount || 0;
  const totalTok     = usage.totalTokenCount       || (promptTok + completionTok);

  const pricing = PRICING[state.model] || { input: 1.0, output: 3.0 };
  const cost    = (promptTok / 1e6) * pricing.input + (completionTok / 1e6) * pricing.output;

  state.stats.calls++;
  state.stats.promptTokens     += promptTok;
  state.stats.completionTokens += completionTok;
  state.stats.totalTokens      += totalTok;
  state.stats.costUsd          += cost;

  updateStatsUI();
}

function updateStatsUI() {
  dom.statCalls.textContent  = state.stats.calls.toLocaleString();
  dom.statTokens.textContent = state.stats.totalTokens.toLocaleString();
  dom.statCost.textContent   = `$${state.stats.costUsd.toFixed(6)}`;
  dom.statTurns.textContent  = state.stats.turns.toLocaleString();
}

// ─────────────────────────────────────────────────────────────
// UI: Rendering messages
// ─────────────────────────────────────────────────────────────

function appendMessage(role, content, usage = null, isError = false) {
  const row = document.createElement('div');
  row.className = `message-row ${role === 'user' ? 'user-row' : 'assistant-row'}`;

  const avatar = document.createElement('div');
  avatar.className = `avatar ${role === 'user' ? 'user-avatar' : 'assistant-avatar'}`;
  avatar.setAttribute('aria-hidden', 'true');
  avatar.innerHTML = role === 'user'
    ? '<span>U</span>'
    : `<svg viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="14" fill="url(#av${Date.now()})"/><path d="M10 16 Q16 8 22 16 Q16 24 10 16Z" fill="white" opacity="0.9"/><defs><linearGradient id="av${Date.now()}" x1="0" y1="0" x2="32" y2="32"><stop offset="0%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#2563eb"/></linearGradient></defs></svg>`;

  const msg = document.createElement('div');
  msg.className = `message ${role === 'user' ? 'user-message' : 'assistant-message'}${isError ? ' error-message' : ''}`;

  const bubble = document.createElement('div');
  bubble.className = 'message-content';
  bubble.innerHTML = renderMarkdown(content);

  const meta = document.createElement('div');
  meta.className = 'message-meta';

  const time = document.createElement('span');
  time.textContent = formatTime(new Date());

  const roleLabel = document.createElement('span');
  roleLabel.textContent = role === 'user' ? 'You' : 'GeminiChat';

  const dot = document.createElement('span');
  dot.className = 'dot-sep';
  dot.textContent = '·';

  meta.appendChild(roleLabel);
  meta.appendChild(dot);
  meta.appendChild(time);

  if (role === 'assistant' && usage) {
    const tokenBadge = document.createElement('span');
    const total = usage.totalTokenCount || ((usage.promptTokenCount || 0) + (usage.candidatesTokenCount || 0));
    if (total > 0) {
      tokenBadge.className = 'token-badge';
      tokenBadge.innerHTML = `<span class="dot-sep">·</span> 🪙 ${total.toLocaleString()} tokens`;
      meta.appendChild(tokenBadge);
    }
  }

  if (role === 'assistant' && !isError) {
    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-response-btn';
    copyBtn.textContent = '📋 Copy';
    copyBtn.setAttribute('aria-label', 'Copy response');
    copyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(content).then(() => {
        copyBtn.textContent = '✅ Copied!';
        setTimeout(() => { copyBtn.textContent = '📋 Copy'; }, 2000);
      });
    });
    meta.appendChild(dot.cloneNode(true));
    meta.appendChild(copyBtn);
  }

  msg.appendChild(bubble);
  msg.appendChild(meta);
  row.appendChild(avatar);
  row.appendChild(msg);

  dom.messagesContainer.appendChild(row);
  scrollToBottom();
}

// ─────────────────────────────────────────────────────────────
// Markdown renderer (lightweight)
// ─────────────────────────────────────────────────────────────

function renderMarkdown(text) {
  // Escape HTML first (except for code blocks)
  let html = text;

  // Code blocks (``` ... ```)
  html = html.replace(/```(\w+)?\n?([\s\S]*?)```/g, (_, lang, code) => {
    const langClass = lang ? ` class="language-${lang}"` : '';
    return `<pre><code${langClass}>${escapeHtml(code.trim())}</code></pre>`;
  });

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Bold
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

  // Italic
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Headers
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm,  '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm,   '<h1>$1</h1>');

  // Numbered lists
  html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, m => `<ol>${m}</ol>`);

  // Unordered lists
  html = html.replace(/^[-*] (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, m => `<ul>${m}</ul>`);

  // Links
  html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g,
    '<a href="$2" target="_blank" rel="noopener">$1</a>');

  // Paragraphs (double newline)
  html = html.replace(/\n\n+/g, '</p><p>');

  // Single line breaks
  html = html.replace(/\n/g, '<br>');

  return `<p>${html}</p>`;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ─────────────────────────────────────────────────────────────
// Streaming state
// ─────────────────────────────────────────────────────────────

function setStreaming(active) {
  state.isStreaming = active;
  dom.typingIndicator.classList.toggle('hidden', !active);
  dom.sendBtn.classList.toggle('loading', active);
  updateSendButton();

  if (!active) scrollToBottom();
}

// ─────────────────────────────────────────────────────────────
// Clear conversation
// ─────────────────────────────────────────────────────────────

function clearConversation() {
  state.history = [];

  // Remove all messages except welcome
  const rows = dom.messagesContainer.querySelectorAll('.message-row:not(#welcome-msg)');
  rows.forEach(r => r.remove());

  // Reset stats
  Object.assign(state.stats, { calls: 0, totalTokens: 0, promptTokens: 0, completionTokens: 0, costUsd: 0, turns: 0 });
  updateStatsUI();

  showToast('Conversation cleared.', 'success');
}

// ─────────────────────────────────────────────────────────────
// Toast notifications
// ─────────────────────────────────────────────────────────────

function showToast(message, type = 'info', duration = 3500) {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  dom.toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(20px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// ─────────────────────────────────────────────────────────────
// Utilities
// ─────────────────────────────────────────────────────────────

function scrollToBottom() {
  dom.messagesContainer.scrollTo({
    top:      dom.messagesContainer.scrollHeight,
    behavior: 'smooth',
  });
}

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ─────────────────────────────────────────────────────────────
// Boot
// ─────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', init);
