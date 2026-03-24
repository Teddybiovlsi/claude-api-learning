import ast
import re
from dotenv import load_dotenv
from anthropic import Anthropic
from statistics import mean

import json

load_dotenv()

client = Anthropic()
MODEL = "claude-haiku-4-5"

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": MODEL,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    
    response = client.messages.create(**params)
    return response.content[0].text

def generate_dataset():
    prompt = """
    Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.
    
    Example output:
    ```json
    [
        {
        "task": "Description of task",
        },
        ...additional
    ]
    ```
    
    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
    * Focus on tasks that do not require writing much code
    
    Please generate 3 objects.
    """
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    return json.loads(text)

# This function takes a test case and merges it with our prompt template:
def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
    Please solve the following task:
    {test_case["task"]}
    """
    
    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output

def validate_json_output(output) -> int:
    """Validates that the output is a JSON object and returns a score based on validity"""
    try:
        json.loads(output)
        return 10  # Perfect score for valid JSON
    except json.JSONDecodeError:
        return 0  # No points for invalid JSON
    
def validate_python_output(output) -> int:
    """Validates that the output is a valid Python function and returns a score based on validity"""
    try:
        ast.parse(output)
        return 10  # Perfect score for valid Python
    except SyntaxError:
        return 0  # No points for invalid Python
    
def validate_regex_output(output) -> int:
    """Validates that the output is a valid regex pattern and returns a score based on validity"""
    try:
        re.compile(output)
        return 10  # Perfect score for valid regex
    except re.error:
        return 0  # No points for invalid regex


# Implementing a Model Grader
# Function to grade a test case + output using a model
def grade_by_model(test_case, output):
    eval_prompt = f"""
You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

Original Task:
<task>
{test_case["task"]}
</task>

Solution to Evaluate:
<solution>
{output}
</solution>

Output Format
Provide your evaluation as a structured JSON object with the following fields, in this specific order:
- "strengths": An array of 1-3 key strengths
- "weaknesses": An array of 1-3 key areas for improvement
- "reasoning": A concise explanation of your overall assessment
- "score": A number between 1-10

Respond with JSON. Keep your response concise and direct.
Example response shape:
{{
    "strengths": string[],
    "weaknesses": string[],
    "reasoning": string,
    "score": number
}}

* Respond only with Python, JSON, or a plain Regex
* Do not add any comments or commentary or explanation
    """

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)


# The run test case Function
def run_test_case(test_case):
    """Runs a test case through the prompt and returns the output"""
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)
    
    # TODO - Grading
    model_grade = grade_by_model(test_case, output)
    score = model_grade["score"]
    reasoning = model_grade["reasoning"]
    
    return {
        "output": output,
        "test_case": test_case,
        "score": score,
        "reasoning": reasoning
    }

# The run eval Function
def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []
    
    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    average_score = mean(result["score"] for result in results)
    print(f"Average Score: {average_score}")
    
    return results