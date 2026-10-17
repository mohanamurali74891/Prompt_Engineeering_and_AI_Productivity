# 💼 Resume & Career Prompt Templates

> Part of the AI Productivity Toolkit — Module 2, Codomax Gen AI Internship

---

## Template 1: Resume Bullet Point Generator

```
ROLE: You are a professional resume writer and career coach with 10+ years of experience.

CONTEXT: I need to write strong, quantified resume bullet points for my experience section.

INSTRUCTIONS:
- Transform the raw job description into 3–5 powerful resume bullet points
- Use the PAR format: Problem → Action → Result
- Start each bullet with a strong action verb (Engineered, Spearheaded, Optimized, etc.)
- Quantify impact wherever possible (%, $, time saved, users, etc.)
- Keep each bullet under 20 words

CONSTRAINTS:
- No first-person pronouns (no "I", "my", "we")
- No passive voice
- Results must be realistic and believable
- Use industry-specific keywords for ATS optimization

INPUT VARIABLES:
- Job Title: [TITLE]
- Company: [COMPANY]
- Industry: [INDUSTRY]
- Raw Description: [WHAT YOU ACTUALLY DID — in plain language]
- Key Achievement: [YOUR BIGGEST WIN]
- Tools/Tech Used: [TOOLS]

OUTPUT FORMAT:
• [Action verb] [what you did] resulting in [measurable impact]
• [Action verb] [what you did] by [how] leading to [result]
• [continue...]
```

**Example Input:**
```
Job Title: AI Research Intern
Company: TechLabs
Industry: AI/ML
Raw Description: I helped build a chatbot that answered customer questions
Key Achievement: Reduced support tickets by 30%
Tools: Python, LangChain, Gemini API
```

**Example Output:**
```
• Engineered an LLM-powered customer support chatbot using Python and LangChain, reducing support ticket volume by 30%
• Integrated Gemini API to enable real-time natural language understanding across 5,000+ monthly queries
• Optimized prompt templates to improve chatbot response accuracy from 72% to 91% over 4 iterations
```

---

## Template 2: LinkedIn Summary / About Section Generator

```
ROLE: Personal branding expert and LinkedIn optimization specialist

CONTEXT: Write a compelling LinkedIn "About" section for my profile.

INSTRUCTIONS:
- Hook: First 2 lines must grab attention (they appear before "See more")
- Story: Brief professional journey (2–3 sentences)
- Expertise: What I specialize in (skills, domains)
- Value Proposition: What I bring to employers/clients
- CTA: End with how to connect or reach out
- Tone: Professional yet conversational, first-person is fine here

CONSTRAINTS:
- Under 300 words
- Avoid buzzwords: "passionate", "guru", "ninja", "rockstar"
- Use line breaks for readability
- Include relevant keywords for searchability

INPUT:
- Name: [NAME]
- Current Role: [ROLE / STUDENT]
- Domain: [AI / ML / Software / Data, etc.]
- Top 3 Skills: [SKILLS]
- Career Goal: [GOAL]
- Notable Achievement: [ACHIEVEMENT]
- Personality Trait: [1 authentic trait]

OUTPUT FORMAT:
[Hook — 2 lines]

[Story — 2–3 sentences]

🔧 What I do:
• [Skill/domain 1]
• [Skill/domain 2]
• [Skill/domain 3]

[Value proposition — 2 sentences]

[CTA — 1 sentence with contact preference]
```

---

## Template 3: Job Description to Skills Extractor

```
ROLE: Career strategist and ATS optimization expert

CONTEXT: Analyze this job description and extract key information to help tailor my resume.

INSTRUCTIONS:
- Extract: Required skills, Preferred skills, Keywords for ATS, Company culture signals
- Map each skill to: Must Have / Nice to Have / Bonus
- Suggest which of my skills to highlight
- Flag any gaps I need to address

INPUT:
[PASTE JOB DESCRIPTION]

MY CURRENT SKILLS:
[LIST YOUR SKILLS]

OUTPUT FORMAT:
## Job Analysis: [Role] at [Company]

**Must-Have Skills:**
| Skill | Do I Have It? |
|-------|--------------|
| [skill] | ✅ / ❌ / Partial |

**ATS Keywords to Include:**
[comma-separated list]

**Culture Signals:**
[What the company seems to value]

**Resume Customization Tips:**
• [Tip 1]
• [Tip 2]

**Skill Gaps to Address:**
• [Gap 1 — how to bridge it]
```

---

## Template 4: Cover Letter Generator

```
ROLE: Professional cover letter writer

CONTEXT:
- Applicant: [NAME]
- Role: [JOB TITLE]
- Company: [COMPANY NAME]
- Hiring Manager: [NAME or "Hiring Manager"]
- My background: [2–3 sentence summary]
- Why this role: [GENUINE REASON]
- Key achievement relevant to this role: [ACHIEVEMENT]

INSTRUCTIONS:
- Opening: Compelling hook, not "I am applying for..."
- Paragraph 2: Relevant experience + achievement with metrics
- Paragraph 3: Why THIS company (research-based, specific)
- Closing: Confident CTA
- Tone: Enthusiastic, professional, direct
- Length: 250–350 words

OUTPUT:
[Full cover letter]
```

---

## Template 5: Interview Preparation — STAR Stories

```
ROLE: Interview coach specializing in behavioral interviews

CONTEXT: Help me prepare a STAR-format story for behavioral interview questions.

INSTRUCTIONS:
- Situation: Set the scene briefly (1–2 sentences)
- Task: What was your responsibility? (1 sentence)
- Action: What specifically did YOU do? (3–4 sentences — this is the meat)
- Result: Quantified outcome + what you learned (2 sentences)
- Tip at the end: Which common behavioral questions this story answers

INPUT:
- Experience/Project: [DESCRIBE THE SITUATION]
- Your Role: [YOUR ROLE]
- Challenge: [MAIN CHALLENGE]
- What You Did: [YOUR ACTIONS]
- Outcome: [RESULT]

OUTPUT FORMAT:
**STAR Story: [Title]**

**S — Situation:** [context]
**T — Task:** [responsibility]
**A — Action:** [your specific actions]
**R — Result:** [measurable outcome]

**💡 Use this story for:**
• Tell me about a time you [...]
• Describe a challenge you overcame
• [other relevant question]
```

---

*These templates are part of the AI Productivity Toolkit built in Module 2.*
