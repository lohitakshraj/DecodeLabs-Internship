"""
Password Strength Checker
Project 1 - DecodeLabs Industrial Training Kit
Author: [Lohitaksh Raj]
Batch: 2026
"""

import re

# A small list of commonly leaked/weak passwords (bonus feature)
COMMON_LEAKED_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345",
    "qwerty", "abc123", "password1", "111111", "iloveyou",
    "admin", "welcome", "letmein", "monkey", "dragon",
    "sunshine", "princess", "qwerty123", "000000", "1q2w3e4r"
}


def check_password_strength(password: str) -> dict:
    """
    Evaluates a password and returns a dictionary with the
    strength rating, score, and improvement feedback.
    """
    feedback = []
    score = 0

    # 1. Check length
    length = len(password)
    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    else:
        feedback.append("❌ Use at least 8 characters (12+ recommended).")

    # 2. Check for uppercase letters
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("❌ Add at least one UPPERCASE letter.")

    # 3. Check for lowercase letters
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Add at least one lowercase letter.")

    # 4. Check for numbers
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # 5. Check for symbols
    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\\[\]~`';]", password):
        score += 1
    else:
        feedback.append("❌ Add at least one symbol (e.g. !@#$%).")

    # 6. Bonus: check against common leaked passwords
    if password.lower() in COMMON_LEAKED_PASSWORDS:
        score = 0
        feedback.append("🚨 This password appears in known data leaks!")

    # Decide the strength label
    if score <= 2:
        strength = "WEAK 🔴"
    elif score <= 4:
        strength = "MEDIUM 🟡"
    else:
        strength = "STRONG 🟢"

    return {
        "password": password,
        "length": length,
        "score": score,
        "strength": strength,
        "feedback": feedback
    }


def display_result(result: dict) -> None:
    """Nicely prints the analysis result to the console."""
    print("\n" + "=" * 45)
    print("   PASSWORD STRENGTH ANALYSIS REPORT")
    print("=" * 45)
    print(f" Length   : {result['length']} characters")
    print(f" Score    : {result['score']} / 6")
    print(f" Strength : {result['strength']}")
    print("-" * 45)

    if result["feedback"]:
        print(" Suggestions to improve:")
        for tip in result["feedback"]:
            print(f"   {tip}")
    else:
        print(" ✅ Excellent! Your password meets all criteria.")
    print("=" * 45 + "\n")


def main():
    print("🛡  Welcome to the RAJ Password Strength Checker")
    print("   Type 'exit' anytime to quit.\n")

    while True:
        pwd = input("Enter a password to test: ").strip()
        if pwd.lower() == "exit":
            print("Goodbye! Stay secure. 👋")
            break
        if not pwd:
            print("⚠  Password cannot be empty. Try again.\n")
            continue

        result = check_password_strength(pwd)
        display_result(result)


if __name__ == "__main__":
    main()
