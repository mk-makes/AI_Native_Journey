# A simple list to keep track of users who have visited during this run of the script.
# In a real application, this would typically be a database or file.
visited_users = []

# First, print a general welcome message to the user
print("Welcome to this interactive program!")

# Next, ask the user for their name and store their input in a variable
user_name = input("Please enter your name: ")

# --- Name-based Greeting (including MK's special greeting) ---
if user_name.strip().lower() == "MK":
    print(f"Hey, it's the awesome AI Director, {user_name}!")
else:
    # Check if this user is a "first-time" visitor in this session
    if user_name.strip().lower() not in [name.lower() for name in visited_users]:
        print(f"Hello, {user_name}! It looks like this is your first time here. Welcome aboard!")
        visited_users.append(user_name) # Add them to our 'visited' list
    else:
        print(f"Welcome back, {user_name}! Great to see you again.")

# --- Mood Check ---
user_mood = input("How are you feeling today? (e.g., great, tired, okay): ")

if "great" in user_mood.strip().lower() or "good" in user_mood.strip().lower():
    print("That's fantastic to hear! Let's make it an even better day.")
elif "tired" in user_mood.strip().lower() or "sleepy" in user_mood.strip().lower():
    print("Aww, I'm sorry to hear that. Maybe a quick stretch or a glass of water could help?")
elif "okay" in user_mood.strip().lower() or "fine" in user_mood.strip().lower():
    print("Okay, that's fair! Hope the program can brighten your day a little.")
else:
    print("Thanks for sharing! Whatever you're feeling, I hope you find something useful here.")

print("Enjoy your time with the program!")