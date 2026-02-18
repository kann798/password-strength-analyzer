from app.interface import launch_gui


def main():
    password = input("Enter your password: ")

    strength, feedback = evaluate_password(password)

    print("\nPassword Strength:", strength)

    if feedback:
        print("\nSuggestions:")
        for msg in feedback:
            print("-", msg)


if __name__ == "__main__":
    launch_gui()