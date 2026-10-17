# 🧰 AI Productivity Toolkit — Complete Guide

> Module 2 | Codomax Gen AI Internship | Day 6–10

---

## What is the AI Productivity Toolkit?

The AI Productivity Toolkit is a **curated collection of reusable prompt workflows** that automate common professional tasks using Large Language Models (LLMs). Instead of writing prompts from scratch each time, these templates provide a structured starting point that you can customize for your specific needs.

Think of it as a **prompt library** — your personal AI assistant configuration for everyday tasks.

---

## 🗂️ Toolkit Contents

| Module | Templates | Use Cases |
|--------|-----------|-----------|
| 📝 Summarization | 5 templates | Articles, papers, meetings, videos, legal docs |
| 📧 Email Writing | 5 templates | Cold outreach, follow-ups, applications, thank-yous |
| 💼 Resume & Career | 5 templates | Bullet points, LinkedIn, cover letters, interview prep |
| 💻 Coding Assistance | 6 templates | Code gen, debugging, review, testing, documentation |
| 🔬 Research | 5 templates | Deep dives, comparisons, literature reviews, trends |

**Total: 26 reusable prompt templates**

---

## 🚀 How to Use the Toolkit

### Step 1: Identify Your Task
Determine which category your task falls under:
- Need to condense information? → **Summarization**
- Writing a professional message? → **Email Writing**
- Job searching or career growth? → **Resume & Career**
- Building or fixing software? → **Coding Assistance**
- Learning or researching a topic? → **Research**

### Step 2: Choose a Template
Open the relevant template file and find the template that best matches your specific use case.

### Step 3: Fill in the Variables
All templates use `[PLACEHOLDER]` notation for customizable inputs. Replace each placeholder with your specific information.

**Example:**
```
Before: "TOPIC: [TOPIC]"
After:  "TOPIC: Transformer Architecture in Large Language Models"
```

### Step 4: Run the Prompt
Copy the completed prompt into your preferred AI tool:
- **Google Gemini**: gemini.google.com
- **ChatGPT**: chat.openai.com
- **Claude**: claude.ai
- **Via API**: Use the Colab notebook

### Step 5: Iterate if Needed
If the output isn't quite right, try:
1. Being more specific in the instructions
2. Adding an example of the desired output
3. Adjusting constraints (shorter/longer, different format)
4. Changing the role assigned to the model

---

## 📖 Workflow Guides

### Workflow 1: Weekly Work Summary Automation

**Use case:** Every Friday, generate a weekly progress report automatically.

```
ROLE: Professional project coordinator

CONTEXT: I need to write my weekly work summary for my manager.

MY WEEK'S ACTIVITIES:
[bullet list of what you did this week — just rough notes]

METRICS THIS WEEK:
[any numbers: emails sent, lines of code, tasks completed, meetings attended]

INSTRUCTIONS:
- Transform my rough notes into a polished weekly summary
- Organize by: Completed / In Progress / Blocked / Next Week
- Highlight 1–2 key achievements prominently
- Keep it under 300 words
- Professional tone suitable for manager review

OUTPUT FORMAT:
## Weekly Summary — Week of [date]

### ✅ Completed
[formatted list]

### 🔄 In Progress
[formatted list]

### ⚠️ Blockers
[any blockers or needs]

### 📅 Next Week
[upcoming priorities]

### 🏆 Highlight
[one key achievement in 2 sentences]
```

---

### Workflow 2: Email Inbox Zero — Reply Generator

**Use case:** Quickly draft replies to common email types.

```
ROLE: Professional executive assistant

CONTEXT: I need to reply to the following email. Draft a response for me.

ORIGINAL EMAIL:
[paste the email you received]

MY INTENT:
[what do you want to communicate? — e.g., "I want to decline politely but leave door open"]

MY CONSTRAINTS:
- Tone: [Formal / Semi-formal / Friendly]
- Length: [Brief (under 50 words) / Standard / Detailed]
- My name: [YOUR NAME]
- My role: [YOUR ROLE]

INSTRUCTIONS:
- Match the tone of the original email
- Be direct and clear
- End with next steps if applicable
- Don't be overly apologetic

OUTPUT:
Subject: Re: [original subject]

[reply body]

[signature]
```

---

### Workflow 3: Content Research Pipeline

**Use case:** Research a topic from scratch to publishable insights.

**Stage 1 — Overview:**
```
Give me a structured overview of [TOPIC] covering:
1. What it is (definition + history)
2. Why it matters now
3. Key sub-topics to explore
4. Top 5 questions experts are asking
```

**Stage 2 — Deep Dive:**
```
[Take one of the sub-topics from Stage 1]
Provide a detailed explanation of [SUB-TOPIC] including:
- Core mechanisms/principles
- Real-world examples
- Current research or developments
- Common misconceptions
```

**Stage 3 — Content Creation:**
```
Using the research below, write a [BLOG POST / LINKEDIN ARTICLE / REPORT SECTION]:
[paste your Stage 1 + Stage 2 outputs]

Target audience: [AUDIENCE]
Tone: [TONE]
Length: [LENGTH]
Include: [hook, examples, statistics if available, clear CTA]
```

---

### Workflow 4: Job Application Accelerator

**Use case:** Apply to a job in 30 minutes instead of 3 hours.

```
Step 1: Job Description Analysis
→ Use Template: resume_templates.md > Template 3

Step 2: Resume Tailoring
→ Use Template: resume_templates.md > Template 1 (generate bullets for relevant experience)

Step 3: Cover Letter
→ Use Template: resume_templates.md > Template 4

Step 4: Interview Prep
→ Use Template: resume_templates.md > Template 5 (STAR stories for this specific role)

Step 5: LinkedIn Outreach
→ Use Template: email_templates.md > Template 1 (cold outreach to someone at the company)
```

---

### Workflow 5: AI-Assisted Development Cycle

**Use case:** Build a feature faster with AI assistance at every step.

```
Step 1: Requirements to Code
→ Use Template: coding_templates.md > Template 1

Step 2: Code Review
→ Use Template: coding_templates.md > Template 3

Step 3: Test Generation
→ Use Template: coding_templates.md > Template 4

Step 4: Documentation
→ Use Template: coding_templates.md > Template 5

Step 5: Debug if needed
→ Use Template: coding_templates.md > Template 2
```

---

## 💡 Pro Tips

### Tip 1: Chain Prompts for Complex Tasks
Don't try to do everything in one prompt. Break complex tasks into stages:
- Prompt 1: Research / gather information
- Prompt 2: Structure / organize the information
- Prompt 3: Write / generate the final output
- Prompt 4: Review / refine the output

### Tip 2: Save Your Best Prompts
When a prompt works exceptionally well, save it with:
- The context/use case
- The exact prompt text
- Sample output
- Iteration notes

### Tip 3: Use System Prompts for Consistency
If using the API, set a system prompt to establish consistent behavior:
```python
system_prompt = """
You are a professional assistant specializing in [DOMAIN].
Always:
- Be concise and direct
- Use structured formatting (headers, bullets)
- Acknowledge uncertainty when present
- Ask for clarification if requirements are ambiguous
"""
```

### Tip 4: Temperature Settings
- **Temperature 0.0–0.3**: Factual tasks (summarization, classification, data extraction)
- **Temperature 0.5–0.7**: Balanced tasks (email writing, code generation)
- **Temperature 0.8–1.0**: Creative tasks (brainstorming, creative writing)

### Tip 5: Prompt Versioning
Track your prompt improvements:
```
prompt_v1 = "Summarize this: [text]"  # Score: 2.5/5
prompt_v2 = "ROLE: Analyst. Summarize in 3 bullets: [text]"  # Score: 3.8/5
prompt_v3 = [full template]  # Score: 4.7/5
```

---

## 📊 Toolkit ROI Calculation

**Time saved per week (estimated):**

| Task | Manual Time | With AI Toolkit | Time Saved |
|------|------------|----------------|-----------|
| Email writing | 45 min | 10 min | 35 min |
| Meeting summaries | 30 min | 5 min | 25 min |
| Research overview | 120 min | 30 min | 90 min |
| Resume bullet points | 60 min | 10 min | 50 min |
| Code documentation | 45 min | 5 min | 40 min |
| **Total** | **5 hrs** | **1 hr** | **4 hrs/week** |

**That's ~200 hours saved per year** — equivalent to over 5 full work weeks.

---

## 🔮 Future Additions (Roadmap)

- [ ] Social media content calendar generator
- [ ] Product requirements document (PRD) template
- [ ] Meeting agenda generator
- [ ] Project proposal template
- [ ] Data analysis report template
- [ ] API integration guide for automated workflows
- [ ] Multi-model comparison prompts (Gemini vs GPT-4 vs Claude)

---

## 📚 Resources & References

| Resource | Type | Link |
|----------|------|------|
| Prompt Engineering Guide | Guide | https://www.promptingguide.ai |
| Google's Prompting Essentials | Course | https://cloud.google.com/learn/training |
| OpenAI Prompt Engineering | Docs | https://platform.openai.com/docs/guides/prompt-engineering |
| Anthropic's Prompt Library | Library | https://docs.anthropic.com/prompt-library |
| Lilian Weng's Blog on Prompting | Blog | https://lilianweng.github.io |

---

*AI Productivity Toolkit v1.0 — Built as part of Codomax Gen AI Internship, Module 2*
