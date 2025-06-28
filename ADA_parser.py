# ada_parser.py

def parse_prompt(prompt):
    """
    Parses a natural language prompt into structured data using a Role-Task-Format schema.
    Returns a dictionary with detected values.
    """
    parsed_prompt_data = {
        "role": "user",   # default assumption
        "task": None,
        "format": None
    }

    if "write" in prompt.lower():
        parsed_prompt_data["task"] = "write"
    if "blog post" in prompt.lower():
        parsed_prompt_data["format"] = "blog post"

    return parsed_prompt_data


def generate_thought_trace(prompt, parsed_data):
    """
    Generates a step-by-step explanation of how ADA parsed the prompt.
    Returns a list of thought trace entries.
    """
    thought_trace_log = []

    if "write" in prompt.lower():
        thought_trace_log.append("Detected task: 'write' based on keyword 'write'.")
    else:
        thought_trace_log.append("No specific task detected.")

    if "blog post" in prompt.lower():
        thought_trace_log.append("Detected format: 'blog post' from phrase match.")
    else:
        thought_trace_log.append("No specific format detected.")

    thought_trace_log.append(f"Defaulted role to '{parsed_data['role']}'.")

    return thought_trace_log


# --- Sample Run (can be removed/commented out for production) ---

if __name__ == "__main__":
    user_prompt = "Write a blog post about LLMs"
    parsed = parse_prompt(user_prompt)
    trace = generate_thought_trace(user_prompt, parsed)

    print("Parsed Prompt Data:")
    print(parsed)
    print("\nThought Trace:")
    for step in trace:
        print(step)
