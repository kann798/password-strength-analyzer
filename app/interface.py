import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from app.core_logic import evaluate_password


def launch_gui():

    last_result = ""

    def toggle_password():
        if show_var.get():
            entry.config(show="")
        else:
            entry.config(show="*")

    def export_report():
        if not last_result:
            messagebox.showinfo("Info", "No analysis to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if not file_path:
            return

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(last_result)

        messagebox.showinfo("Success", "Report exported successfully.")

    def check_strength():
        nonlocal last_result

        password = entry.get()

        if not password:
            messagebox.showwarning("Input Error", "Please enter a password.")
            return

        rule_strength, percentage, entropy, entropy_rating, feedback = evaluate_password(password)

        result_text = (
            f"Rule Strength: {rule_strength} ({percentage}%)\n"
            f"Entropy: {entropy} bits ({entropy_rating})"
        )

        result_label.config(text=result_text)
        progress["value"] = percentage

        if rule_strength == "Strong":
            result_label.config(fg="green")
        elif rule_strength == "Medium":
            result_label.config(fg="orange")
        else:
            result_label.config(fg="red")

        suggestions_text.config(state="normal")
        suggestions_text.delete("1.0", tk.END)

        for item in feedback:
            suggestions_text.insert(tk.END, "- " + item + "\n")

        suggestions_text.config(state="disabled")

        last_result = result_text + "\n\nSuggestions:\n"
        for item in feedback:
            last_result += "- " + item + "\n"

    # ---------------- GUI Layout ----------------

    root = tk.Tk()
    root.title("Password Strength Analyzer")
    root.geometry("520x520")
    root.resizable(False, False)

    tk.Label(root,
             text="Advanced Password Strength Analyzer",
             font=("Arial", 14, "bold")).pack(pady=10)

    entry = tk.Entry(root, width=35, show="*")
    entry.pack(pady=5)

    show_var = tk.BooleanVar()
    tk.Checkbutton(root,
                   text="Show Password",
                   variable=show_var,
                   command=toggle_password).pack()

    tk.Button(root,
              text="Check Strength",
              command=check_strength).pack(pady=5)

    result_label = tk.Label(root,
                            text="",
                            font=("Arial", 12, "bold"),
                            justify="center")
    result_label.pack(pady=10)

    progress = ttk.Progressbar(root,
                                orient="horizontal",
                                length=350,
                                mode="determinate")
    progress.pack(pady=5)

    suggestions_text = tk.Text(root,
                                height=8,
                                width=60,
                                state="disabled")
    suggestions_text.pack(pady=10)

    tk.Button(root,
              text="Export Report",
              command=export_report).pack(pady=5)

    # Safe exit handling
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application closed.")
