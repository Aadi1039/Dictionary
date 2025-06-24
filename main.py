import tkinter as tk
from tkinter import messagebox
import requests
import itertools

# ----- Function: Fetch & Display Definition -----
def get_definition():
    word = word_entry.get().strip()
    if not word:
        messagebox.showwarning("Input Required", "Please enter a word.")
        return

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        output.delete("1.0", tk.END)
        output.insert(tk.END, f"🔍 Word: {data[0]['word'].capitalize()}\n\n")

        for meaning in data[0]["meanings"]:
            part = meaning.get("partOfSpeech", "unknown")
            output.insert(tk.END, f"📌 Part of Speech: {part}\n")
            for idx, definition in enumerate(meaning["definitions"], start=1):
                output.insert(tk.END, f"  {idx}. {definition['definition']}\n")
                if "example" in definition:
                    output.insert(tk.END, f"     💡 Example: {definition['example']}\n")
            output.insert(tk.END, "\n")

    except requests.exceptions.HTTPError:
        output.delete("1.0", tk.END)
        output.insert(tk.END, "❌ No definition found. Try a different word.")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong!\n\n{e}")

# ----- GUI Setup -----
root = tk.Tk()
root.title("Seven Heaven Dictionary | Powered by Python")
root.geometry("800x560")
root.configure(bg="#f4f6f9")

# ----- Animated Color-Changing Background -----
# Define a list of colors to cycle through
bg_colors = ["#f4f6f9", "#e0f7fa", "#ffe082", "#ffd6e0", "#d1c4e9", "#b2dfdb", "#ffccbc"]
color_cycle = itertools.cycle(bg_colors)

def animate_bg():
    next_color = next(color_cycle)
    root.configure(bg=next_color)
    header.configure(bg=next_color)
    input_frame.configure(bg=next_color)
    # You can add more frames if you want them to match the background
    root.after(900, animate_bg)

# ----- Header -----
header = tk.Canvas(root, bg="#f4f6f9", height=90, highlightthickness=0)
header.pack(fill=tk.X, pady=(0, 8))

# Draw a rounded rectangle for the dark box
def draw_rounded_rect(canvas, x1, y1, x2, y2, radius=30, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

box = draw_rounded_rect(header, 120, 10, 680, 80, radius=30, fill="#181c24", outline="#0078d4", width=3)

title = header.create_text(400, 45, text="🧠 Seven Heaven Dictionary", font=("Segoe UI", 24, "bold"),
                           fill="#f4f6f9")

# Animated border shimmer
def animate_border():
    current_color = header.itemcget(box, "outline")
    next_color = "#00cfff" if current_color == "#0078d4" else "#0078d4"
    header.itemconfig(box, outline=next_color)
    root.after(700, animate_border)

animate_border()

# ----- Input Section -----
input_frame = tk.Frame(root, bg="#f4f6f9")
input_frame.pack(pady=10)

word_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=30,
                      relief="flat", bg="#ffffff", fg="#202124", bd=1)
word_entry.pack(side=tk.LEFT, ipady=6, padx=(0, 12))

search_btn = tk.Button(input_frame, text="Search", font=("Segoe UI", 12, "bold"),
                       bg="#0078d4", fg="white", activebackground="#005a9e",
                       relief="flat", padx=14, pady=6, cursor="hand2", command=get_definition)
search_btn.pack(side=tk.LEFT)

# ----- Output Panel -----
output_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
output_frame.pack(padx=30, pady=20, fill=tk.BOTH, expand=True)

output = tk.Text(output_frame, wrap=tk.WORD, font=("Segoe UI", 13),
                 bg="#ffffff", fg="#333333", padx=12, pady=12, bd=0)
output.pack(fill=tk.BOTH, expand=True)

animate_bg()  # <-- Moved line here, after header and input_frame are defined

# ----- Start the App -----
root.mainloop()
