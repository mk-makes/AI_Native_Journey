# This script generates a personalized welcome message for your GitHub AI Native repository.

def generate_welcome_message(repo_name, your_name="fellow developer"):
    """
    Generates a personalized welcome message.

    Args:
        repo_name (str): The name of your GitHub repository.
        your_name (str, optional): Your name or a general greeting for collaborators.
                                   Defaults to "fellow developer".

    Returns:
        str: The personalized welcome message.
    """
    message = f"Welcome, {your_name}, to the '{repo_name}' GitHub repository!\n"
    message += "We're thrilled to embark on this AI-native journey with you.\n"
    message += "Explore, contribute, and let's build something amazing together!"
    return message

if __name__ == "__main__":
    # --- Configuration ---
    # Replace 'YourAINativeRepo' with the actual name of your GitHub repository.
    repo_name = "AI-Native-Journey"
    # Optionally, replace "fellow developer" with your name if you want.
    # For example: your_name = "Alice"
    your_name = "fellow developer"
    # --- End Configuration ---

    welcome_message = generate_welcome_message(repo_name, your_name)
    print(welcome_message)