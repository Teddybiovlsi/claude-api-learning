# Prompt Engineering Techniques

A personal reference guide for writing better prompts.

---

## 1. Be Clear and Direct

Tell the model exactly what you want. Avoid vague or ambiguous language.

| Bad | Good |
|-----|------|
| "Tell me about Python" | "Explain what a Python list comprehension is, with 2 short examples" |
| "Fix my code" | "This function returns None instead of the list. Find the bug and fix it." |
| "Write something about databases" | "Write a 3-sentence explanation of what an index is in a SQL database, for a beginner." |

**Rule:** If your prompt could mean multiple things, rewrite it until it can only mean one thing.

### Step-by-step: How to sharpen a vague prompt

1. Write your first draft prompt (even if vague)
2. Ask yourself: "What exactly do I want the output to look like?"
3. Ask yourself: "What should it NOT include?"
4. Add those details to your prompt

**Before:**
```
Tell me about sorting algorithms.
```

**After applying the steps:**
```
List 3 common sorting algorithms (bubble, merge, quicksort).
For each one, give: the time complexity and one sentence on when to use it.
Format it as a table.
```

---

## 2. Use a Role / Persona

Give Claude a role so it adopts the right tone and expertise level.

**Why it works:** The model adjusts its vocabulary, depth, and assumptions based on the role you give it.

### Role formula:
```
You are a [role]. [Task].
```

### Examples by use case:

| Goal | Role to use |
|------|-------------|
| Debug code | "You are a senior software engineer specializing in Python." |
| Simplify concepts | "You are a teacher explaining to a 10-year-old." |
| Write professional email | "You are a business communication expert." |
| Review security | "You are a cybersecurity engineer doing a code review." |
| Learn a concept | "You are a patient tutor. I am a complete beginner." |

### Step-by-step: Building a role prompt

1. Decide the domain (coding, writing, math, etc.)
2. Choose the expertise level that fits your need
3. Optionally describe your own level so the model calibrates its response

**Example (built step by step):**
```
Step 1 → domain: web development
Step 2 → expert level: senior engineer
Step 3 → my level: I'm a junior dev, 6 months experience
```

**Final prompt:**
```
You are a senior web developer. I am a junior developer with 6 months of experience.
Explain what CORS is and why browsers enforce it. Use a simple analogy.
```

---

## 3. Give Context

Provide background so the model understands *why* you're asking.

**Rule:** Answer these 3 questions inside your prompt:
- Who am I?
- What do I already know?
- Why am I asking this?

### Step-by-step: Adding context to a weak prompt

**Weak prompt:**
```
How do I use useState?
```

**Step 1 — Add who you are:**
```
I'm learning React for the first time.
How do I use useState?
```

**Step 2 — Add what you already know:**
```
I'm learning React for the first time. I understand JavaScript but not React hooks.
How do I use useState?
```

**Step 3 — Add why you're asking:**
```
I'm learning React for the first time. I understand JavaScript but not React hooks.
I'm building a simple counter app and I need to track a number that changes when I click a button.
How do I use useState to do this?
```

Each step makes the response more tailored and useful.

---

## 4. Specify Output Format

Tell the model *how* to respond — list, JSON, markdown, table, plain text, code only, etc.

**Rule:** If format matters to you, always state it explicitly.

### Common formats and when to use them:

| Format | When to use | Example instruction |
|--------|-------------|---------------------|
| Numbered list | Steps, rankings | "Respond as a numbered list" |
| Bullet points | Features, options | "Use bullet points only" |
| Table | Comparisons | "Format as a markdown table" |
| JSON | Data, APIs | "Return a JSON object with keys: x, y, z" |
| Code only | Clean output to copy | "Return only the code, no explanation" |
| Prose | Explanations, essays | "Write in full paragraphs" |

### Step-by-step: Specifying format for a comparison task

**Task:** Compare SQL vs NoSQL databases

**Without format:**
```
Compare SQL and NoSQL databases.
```
→ You get a long essay, hard to scan.

**With format:**
```
Compare SQL and NoSQL databases.
Format your answer as a table with these columns: Feature | SQL | NoSQL
Include rows for: data structure, scalability, use case, example database.
```
→ You get a clean, scannable table.

---

## 5. Few-Shot Prompting (Give Examples)

Show the model examples of the input → output pattern you want before asking your question.

**Why it works:** Examples are stronger than instructions — they show the model the exact pattern to follow.

### The pattern:
```
[Example input 1] → [Example output 1]
[Example input 2] → [Example output 2]
[Your actual input] → ?
```

### Step-by-step: Writing a few-shot prompt

**Goal:** Rewrite casual sentences into formal ones.

**Step 1 — Write 2 examples:**
```
Casual: "Hey, just checking if you got my email?"
Formal: "I wanted to follow up to confirm receipt of my previous message."

Casual: "The app keeps crashing, it's super annoying."
Formal: "The application is experiencing repeated crashes, which is causing significant disruption."
```

**Step 2 — Add your actual input:**
```
Casual: "I dunno when the meeting is, nobody told me."
Formal: ?
```

**Full prompt:**
```
Rewrite the following casual sentences into formal professional English.

Casual: "Hey, just checking if you got my email?"
Formal: "I wanted to follow up to confirm receipt of my previous message."

Casual: "The app keeps crashing, it's super annoying."
Formal: "The application is experiencing repeated crashes, which is causing significant disruption."

Casual: "I dunno when the meeting is, nobody told me."
Formal: ?
```

**Tip:** 2–3 examples is usually enough. More examples = more consistent output.

---

## 6. Chain of Thought (CoT)

Ask the model to think step by step before giving a final answer. Dramatically improves reasoning, math, and debugging.

**Rule:** Use CoT whenever the task involves logic, math, debugging, or multi-step reasoning.

### Two ways to trigger CoT:

**Option A — Explicit instruction:**
```
Think step by step before giving your final answer.
```

**Option B — Ask for reasoning first:**
```
First explain your reasoning, then give the final answer.
```

### Step-by-step: Applying CoT to a debugging problem

**Without CoT:**
```
Why does this function return undefined?

function getUser(id) {
  users.find(u => u.id === id)
}
```

**With CoT:**
```
Why does this function return undefined?
Think through it step by step: check the syntax, the logic, and what JavaScript implicitly returns.

function getUser(id) {
  users.find(u => u.id === id)
}
```

→ With CoT, the model will walk through: "The function has no return statement → arrow function body without braces → find() result is not returned → result is undefined." Much more useful than just "add a return statement."

---

## 7. Break Complex Tasks into Steps

Don't ask for everything at once. Split large tasks into smaller sub-tasks across multiple messages.

**Rule:** One task per prompt. If your prompt has "and" in it, consider splitting it.

### Step-by-step: Building a feature across multiple prompts

**Goal:** Build a user login system

**Wrong — one giant prompt:**
```
Build a login system with a database, API, JWT tokens, and a React frontend form.
```

**Right — step by step across messages:**

```
Message 1:
Design the database schema for a user login system.
Include: users table with id, email, hashed_password, created_at.
```

```
Message 2:
Based on this schema: [paste schema from Message 1]
Write a POST /login API endpoint in Python FastAPI that:
- Accepts email and password
- Verifies the password hash
- Returns a JWT token on success
```

```
Message 3:
Write a React login form component that:
- Has email and password fields
- Calls POST /login on submit
- Stores the returned JWT in localStorage
- Redirects to /dashboard on success
```

**Why this works:** Each step builds on the last. The model has focused context and produces better output than trying to do everything at once.

---

## 8. Set Constraints

Limit the scope, length, or style to get a focused and useful response.

**Rule:** Constraints reduce noise and keep responses on target.

### Types of constraints you can set:

| Type | Example |
|------|---------|
| Length | "In 3 bullet points only" / "Under 100 words" |
| Scope | "Focus only on the backend, not the UI" |
| Format | "No code, just plain English explanation" |
| Audience | "Explain it as if I'm 12 years old" |
| Exclusion | "Do not use recursion" / "No third-party libraries" |

### Step-by-step: Using constraints to get a precise answer

**Unconstrained prompt:**
```
How do I center a div in CSS?
```
→ You might get 6 different methods, history of CSS, and browser compatibility notes.

**With constraints:**
```
How do I center a div in CSS?
Give me only the modern flexbox approach.
Show the CSS code only, no explanation.
```
→ You get exactly what you need.

---

## 9. Ask for Alternatives

Request multiple options so you can evaluate and choose the best one.

**Why it works:** Forces the model to explore the solution space instead of defaulting to the first idea.

### Step-by-step: Getting useful alternatives

**Weak prompt:**
```
What should I name this function that fetches user data from an API?
```

**Better — ask for alternatives with tradeoffs:**
```
Give me 4 different name options for a function that fetches user data from an API.
For each name, give one sentence explaining when you would prefer it.
```

**Example output you'd get:**
- `fetchUser` — simple and direct, good for small codebases
- `getUserById` — more explicit, good when multiple fetch functions exist
- `loadUserProfile` — implies a UI loading action, good for frontend code
- `retrieveUserData` — formal/verbose, good for enterprise or API client code

Now you can make an informed choice instead of guessing.

---

## 10. Iterate and Refine

Prompting is a conversation. The first response is a draft — refine it with follow-ups.

**Rule:** You don't need the perfect prompt on the first try. Iterate toward what you want.

### Common refinement moves:

| Problem with response | Follow-up to use |
|----------------------|------------------|
| Too long | "Make it shorter, keep only the key points" |
| Too simple | "Go deeper on [specific part]" |
| Wrong tone | "Rewrite this in a more formal / casual tone" |
| Off-topic | "Ignore [X], focus only on [Y]" |
| Too abstract | "Give me a concrete code example for this" |
| Not specific enough | "Be more specific about [X]" |

### Step-by-step: A real iteration flow

**Round 1:**
```
You: Explain async/await in JavaScript.
Claude: [gives a long general explanation]
```

**Round 2 — narrow it:**
```
You: Good. Now focus only on error handling with try/catch inside async functions. Show a code example.
Claude: [gives focused example]
```

**Round 3 — push further:**
```
You: Now show me what happens if I forget the await keyword. What bug does it cause?
Claude: [explains the specific bug]
```

Each round gets more useful. This is more effective than writing one huge prompt upfront.

---

## Putting It All Together — Full Example

**Task:** You want Claude to help you review your Python code.

**Combining techniques 1, 2, 3, 4, 8:**

```
You are a senior Python engineer doing a code review. (Role)
I am a junior developer, 3 months into learning Python. (Context)

Review the following function for: (Clear + Scoped)
1. Correctness — does it do what it claims?
2. Edge cases — what inputs could break it?
3. Style — does it follow Python best practices?

Do NOT rewrite the function yet, just list the issues. (Constraint)
Format your response as a numbered list. (Output Format)

def get_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)
```

This prompt combines 5 techniques at once and will produce a focused, useful code review.

---

## Quick Reference Checklist

Before sending a prompt, ask yourself:

- [ ] Is my goal clear and specific?
- [ ] Did I give enough context (who I am, what I need, why)?
- [ ] Did I specify the output format I want?
- [ ] Should I add examples to show the pattern? (few-shot)
- [ ] Is this task too complex — should I split it?
- [ ] Should I ask it to think step by step? (CoT)
- [ ] Did I set constraints to avoid a bloated response?
- [ ] Should I ask for multiple alternatives?
