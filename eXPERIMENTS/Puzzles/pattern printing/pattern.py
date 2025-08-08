import time
import string

def print_with_twist(message):
    result = ""
    for ch in message:
        if ch == " ":
            result += " "
            continue
        # Skip non-alphabetic characters without cycling
        if ch.lower() not in string.ascii_lowercase:
            result += ch
            continue
        # Cycle through lowercase letters to find match
        for letter in string.ascii_lowercase:
            print(result + letter)
            time.sleep(0.09)
            if letter == ch.lower():
                break
        result += ch

# Add this to run the function
if __name__ == "__main__":
    # Get user input for the message
    user_message = input("Enter the message you want to display with the twist effect: ")
    print_with_twist(user_message)