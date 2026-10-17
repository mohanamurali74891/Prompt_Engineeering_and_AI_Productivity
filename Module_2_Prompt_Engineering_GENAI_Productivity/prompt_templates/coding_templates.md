# 💻 AI-Assisted Coding Prompt Templates

> Part of the AI Productivity Toolkit — Module 2, Codomax Gen AI Internship

---

## Template 1: Code Generation from Requirements

```
ROLE: You are a senior software engineer with expertise in [LANGUAGE/FRAMEWORK].

CONTEXT: I need you to write production-quality code based on my requirements.

INSTRUCTIONS:
- Write clean, readable, well-commented code
- Follow best practices and design patterns for [LANGUAGE]
- Include error handling and edge cases
- Add docstrings/comments for each function
- Provide example usage at the bottom

CONSTRAINTS:
- Do NOT use deprecated libraries or functions
- Code must be compatible with [PYTHON VERSION / NODE VERSION / etc.]
- Do not include unnecessary dependencies
- Keep functions small and single-purpose (SRP)

REQUIREMENTS:
[DESCRIBE WHAT THE CODE SHOULD DO]

INPUT/OUTPUT EXAMPLE:
Input: [example input]
Expected Output: [expected output]

TECH STACK:
- Language: [LANGUAGE]
- Libraries allowed: [LIST]
- Environment: [Local / Cloud / Colab / Browser]

OUTPUT FORMAT:
```python
# [filename.py]
# Description: [what this code does]
# Author: [name]

[full code with comments]

# Example usage:
if __name__ == "__main__":
    [example]
```
```

---

## Template 2: Code Debugger & Error Explainer

```
ROLE: Expert debugging assistant and code reviewer

CONTEXT: My code is throwing an error and I need help fixing it.

INSTRUCTIONS:
1. Identify the root cause of the error (not just the symptom)
2. Explain WHY the error occurs in simple terms
3. Provide the corrected code with comments showing what changed
4. Suggest how to prevent this type of error in the future
5. If there are other bugs or code smells, mention them briefly

CONSTRAINTS:
- Explain the fix, don't just give code
- Keep the explanation beginner-friendly
- Preserve the original code structure unless the fix requires restructuring

MY CODE:
```
[PASTE YOUR CODE HERE]
```

ERROR MESSAGE:
```
[PASTE ERROR / TRACEBACK HERE]
```

WHAT I EXPECTED:
[DESCRIBE EXPECTED BEHAVIOR]

OUTPUT FORMAT:
## 🐛 Root Cause
[explanation of WHY the error happens]

## ✅ Fixed Code
```[language]
[corrected code with # FIXED: comments]
```

## 🔍 What Changed
• [change 1 — why]
• [change 2 — why]

## 🛡️ Prevention Tip
[how to avoid this in future]
```

---

## Template 3: Code Review & Optimization

```
ROLE: Senior software engineer conducting a thorough code review

CONTEXT: Please review my code for quality, performance, and best practices.

REVIEW CRITERIA:
- Code readability and naming conventions
- Logic correctness and edge cases
- Performance bottlenecks
- Security vulnerabilities (if applicable)
- DRY principle violations (repeated code)
- Missing error handling

INSTRUCTIONS:
- Rate the code overall (1–10)
- Provide specific, actionable feedback with line references
- Show the improved version of problematic sections
- Prioritize: Critical > Major > Minor issues

CODE TO REVIEW:
```
[PASTE CODE]
```

OUTPUT FORMAT:
## Code Review Report

**Overall Rating:** [X/10]
**Language:** [language]

### 🔴 Critical Issues
[issue with line reference and fix]

### 🟡 Major Issues
[issue with line reference and suggestion]

### 🟢 Minor Improvements
[suggestion]

### ✅ What's Good
[positive feedback]

### 📈 Optimized Version
```[language]
[improved code]
```
```

---

## Template 4: Unit Test Generator

```
ROLE: QA engineer and test automation specialist

CONTEXT: Generate comprehensive unit tests for the following code.

INSTRUCTIONS:
- Write tests using [pytest / unittest / Jest / etc.]
- Cover: Happy path, Edge cases, Error cases, Boundary values
- Use descriptive test names that explain what is being tested
- Add setup/teardown if needed
- Aim for 80%+ code coverage

CONSTRAINTS:
- No mocking unless necessary
- Each test should test ONE thing only
- Tests must be independent (no shared state)

CODE TO TEST:
```
[PASTE YOUR FUNCTION/CLASS]
```

TESTING FRAMEWORK: [pytest / unittest / Jest]

OUTPUT FORMAT:
```python
# test_[filename].py
# Tests for: [what is being tested]

import pytest
from [module] import [function]

class Test[ClassName]:
    
    def test_[scenario]_returns_[expected](self):
        """[description of what this tests]"""
        # Arrange
        [setup]
        # Act
        result = [function call]
        # Assert
        assert result == [expected]
    
    [more tests...]
```

**Coverage Report:**
| Scenario | Test Name | Status |
|----------|-----------|--------|
| Happy path | test_... | ✅ |
| Edge case | test_... | ✅ |
```

---

## Template 5: Code Documentation Generator

```
ROLE: Technical documentation writer

CONTEXT: Generate professional documentation for this code.

INSTRUCTIONS:
- Add docstrings to every function/class following [Google/NumPy/Sphinx] style
- Create a module-level docstring explaining the file's purpose
- Add inline comments for complex logic
- Generate a README section explaining how to use this module

CODE:
```
[PASTE CODE]
```

DOCSTRING STYLE: [Google / NumPy / Sphinx]

OUTPUT FORMAT:
```python
"""
Module: [module_name]
Description: [what this module does]
Author: [name]
Date: [date]
"""

[fully documented code]
```

**Usage README Section:**
```markdown
## [Module Name]

### Installation
[pip install commands]

### Quick Start
```python
[example usage]
```

### API Reference
[function signatures and descriptions]
```
```

---

## Template 6: Algorithm Explainer

```
ROLE: Computer science professor and algorithm expert

CONTEXT: Explain the following algorithm/code to me as if I'm a beginner.

INSTRUCTIONS:
- Start with the big picture (what does this do?)
- Walk through the logic step by step using a simple example
- Explain time and space complexity in plain English
- Draw an ASCII diagram if helpful
- Suggest when to use this algorithm

CODE/ALGORITHM:
```
[PASTE CODE OR ALGORITHM NAME]
```

MY LEVEL: [Beginner / Intermediate / Advanced]

OUTPUT FORMAT:
## Algorithm: [Name]

**What it does:** [one sentence]

**Step-by-step walkthrough:**
[numbered steps with a simple example]

**Example trace:**
Input: [example]
Step 1: [what happens]
Step 2: [what happens]
Output: [result]

**Time Complexity:** O([?]) — [plain English explanation]
**Space Complexity:** O([?]) — [plain English explanation]

**Use when:** [scenarios]
**Avoid when:** [scenarios]
```

---

*These templates are part of the AI Productivity Toolkit built in Module 2.*
