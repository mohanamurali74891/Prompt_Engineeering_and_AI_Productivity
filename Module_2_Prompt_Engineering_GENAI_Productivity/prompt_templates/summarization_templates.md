# 📝 Summarization Prompt Templates

> Part of the AI Productivity Toolkit — Module 2, Codomax Gen AI Internship

---

## Template 1: Article / Blog Post Summarizer

```
ROLE: You are a professional research analyst and technical writer.

CONTEXT: I need a concise summary of the following article/blog post.

INSTRUCTIONS:
- Provide a summary in 3 sections:
  1. TL;DR (1 sentence — the core takeaway)
  2. Key Points (3–5 bullet points)
  3. Why It Matters (2–3 sentences on implications)
- Use plain language, accessible to a non-expert
- Do not add opinions or external information

CONSTRAINTS:
- Total output should be under 200 words
- Use bullet points for Key Points section
- Do not use jargon unless the original text uses it

INPUT:
[PASTE ARTICLE TEXT HERE]

OUTPUT FORMAT:
**TL;DR:** [one sentence]

**Key Points:**
• [point 1]
• [point 2]
• [point 3]

**Why It Matters:**
[2–3 sentences]
```

---

## Template 2: Research Paper Summarizer

```
ROLE: You are an academic research assistant with expertise in AI and technology.

CONTEXT: Summarize the following research paper for a non-specialist audience.

INSTRUCTIONS:
- Extract: Problem statement, Methodology, Key findings, Limitations, Future work
- Use simple, clear language
- Highlight numbers and statistics if present
- Include authors and publication year if mentioned

CONSTRAINTS:
- Output under 300 words
- Use section headers
- No plagiarism — paraphrase all content

INPUT:
[PASTE PAPER ABSTRACT OR FULL TEXT]

OUTPUT FORMAT:
## Research Paper Summary

**Problem:** [What problem does this paper solve?]

**Method:** [How did they approach it?]

**Key Findings:**
• [Finding 1]
• [Finding 2]
• [Finding 3]

**Limitations:** [What are the weaknesses?]

**Future Work:** [What comes next?]

**Impact Score (1–10):** [Your rating] — [one sentence justification]
```

---

## Template 3: Meeting Notes Summarizer

```
ROLE: You are an executive assistant specializing in meeting documentation.

CONTEXT: Summarize the following meeting transcript or notes.

INSTRUCTIONS:
- Extract: Attendees, Date/Time, Agenda items discussed, Decisions made, Action items (with owners), Next steps
- Be factual and concise
- Flag any unresolved questions with ⚠️

CONSTRAINTS:
- Output in structured format only
- Action items must include owner and deadline if mentioned
- Do not include filler conversation

INPUT:
[PASTE MEETING NOTES OR TRANSCRIPT]

OUTPUT FORMAT:
## Meeting Summary

**Date:** [date]  
**Attendees:** [names]

**Discussion Points:**
1. [topic 1]
2. [topic 2]

**Decisions Made:**
• [decision 1]
• [decision 2]

**Action Items:**
| Task | Owner | Deadline |
|------|-------|----------|
| [task] | [name] | [date] |

**Open Questions:** ⚠️
• [unresolved item]
```

---

## Template 4: YouTube Video / Podcast Summarizer

```
ROLE: Content curator and summarization expert

CONTEXT: Summarize the key insights from the following video/podcast transcript.

INSTRUCTIONS:
- Hook: One compelling sentence about the content
- Main Topics: 3–5 topics covered
- Golden Nuggets: 3 most actionable/insightful quotes or ideas
- My Takeaway: What the listener should do differently

INPUT:
[PASTE TRANSCRIPT OR DESCRIPTION]

OUTPUT FORMAT:
🎯 **Hook:** [compelling sentence]

📌 **Main Topics Covered:**
1. [topic]
2. [topic]
3. [topic]

💡 **Golden Nuggets:**
1. "[quote or idea]"
2. "[quote or idea]"
3. "[quote or idea]"

✅ **Key Takeaway:** [actionable insight]
```

---

## Template 5: Legal / Terms of Service Summarizer

```
ROLE: Legal assistant simplifying complex documents

CONTEXT: Summarize the key points of the following Terms of Service / Legal document in plain English.

INSTRUCTIONS:
- What data is collected?
- What rights does the user have?
- What rights does the company have?
- Any red flags or unusual clauses?
- Rate the document: User-Friendly / Neutral / User-Hostile

CONSTRAINTS:
- Use simple language (Grade 8 reading level)
- Flag concerning clauses with 🚨
- Keep under 250 words

INPUT:
[PASTE LEGAL TEXT]

OUTPUT FORMAT:
## Plain English Summary

**Data Collected:** [list]
**Your Rights:** [list]
**Their Rights:** [list]

**🚨 Red Flags:**
• [concerning clause if any]

**Verdict:** [User-Friendly / Neutral / User-Hostile] — [one sentence reason]
```

---

*These templates are part of the AI Productivity Toolkit built in Module 2.*
