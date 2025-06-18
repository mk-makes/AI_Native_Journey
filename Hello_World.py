# First, print a general welcome message to the user
print("Welcome to this interactive program!")

# Next, ask the user for their name and store their input in a variable
user_name = input("Please enter your name: ")

# Finally, use the entered name to give a personalized greeting
if user_name.strip().lower() == "MK":
    print(f"Hey, it's the awesome AI Director, {user_name}!")
else:
    print(f"Hello, {user_name}! It's great to meet you.")