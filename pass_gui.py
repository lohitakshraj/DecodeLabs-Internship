"""
Password Strength Checker - GUI Version
Project 1 - DecodeLabs Industrial Training Kit
Author: [Lohitaksh Raj]
Batch: 2026
"""

import tkinter as tk
from tkinter import ttk
import re

# Common leaked passwords (bonus feature)
COMMON_LEAKED_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345",
    "qwerty", "abc123", "password1", "111111", "iloveyou",
    "admin", "welcome", "letmein", "monkey", "dragon",
    "sunshine", "princess", "qwerty123", "000000", "1q2w3e4r"
}


def analyze_password(password: str) -> dict:
    """Analyzes a password and returns score, strength, and feedback."""
    feedback = []
    score = 0
    checks = {
        "length": False,
        "uppercase": False,
        "lowercase": False,
        "number": False,
        "symbol": False
    }

    # Length check
    length = len(password)
    if length >= 12:
        score += 2
        checks["length"] = True
    elif length >= 8:
        score += 1
        checks["length"] = True
    else:
        feedback.append("Use at least 8 characters (12+ recommended)")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
        checks["uppercase"] = True
    else:
        feedback.append("Add at least one UPPERCASE letter")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
        checks["lowercase"] = True
    else:
        feedback.append("Add at least one lowercase letter")

    # Number
    if re.search(r"[0-9]", password):
        score += 1
        checks["number"] = True
    else:
        feedback.append("Add at least one number (0-9)")

    # Symbol
    if re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\\[\]~`';]", password):
        score += 1
        checks["symbol"] = True
    else:
        feedback.append("Add at least one symbol (e.g. !@#$%)")

    # Leaked password check
    is_leaked = password.lower() in COMMON_LEAKED_PASSWORDS
    if is_leaked:
        score = 0
        feedback.insert(0, "⚠ This password appears in known data leaks!")

    # Determine strength
    if not password:
        strength, color = "—", "#888888"
    elif score <= 2:
        strength, color = "WEAK", "#e74c3c"      # red
    elif score <= 4:
        strength, color = "MEDIUM", "#f39c12"    # orange
    else:
        strength, color = "STRONG", "#27ae60"    # green

    return {
        "score": score,
        "max_score": 6,
        "strength": strength,
        "color": color,
        "feedback": feedback,
        "checks": checks,
        "is_leaked": is_leaked,
        "length": length
    }


class PasswordCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LOHITAKSH RAJ - Password Strength Checker 🛡")
        self.root.geometry("520x640")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        self.show_password = False
        self.build_ui()

    def build_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="🛡  Password Strength Checker",
            font=("Helvetica", 20, "bold"),
            bg="#1e1e2e",
            fg="#ffffff"
        )
        title.pack(pady=(25, 5))

        subtitle = tk.Label(
            self.root,
            text="LOHITAKSH RAJ • Project 1 • Batch 25MAY-25JUNE,2026",
            font=("Helvetica", 11),
            bg="#1e1e2e",
            fg="#a0a0b0"
        )
        subtitle.pack(pady=(0, 20))

        # Password entry frame
        entry_frame = tk.Frame(self.root, bg="#1e1e2e")
        entry_frame.pack(pady=10)

        tk.Label(
            entry_frame,
            text="Enter your password:",
            font=("Helvetica", 12),
            bg="#1e1e2e",
            fg="#ffffff"
        ).pack(anchor="w")

        input_row = tk.Frame(entry_frame, bg="#1e1e2e")
        input_row.pack(pady=5)

        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self.on_password_change)

        self.entry = tk.Entry(
            input_row,
            textvariable=self.password_var,
            font=("Courier", 14),
            width=25,
            show="•",
            bg="#2d2d44",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            bd=8
        )
        self.entry.pack(side="left", padx=(0, 5))
        self.entry.focus()

        self.toggle_btn = tk.Button(
            input_row,
            text="👁",
            font=("Helvetica", 12),
            command=self.toggle_password,
            bg="#3d3d5c",
            fg="#ffffff",
            relief="flat",
            width=3,
            cursor="hand2"
        )
        self.toggle_btn.pack(side="left")

        # Strength label
        self.strength_label = tk.Label(
            self.root,
            text="—",
            font=("Helvetica", 22, "bold"),
            bg="#1e1e2e",
            fg="#888888"
        )
        self.strength_label.pack(pady=(20, 5))

        # Progress bar
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "strength.Horizontal.TProgressbar",
            troughcolor="#2d2d44",
            background="#888888",
            bordercolor="#1e1e2e",
            lightcolor="#888888",
            darkcolor="#888888"
        )

        self.progress = ttk.Progressbar(
            self.root,
            style="strength.Horizontal.TProgressbar",
            length=400,
            maximum=6,
            value=0
        )
        self.progress.pack(pady=5)

        self.score_label = tk.Label(
            self.root,
            text="Score: 0 / 6",
            font=("Helvetica", 11),
            bg="#1e1e2e",
            fg="#a0a0b0"
        )
        self.score_label.pack(pady=(2, 15))

        # Checklist frame
        checklist_frame = tk.Frame(self.root, bg="#27273d", padx=20, pady=15)
        checklist_frame.pack(padx=30, fill="x")

        tk.Label(
            checklist_frame,
            text="Requirements",
            font=("Helvetica", 12, "bold"),
            bg="#27273d",
            fg="#ffffff"
        ).pack(anchor="w", pady=(0, 8))

        self.check_labels = {}
        requirements = [
            ("length", "At least 8 characters"),
            ("uppercase", "Contains uppercase letter (A-Z)"),
            ("lowercase", "Contains lowercase letter (a-z)"),
            ("number", "Contains a number (0-9)"),
            ("symbol", "Contains a symbol (!@#$...)")
        ]

        for key, text in requirements:
            lbl = tk.Label(
                checklist_frame,
                text=f"○  {text}",
                font=("Helvetica", 11),
                bg="#27273d",
                fg="#a0a0b0",
                anchor="w"
            )
            lbl.pack(anchor="w", pady=2)
            self.check_labels[key] = (lbl, text)

        # Feedback / warning area
        self.feedback_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 10, "italic"),
            bg="#1e1e2e",
            fg="#f39c12",
            wraplength=450,
            justify="center"
        )
        self.feedback_label.pack(pady=15)

        # Footer
        footer = tk.Label(
            self.root,
            text="Powered by LOHITAKSH RAJ",
            font=("Helvetica", 9),
            bg="#1e1e2e",
            fg="#606075"
        )
        footer.pack(side="bottom", pady=10)

    def toggle_password(self):
        self.show_password = not self.show_password
        self.entry.config(show="" if self.show_password else "•")
        self.toggle_btn.config(text="🙈" if self.show_password else "👁")

    def on_password_change(self, *args):
        password = self.password_var.get()
        result = analyze_password(password)

        # Update strength label
        self.strength_label.config(text=result["strength"], fg=result["color"])

        # Update progress bar
        self.progress["value"] = result["score"]
        style = ttk.Style()
        style.configure(
            "strength.Horizontal.TProgressbar",
            background=result["color"],
            lightcolor=result["color"],
            darkcolor=result["color"]
        )

        # Update score
        self.score_label.config(text=f"Score: {result['score']} / {result['max_score']}")

        # Update checklist
        for key, (lbl, text) in self.check_labels.items():
            if result["checks"][key]:
                lbl.config(text=f"✓  {text}", fg="#27ae60")
            else:
                lbl.config(text=f"○  {text}", fg="#a0a0b0")

        # Update feedback
        if result["is_leaked"]:
            self.feedback_label.config(
                text="🚨 This password is in known data leaks. Choose another!",
                fg="#e74c3c"
            )
        elif not password:
            self.feedback_label.config(text="")
        elif result["feedback"]:
            self.feedback_label.config(
                text="Tip: " + result["feedback"][0],
                fg="#f39c12"
            )
        else:
            self.feedback_label.config(
                text="✅ Excellent! Your password is rock solid.",
                fg="#27ae60"
            )


def main():
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
