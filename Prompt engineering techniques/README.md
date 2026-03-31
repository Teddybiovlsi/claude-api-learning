# Prompt Engineering Techniques

A personal reference guide for writing better prompts.

---

## 1. Be Clear and Direct

Tell the model exactly what you want. Avoid vague or ambiguous language.

**When to use:** Always — this is the foundation of every prompt. Apply this before anything else.

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

**When to use:**
- You want the response at a specific expertise level (beginner-friendly vs. expert-level)
- You need a specific professional tone (engineer, teacher, lawyer, designer)
- The default response feels too generic or surface-level
- You want it to match your own skill level (e.g. "I'm a beginner")

**When NOT to use:** For simple factual questions where tone doesn't matter (e.g. "What year was Python created?")

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

**When to use:**
- The question is specific to your situation (not a general knowledge question)
- You have constraints the model needs to know (tech stack, language, framework)
- You've already tried something and it didn't work — say what you tried
- You're a beginner and want a simpler explanation

**When NOT to use:** Skip the background if it's a quick, universal question (e.g. "What does `===` mean in JavaScript?")

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

**When to use:**
- You're going to copy/paste the output somewhere (code editor, document, spreadsheet)
- You need to scan or compare information quickly (use a table or list)
- You're building something that parses the response (use JSON)
- The default response is longer or more verbose than what you need
- You want code only, without explanation (or explanation only, without code)

**When NOT to use:** If you just want a conversational answer and format doesn't matter, skip it.

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

**When to use:**
- You want the output to follow a very specific format or style that's hard to describe in words
- You're doing repetitive transformations (rewriting, classifying, extracting)
- The model keeps getting the format slightly wrong even after instructions
- You want consistent results across many inputs

**When NOT to use:** For one-off questions or when the task is simple enough that an instruction alone works fine. Examples add length — don't use them if they're not needed.

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

**When to use:**
- Math or calculation problems (the answer depends on intermediate steps)
- Debugging — you want to understand *why* something is wrong, not just the fix
- Logic or reasoning tasks (e.g. "which option is better and why?")
- Planning tasks where order matters
- When the first answer felt wrong — CoT forces the model to slow down and check itself

**When NOT to use:** For simple factual lookups or short answers where reasoning is not needed (e.g. "What is the capital of France?"). CoT adds length — only use it when depth matters.

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

**When to use:**
- Your task has multiple moving parts (schema + API + frontend)
- Each step depends on the output of the previous one
- The response quality drops when you ask for too much at once
- You want to review and approve each part before continuing
- You're building something large and need to stay in control

**When NOT to use:** If the task is small and self-contained — splitting it unnecessarily adds friction.

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

**When to use:**
- The response keeps being too long or covering things you don't need
- You have technical restrictions (no libraries, specific language version, character limit)
- You want to force a specific approach (e.g. "use recursion" or "do NOT use recursion")
- You're writing for a specific audience and need the right tone/complexity level
- You want to exclude things you already know so the response focuses on what's new

**When NOT to use:** Don't over-constrain. If you add too many restrictions, the model may struggle to give a useful answer. Use only the constraints that actually matter.

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

**When to use:**
- You're making a decision and want to compare options (naming, architecture, wording)
- You're not sure what the best approach is and want to see tradeoffs
- The first answer felt too narrow or opinionated
- You're brainstorming and want to explore possibilities before committing

**When NOT to use:** When there's clearly one right answer (e.g. "What is the syntax for a for loop in Python?"). Asking for alternatives there just adds noise.

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

**When to use:**
- The response was close but not quite right — don't rewrite the whole prompt, just correct the specific issue
- You want to go deeper on one part of a long response
- The tone, length, or focus was off
- You want to build on the response (e.g. "Now apply that to my actual code")
- You got a good answer and want to push it further

**When NOT to use:** If the response was completely off-base, it's sometimes faster to start fresh with a better prompt than to patch a bad response.

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

## 11. Use XML Tags to Structure Your Prompt

Wrap different parts of your prompt in XML tags to clearly separate instructions, context, code, and examples. Claude is trained to read XML tags and treats each section as distinct — this reduces confusion in complex prompts.

**When to use:**
- Your prompt has multiple distinct sections (instructions + code + examples)
- You're passing in long content like a document, codebase, or conversation history
- The model keeps mixing up what to do vs. what to read
- You want the model to only act on one part of the input and treat the rest as reference
- Your prompt is long enough that structure becomes important for clarity

**When NOT to use:** Short, single-purpose prompts don't need tags. "Explain recursion in 3 bullet points" is already clear without structure.

### Common XML tags and what they're for:

| Tag | Purpose |
|-----|---------|
| `<instructions>` | What you want the model to do |
| `<context>` | Background information for the model to know |
| `<code>` | Code you want analyzed, debugged, or reviewed |
| `<example>` | A sample input/output to show the pattern |
| `<document>` | A long piece of text to summarize or reference |
| `<output_format>` | How you want the response structured |
| `<question>` | The specific question to answer |

### Step-by-step: Converting a messy prompt to XML-structured

**Messy prompt (hard to parse):**
```
You are a senior Python engineer. I have this function that calculates average
but it crashes on empty lists. Here's the code: def get_average(numbers): return
sum(numbers) / len(numbers). Give me the fixed version and explain the edge cases.
Format the answer with the code first, then the explanation.
```

**Step 1 — Identify the sections:**
- Role → senior Python engineer
- Context → crashes on empty lists
- Code → the function
- Task → fix it and explain edge cases
- Format → code first, then explanation

**Step 2 — Wrap each section in a tag:**

```xml
<role>You are a senior Python engineer.</role>

<context>
I have a function that calculates the average of a list.
It crashes when the input list is empty.
</context>

<code>
def get_average(numbers):
    return sum(numbers) / len(numbers)
</code>

<instructions>
1. Fix the function to handle the empty list edge case.
2. Explain what other edge cases could still break it.
</instructions>

<output_format>
Show the fixed code first, then the explanation as a numbered list.
</output_format>
```

The model now knows exactly what each part is for and will not confuse the code with the instructions.

### Nested tags — for passing examples inside a prompt:

```xml
<instructions>
Classify the sentiment of each review as Positive, Negative, or Neutral.
</instructions>

<examples>
  <example>
    <input>The product works great, I love it!</input>
    <output>Positive</output>
  </example>
  <example>
    <input>It broke after two days, very disappointed.</input>
    <output>Negative</output>
  </example>
</examples>

<review>
Shipping was fast but the packaging was a bit damaged.
</review>
```

### Key rules for XML tags:

1. **Tag names are up to you** — use names that describe the content clearly
2. **Consistency matters** — use the same tag names throughout a project
3. **Claude will reference tag names in its response** — this helps you trace which part it's reacting to
4. **Combine with other techniques** — XML tags work especially well with Few-Shot (#5) and CoT (#6)

---

## Putting It All Together — Full Example

**Task:** You want Claude to help you review your Python code.

**Combining techniques 1, 2, 3, 4, 8, 11 (XML tags):**

```xml
<role>
You are a senior Python engineer doing a code review.
I am a junior developer, 3 months into learning Python.
</role>

<instructions>
Review the following function for:
1. Correctness — does it do what it claims?
2. Edge cases — what inputs could break it?
3. Style — does it follow Python best practices?

Do NOT rewrite the function yet, just list the issues.
</instructions>

<code>
def get_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)
</code>

<output_format>
Respond as a numbered list. One issue per item.
</output_format>
```

This prompt combines 6 techniques at once. The XML tags make each section unambiguous — the model knows exactly what to do, what to read, and how to respond.

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
- [ ] Is my prompt complex enough to benefit from XML tags to separate sections?
