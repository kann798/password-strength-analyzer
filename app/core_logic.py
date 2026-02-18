import re
import math
import os


# --------------------------------
# Load common passwords from file
# --------------------------------
def load_common_passwords():
    path = os.path.join(os.path.dirname(__file__), "common_passwords.txt")

    if not os.path.exists(path):
        return set()

    with open(path, "r", encoding="utf-8") as file:
        return {line.strip().lower() for line in file}


COMMON_PASSWORDS = load_common_passwords()


# --------------------------------
# Entropy Calculation
# --------------------------------
def calculate_entropy(password: str):
    pool = 0

    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"\d", password):
        pool += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        pool += 32

    if pool == 0:
        return 0

    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)


# --------------------------------
# Entropy Classification
# --------------------------------
def classify_entropy(entropy: float):
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Reasonable"
    elif entropy < 80:
        return "Strong"
    else:
        return "Very Strong"


# --------------------------------
# Main Evaluation Function
# --------------------------------
def evaluate_password(password: str):

    score = 0
    feedback = []
    is_common = False

    # Check common password (exact match)
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("This is a commonly used password. Choose a stronger one.")
        is_common = True

    patterns = {
        "length": r"^.{8,}$",
        "uppercase": r"[A-Z]",
        "lowercase": r"[a-z]",
        "digit": r"\d",
        "special": r"[!@#$%^&*(),.?\":{}|<>]"
    }

    # Length
    if re.match(patterns["length"], password):
        score += 1
    else:
        feedback.append("Password must be at least 8 characters long.")

    # Uppercase
    if re.search(patterns["uppercase"], password):
        score += 1
    else:
        feedback.append("Include at least one uppercase letter.")

    # Lowercase
    if re.search(patterns["lowercase"], password):
        score += 1
    else:
        feedback.append("Include at least one lowercase letter.")

    # Number
    if re.search(patterns["digit"], password):
        score += 1
    else:
        feedback.append("Include at least one number.")

    # Special character
    if re.search(patterns["special"], password):
        score += 1
    else:
        feedback.append("Include at least one special character.")

    # Rule-based strength classification
    if is_common:
        rule_strength = "Weak"
    elif not re.match(patterns["length"], password):
        rule_strength = "Weak"
    elif score == 5:
        rule_strength = "Strong"
    elif score >= 3:
        rule_strength = "Medium"
    else:
        rule_strength = "Weak"

    # Percentage score
    percentage = int((score / 5) * 100)

    # Entropy
    entropy = calculate_entropy(password)
    entropy_rating = classify_entropy(entropy)

    return rule_strength, percentage, entropy, entropy_rating, feedback
