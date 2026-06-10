import tkinter as tk
from tkinter import ttk, filedialog
import os
from datetime import datetime
import shutil
import re

# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Website Manager")
root.geometry("800x600")

status_var = tk.StringVar()
status_var.set("Ready")

# =========================
# IMAGE PROCESSING
# =========================

def process_images(text):

    pattern = r"\[IMAGE:(.*?)\]"

    matches = re.findall(pattern, text)

    for image_path in matches:

        image_path = image_path.strip()

        if not os.path.exists(image_path):
            continue

        image_name = os.path.basename(image_path)

        destination = os.path.join(
            "assets",
            image_name
        )

        # Create assets folder if needed
        os.makedirs("assets", exist_ok=True)

        shutil.copy2(
            image_path,
            destination
        )

        html_tag = (
            f'<img src="../../assets/{image_name}">'
        )

        text = text.replace(
            f"[IMAGE:{image_path}]",
            html_tag
        )

    return text

# =========================
# INSERT IMAGE
# =========================

def insert_image():

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Images", "*.png *.jpg *.jpeg *.gif")
        ]
    )

    if file_path:

        content_text.insert(
            tk.INSERT,
            f"\n[IMAGE:{file_path}]\n"
        )

# =========================
# SAVE POST
# =========================

def save_post():

    section = section_var.get()

    title = title_entry.get().strip()

    if not title:
        status_var.set("Please enter a title.")
        return

    raw_content = content_text.get(
        "1.0",
        tk.END
    )

    content = process_images(raw_content)

    content = content.replace(
        "\n",
        "<br>\n"
    )

    timestamp = datetime.now()

    filename = (
        title.lower()
        .replace(" ", "-")
        .replace("/", "-")
    )

    folder = os.path.join(
        "content",
        section
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    filepath = os.path.join(
        folder,
        f"{filename}.html"
    )

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="../../style.css">
</head>
<body>

<a href="../../index.html">← Home</a>

<h1>{title}</h1>

<p class="timestamp">
{timestamp.strftime("%B %d, %Y %H:%M")}
</p>

<div class="post">

{content}

</div>

</body>
</html>
"""

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html_content)

    status_var.set(
        f"Saved: {filepath}"
    )

# =========================
# SECTION
# =========================

tk.Label(
    root,
    text="Section"
).pack(pady=5)

section_var = tk.StringVar()

section_dropdown = ttk.Combobox(
    root,
    textvariable=section_var,
    values=[
        "logs",
        "projects",
        "knowledge",
        "thoughts"
    ]
)

section_dropdown.pack(
    fill="x",
    padx=20
)

section_dropdown.current(0)

# =========================
# TITLE
# =========================

tk.Label(
    root,
    text="Title"
).pack(pady=5)

title_entry = tk.Entry(root)

title_entry.pack(
    fill="x",
    padx=20
)

# =========================
# CONTENT
# =========================

tk.Label(
    root,
    text="Content"
).pack(pady=5)

content_text = tk.Text(
    root
)

content_text.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

# =========================
# BUTTONS
# =========================

button_frame = tk.Frame(root)

button_frame.pack(
    pady=10
)

image_button = tk.Button(
    button_frame,
    text="Insert Image",
    command=insert_image
)

image_button.pack(
    side="left",
    padx=10
)

save_button = tk.Button(
    button_frame,
    text="Save",
    command=save_post
)

save_button.pack(
    side="left",
    padx=10
)

# =========================
# STATUS BAR
# =========================

status_label = tk.Label(
    root,
    textvariable=status_var
)

status_label.pack(
    side="bottom",
    pady=5
)

# =========================
# START APP
# =========================

root.mainloop()