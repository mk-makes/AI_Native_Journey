# This script greets the user and calculates a “lucky number”
# python_debug_task.py
user_name = input("Hello! What's your name? ") # Corrected quotes
print(f"Nice to meet you, {user_name}!")# favorite_number = 7

# Attempt to calculate a lucky number
# Prompt the user to enter their favorite number
favorite_number_str = input("What's your favorite number? ")

# Convert the input string to an integer
# We use int() because input() always returns a string
favorite_number = int(favorite_number_str)

# Calculate the lucky number
lucky_number = favorite_number * 2

# Display the results
print(f"Your lucky number is: {lucky_number}")
print("Have a great day!")

