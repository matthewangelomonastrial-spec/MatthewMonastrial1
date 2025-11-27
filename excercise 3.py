"""
Student Manager — Modern UI with Theme Switcher (Dark <-> Warm Light)
File format expected: studentMarks.txt
First line: number of students (n)
Each following line: id,name,c1,c2,c3,exam
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os

# -----------------------
# Configuration / Colors
# -----------------------
FILENAME = "studentMarks.txt"

# Theme palettes
THEMES = {
    "dark": {
        "bg": "#14141a",
        "panel": "#1e1e2f",
        "fg": "#E6E6E6",
        "subtext": "#A8AFB8",
        "accent": "#6C8CFF",
        "good": "#39D353",
        "bad": "#FF6B6B",
        "card": "#222235",
        "button_bg": "#2a2a3a"
    },
    "warm": {  # L3: Warm Light Mode (ivory / beige)
        "bg": "#FBF7F0",
        "panel": "#F2E9DD",
        "fg": "#2D2D2D",
        "subtext": "#6B6B6B",
        "accent": "#A97C50",
        "good": "#2E7D32",
        "bad": "#C62828",
        "card": "#FFF8F0",
        "button_bg": "#ECDCCF"
    }
}

# -----------------------
# Utility functions
# -----------------------
def calc_metrics(c1, c2, c3, exam):
    coursework = c1 + c2 + c3
    total = coursework + exam
    percentage = (total / 160.0) * 100.0
    if percentage >= 70:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"
    return coursework, total, percentage, grade

# -----------------------
# File handling
# -----------------------
def load_student_data(filename=FILENAME):
    students = []
    if not os.path.exists(filename):
        # create empty file
        with open(filename, "w") as f:
            f.write("0\n")
        return students
    try:
        with open(filename, "r") as file:
            lines = [ln.strip() for ln in file.readlines() if ln.strip()]
            if not lines:
                return students
            try:
                n = int(lines[0])
            except:
                # fallback: treat all lines as records
                data_lines = lines
            else:
                data_lines = lines[1:]
            for line in data_lines:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 6:
                    continue
                sid = int(parts[0])
                name = parts[1]
                c1, c2, c3, exam = map(int, parts[2:])
                coursework, total, percentage, grade = calc_metrics(c1, c2, c3, exam)
                students.append({
                    "id": sid, "name": name,
                    "c1": c1, "c2": c2, "c3": c3, "exam": exam,
                    "coursework": coursework, "total": total,
                    "percentage": percentage, "grade": grade
                })
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read {filename}:\n{e}")
    return students

def save_student_data():
    try:
        with open(FILENAME, "w") as f:
            f.write(str(len(student_data)) + "\n")
            for s in student_data:
                f.write(f"{s['id']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n")
        set_status("Saved to file.")
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save file:\n{e}")

# -----------------------
# GUI Helpers
# -----------------------
def set_status(msg):
    status_var.set(msg)

def apply_theme(theme_name):
    global CURRENT_THEME
    if theme_name not in THEMES:
        return
    CURRENT_THEME = theme_name
    pal = THEMES[theme_name]

    root.configure(bg=pal["bg"])
    main_frame.configure(bg=pal["bg"])
    left_panel.configure(bg=pal["panel"])
    right_panel.configure(bg=pal["bg"])
    controls_frame.configure(bg=pal["panel"])
    detail_card.configure(bg=pal["card"])
    status_bar.configure(bg=pal["panel"])
    # style ttk elements
    style.configure("TLabel", background=pal["panel"], foreground=pal["fg"])
    style.configure("Card.TLabel", background=pal["card"], foreground=pal["fg"])
    style.configure("TButton", background=pal["button_bg"], foreground=pal["fg"])
    style.map("TButton", background=[("active", pal["accent"])])
    style.configure("Treeview", background=pal["bg"], fieldbackground=pal["bg"], foreground=pal["fg"])
    style.configure("Treeview.Heading", background=pal["panel"], foreground=pal["fg"])
    # Buttons & text colors
    for btn in (btn_view_all, btn_view_ind, btn_add, btn_update, btn_delete, btn_sort, btn_highest, btn_lowest, btn_reload, theme_toggle_btn):
        btn.configure(bg=pal["button_bg"], fg=pal["fg"], activebackground=pal["panel"], bd=0, highlightthickness=0)
    # Treeview tag colors for grades
    tree.tag_configure("grade_A", foreground=pal["good"])
    tree.tag_configure("grade_F", foreground=pal["bad"])
    tree.tag_configure("grade_other", foreground=pal["fg"])
    # detail card text
    for child in detail_card.winfo_children():
        if isinstance(child, tk.Label):
            child.configure(bg=pal["card"], fg=pal["fg"])
    # status
    status_label.configure(bg=pal["panel"], fg=pal["subtext"])
    # accent for header label
    header_label.configure(bg=pal["bg"], fg=pal["fg"])
    # optional background image handling
    if bg_photo_img:
        # show image only in dark theme (makes sense) — warm mode uses flat color
        if theme_name == "dark" and bg_label is not None:
            bg_label.lift()
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            bg_label.place_forget()

def clear_tree():
    for item in tree.get_children():
        tree.delete(item)

def populate_tree():
    clear_tree()
    for s in student_data:
        tag = "grade_A" if s["grade"] == "A" else ("grade_F" if s["grade"] == "F" else "grade_other")
        tree.insert("", "end", iid=str(s["id"]), values=(
            s["id"], s["name"], s["c1"], s["c2"], s["c3"], s["exam"],
            s["coursework"], s["total"], f"{s['percentage']:.2f}", s["grade"]
        ), tags=(tag,))
    set_status(f"{len(student_data)} students displayed.")

def on_tree_select(event):
    sel = tree.focus()
    if not sel:
        show_detail(None)
        return
    sid = int(sel)
    s = next((x for x in student_data if x["id"] == sid), None)
    show_detail(s)

def show_detail(s):
    for w in detail_card.winfo_children():
        w.destroy()
    if not s:
        tk.Label(detail_card, text="Select a student to see details", font=("Helvetica", 11, "italic"), bg=THEMES[CURRENT_THEME]["card"], fg=THEMES[CURRENT_THEME]["subtext"]).pack(padx=8, pady=12)
        return
    # neat info layout
    tk.Label(detail_card, text=s["name"], font=("Helvetica", 14, "bold"), bg=THEMES[CURRENT_THEME]["card"], fg=THEMES[CURRENT_THEME]["fg"]).pack(anchor="w", padx=12, pady=(10,2))
    tk.Label(detail_card, text=f"Student ID: {s['id']}", font=("Helvetica", 10), bg=THEMES[CURRENT_THEME]["card"], fg=THEMES[CURRENT_THEME]["subtext"]).pack(anchor="w", padx=12)
    tk.Frame(detail_card, height=8, bg=THEMES[CURRENT_THEME]["card"]).pack()  # spacer

    info_frame = tk.Frame(detail_card, bg=THEMES[CURRENT_THEME]["card"])
    info_frame.pack(fill="both", expand=True, padx=10, pady=6)

    lbls = [
        ("Coursework (1,2,3)", f"{s['c1']}, {s['c2']}, {s['c3']}"),
        ("Coursework Total", str(s['coursework'])),
        ("Exam", str(s['exam'])),
        ("Total Marks", str(s['total'])),
        ("Percentage", f"{s['percentage']:.2f}%"),
        ("Grade", s['grade'])
    ]
    for i, (k, v) in enumerate(lbls):
        tk.Label(info_frame, text=k + ":", anchor="w", font=("Helvetica", 9, "bold"), bg=THEMES[CURRENT_THEME]["card"], fg=THEMES[CURRENT_THEME]["subtext"]).grid(row=i, column=0, sticky="w", padx=(0,6), pady=2)
        tk.Label(info_frame, text=v, anchor="w", font=("Helvetica", 9), bg=THEMES[CURRENT_THEME]["card"], fg=THEMES[CURRENT_THEME]["fg"]).grid(row=i, column=1, sticky="w", pady=2)

# -----------------------
# Actions
# -----------------------
def view_all_action():
    populate_tree()
    set_status("Viewing all students.")

def find_student_action():
    q = simpledialog.askstring("Find Student", "Enter student name or ID:")
    if not q:
        return
    ql = q.lower()
    found = []
    for s in student_data:
        if ql in s["name"].lower() or q == str(s["id"]):
            found.append(s)
    if not found:
        messagebox.showinfo("Not found", "No matching student found.")
        return
    # show first match and select it
    populate_tree()
    for s in found:
        tree.selection_set(str(s["id"]))
        tree.focus(str(s["id"]))
        tree.see(str(s["id"]))
        show_detail(s)
        break
    set_status(f"Found {len(found)} match(es).")

def add_student_action():
    AddOrUpdateDialog(root, title="Add Student", callback=add_student_callback)

def add_student_callback(data):
    # data: dict with id,name,c1,c2,c3,exam
    if any(str(data['id']) == str(s['id']) for s in student_data):
        messagebox.showerror("Duplicate ID", "A student with that ID already exists.")
        return
    coursework, total, percentage, grade = calc_metrics(data['c1'], data['c2'], data['c3'], data['exam'])
    s = {
        "id": data['id'], "name": data['name'],
        "c1": data['c1'], "c2": data['c2'], "c3": data['c3'], "exam": data['exam'],
        "coursework": coursework, "total": total,
        "percentage": percentage, "grade": grade
    }
    student_data.append(s)
    save_student_data()
    populate_tree()
    set_status(f"Added student {s['name']} (ID {s['id']}).")

def delete_student_action():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Select", "Please select a student to delete.")
        return
    sid = int(sel[0])
    s = next((x for x in student_data if x["id"] == sid), None)
    if not s:
        messagebox.showerror("Error", "Selected student not found.")
        return
    if not messagebox.askyesno("Confirm Delete", f"Delete {s['name']} (ID {s['id']})?"):
        return
    student_data.remove(s)
    save_student_data()
    populate_tree()
    show_detail(None)
    set_status(f"Deleted student ID {sid}.")

def update_student_action():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Select", "Please select a student to update.")
        return
    sid = int(sel[0])
    s = next((x for x in student_data if x["id"] == sid), None)
    if not s:
        messagebox.showerror("Error", "Selected student not found.")
        return
    AddOrUpdateDialog(root, title="Update Student", initial=s.copy(), callback=lambda d: update_student_callback(s, d))

def update_student_callback(orig, data):
    # update orig dict in-place
    orig["name"] = data["name"]
    orig["c1"] = data["c1"]
    orig["c2"] = data["c2"]
    orig["c3"] = data["c3"]
    orig["exam"] = data["exam"]
    coursework, total, percentage, grade = calc_metrics(orig["c1"], orig["c2"], orig["c3"], orig["exam"])
    orig["coursework"] = coursework
    orig["total"] = total
    orig["percentage"] = percentage
    orig["grade"] = grade
    save_student_data()
    populate_tree()
    tree.selection_set(str(orig["id"]))
    show_detail(orig)
    set_status(f"Updated student ID {orig['id']}.")

def sort_records_action():
    # Provide a simple sort dialog (choice)
    choices = [
        "Name (A → Z)", "Name (Z → A)",
        "Percentage (High → Low)", "Percentage (Low → High)",
        "ID (Ascending)", "ID (Descending)"
    ]
    choice = simpledialog.askstring("Sort", "Choose sorting:\n" + "\n".join(choices))
    if not choice:
        return
    if "Name (A" in choice:
        student_data.sort(key=lambda x: x["name"].lower())
    elif "Name (Z" in choice:
        student_data.sort(key=lambda x: x["name"].lower(), reverse=True)
    elif "High" in choice:
        student_data.sort(key=lambda x: x["percentage"], reverse=True)
    elif "Low" in choice:
        student_data.sort(key=lambda x: x["percentage"])
    elif "ID (Ascending" in choice:
        student_data.sort(key=lambda x: x["id"])
    elif "Descending" in choice:
        student_data.sort(key=lambda x: x["id"], reverse=True)
    else:
        messagebox.showinfo("Sort", "Unknown choice.")
        return
    populate_tree()
    set_status(f"Sorted by: {choice}")

def highest_action():
    if not student_data:
        messagebox.showinfo("No Data", "No students loaded.")
        return
    top = max(student_data, key=lambda s: s["total"])
    tree.selection_set(str(top["id"]))
    tree.focus(str(top["id"]))
    tree.see(str(top["id"]))
    show_detail(top)
    set_status(f"Highest scoring: {top['name']} ({top['percentage']:.2f}%).")

def lowest_action():
    if not student_data:
        messagebox.showinfo("No Data", "No students loaded.")
        return
    low = min(student_data, key=lambda s: s["total"])
    tree.selection_set(str(low["id"]))
    tree.focus(str(low["id"]))
    tree.see(str(low["id"]))
    show_detail(low)
    set_status(f"Lowest scoring: {low['name']} ({low['percentage']:.2f}%).")

def reload_action():
    global student_data
    student_data = load_student_data()
    populate_tree()
    show_detail(None)
    set_status("Reloaded from file.")

def toggle_theme():
    apply_theme("warm" if CURRENT_THEME == "dark" else "dark")

# -----------------------
# Dialog for Add / Update
# -----------------------
class AddOrUpdateDialog(tk.Toplevel):
    def __init__(self, parent, title="Add / Update", initial=None, callback=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.callback = callback
        self.initial = initial or {}
        # center window
        self.transient(parent)
        self.grab_set()
        pad = 10
        self.configure(bg=THEMES[CURRENT_THEME]["panel"])
        frm = tk.Frame(self, bg=THEMES[CURRENT_THEME]["panel"], padx=pad, pady=pad)
        frm.pack(fill="both", expand=True)

        # fields: id (disabled if updating), name, c1,c2,c3,exam
        row = 0
        tk.Label(frm, text="Student ID:", bg=THEMES[CURRENT_THEME]["panel"], fg=THEMES[CURRENT_THEME]["fg"]).grid(row=row, column=0, sticky="e", padx=(0,8), pady=6)
        self.ent_id = tk.Entry(frm)
        self.ent_id.grid(row=row, column=1, pady=6)
        if initial:
            self.ent_id.insert(0, str(initial.get("id", "")))
            self.ent_id.configure(state="disabled")
        row += 1

        tk.Label(frm, text="Name:", bg=THEMES[CURRENT_THEME]["panel"], fg=THEMES[CURRENT_THEME]["fg"]).grid(row=row, column=0, sticky="e", padx=(0,8), pady=6)
        self.ent_name = tk.Entry(frm, width=30)
        self.ent_name.grid(row=row, column=1, pady=6)
        if initial:
            self.ent_name.insert(0, initial.get("name", ""))
        row += 1

        # coursework and exam
        tk.Label(frm, text="Coursework 1:", bg=THEMES[CURRENT_THEME]["panel"], fg=THEMES[CURRENT_THEME]["fg"]).grid(row=row, column=0, sticky="e", padx=(0,8), pady=6)
        self.ent_c1 = tk.Entry(frm, width=8)
        self.ent_c1.grid(row=row, column=1, sticky="w", pady=6)
        if initial:
            self.ent_c1.insert(0, str(initial.get("c1", 0)))
        row += 1

        tk.Label(frm, text="Coursework 2:", bg=THEMES[CURRENT_THEME]["panel"], fg=THEMES[CURRENT_THEME]["fg"]).grid(row=row, column=0, sticky="e", padx=(0,8), pady=6)
        self.ent_c2 = tk.Entry(frm, width=8)
        self.ent_c2.grid(row=row, column=1, sticky="w", pady=6)
        if initial:
            self.ent_c2.insert(0, str(initial.get("c2", 0)))
        row += 1

        tk.Label(frm, text="Coursework 3:", bg=THEMES[CURRENT_THEME]["panel"], fg=THEMES[CURRENT_THEME]["fg"]).grid(row=row, column=0, sticky="e", padx=(0,8), pady=6)
        self.ent_c3 = tk.Entry(frm, width=8)
        self.ent_c3.grid(row=row, column=1, sticky="w", pady=6)
        if initial:
            self.ent_c3.insert(0, str(initial.get("c3", 0)))
        row += 1

        tk.Label(frm, text="Exam Mark:", bg=THEMES[CURRENT_THEME]["panel"], fg=THEMES[CURRENT_THEME]["fg"]).grid(row=row, column=0, sticky="e", padx=(0,8), pady=6)
        self.ent_exam = tk.Entry(frm, width=8)
        self.ent_exam.grid(row=row, column=1, sticky="w", pady=6)
        if initial:
            self.ent_exam.insert(0, str(initial.get("exam", 0)))
        row += 1

        # buttons
        btn_frame = tk.Frame(frm, bg=THEMES[CURRENT_THEME]["panel"])
        btn_frame.grid(row=row, column=0, columnspan=2, pady=(10,0))
        tk.Button(btn_frame, text="Cancel", command=self.cancel, bg=THEMES[CURRENT_THEME]["button_bg"], fg=THEMES[CURRENT_THEME]["fg"]).pack(side="right", padx=6)
        tk.Button(btn_frame, text="Save", command=self.on_save, bg=THEMES[CURRENT_THEME]["accent"], fg="#fff").pack(side="right", padx=6)

        self.bind("<Return>", lambda e: self.on_save())
        self.bind("<Escape>", lambda e: self.cancel())
        self.update_idletasks()
        self.center()

    def center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        pw = self.master.winfo_width()
        ph = self.master.winfo_height()
        px = self.master.winfo_rootx()
        py = self.master.winfo_rooty()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"+{x}+{y}")

    def on_save(self):
        try:
            sid = int(self.ent_id.get()) if self.ent_id.get() else None
            name = self.ent_name.get().strip()
            c1 = int(self.ent_c1.get())
            c2 = int(self.ent_c2.get())
            c3 = int(self.ent_c3.get())
            exam = int(self.ent_exam.get())
            if not name or sid is None:
                raise ValueError("Missing fields.")
            data = {"id": sid, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam}
            if self.callback:
                self.callback(data)
            self.destroy()
        except ValueError as ve:
            messagebox.showerror("Invalid", f"Please enter valid values.\n{ve}")

    def cancel(self):
        self.destroy()

# -----------------------
# Column sorting by header click
# -----------------------
_sort_reverse = {}
def treeview_sort_column(tv, col, numeric=False):
    global _sort_reverse
    items = [(tv.set(k, col), k) for k in tv.get_children('')]
    if numeric:
        items.sort(key=lambda t: float(t[0]) if t[0] != '' else 0, reverse=_sort_reverse.get(col, False))
    else:
        items.sort(key=lambda t: t[0].lower() if isinstance(t[0], str) else t[0], reverse=_sort_reverse.get(col, False))
    for index, (val, k) in enumerate(items):
        tv.move(k, '', index)
    _sort_reverse[col] = not _sort_reverse.get(col, False)

# -----------------------
# Build UI
# -----------------------
root = tk.Tk()
root.title("Student Manager — Modern UI")
root.geometry("1000x620")
root.minsize(920, 540)

style = ttk.Style(root)
# set default font
default_font = ("Helvetica", 10)

CURRENT_THEME = "dark"
student_data = load_student_data()

# Background image (only used in dark theme optionally)
bg_photo_img = None
bg_label = None
try:
    if os.path.exists("classroom.png"):
        im = Image.open("classroom.png")
        im = im.resize((1200, 800))
        bg_photo_img = ImageTk.PhotoImage(im)
    else:
        bg_photo_img = None
except Exception:
    bg_photo_img = None

# main frame
main_frame = tk.Frame(root, bg=THEMES[CURRENT_THEME]["bg"])
main_frame.pack(fill="both", expand=True)

# header
header_frame = tk.Frame(main_frame, bg=THEMES[CURRENT_THEME]["bg"])
header_frame.pack(fill="x", padx=12, pady=(12,6))
header_label = tk.Label(header_frame, text="Student Manager", font=("Segoe UI", 18, "bold"), bg=THEMES[CURRENT_THEME]["bg"], fg=THEMES[CURRENT_THEME]["fg"])
header_label.pack(side="left", padx=(6,10))

# theme toggle button
theme_toggle_btn = tk.Button(header_frame, text="Toggle Theme", command=toggle_theme, bd=0)
theme_toggle_btn.pack(side="right", padx=6)

# layout: left controls, right table + detail
content_frame = tk.Frame(main_frame, bg=THEMES[CURRENT_THEME]["bg"])
content_frame.pack(fill="both", expand=True, padx=12, pady=6)

left_panel = tk.Frame(content_frame, width=260, bg=THEMES[CURRENT_THEME]["panel"], relief="flat")
left_panel.pack(side="left", fill="y", padx=(0,10), pady=6)
left_panel.pack_propagate(False)

# controls inside left panel
controls_frame = tk.Frame(left_panel, bg=THEMES[CURRENT_THEME]["panel"])
controls_frame.pack(fill="both", expand=True, padx=12, pady=12)

btn_view_all = tk.Button(controls_frame, text="View All", command=view_all_action)
btn_view_all.pack(fill="x", pady=6)

btn_view_ind = tk.Button(controls_frame, text="Find Student", command=find_student_action)
btn_view_ind.pack(fill="x", pady=6)

btn_add = tk.Button(controls_frame, text="Add Student", command=add_student_action)
btn_add.pack(fill="x", pady=6)

btn_update = tk.Button(controls_frame, text="Update Selected", command=update_student_action)
btn_update.pack(fill="x", pady=6)

btn_delete = tk.Button(controls_frame, text="Delete Selected", command=delete_student_action)
btn_delete.pack(fill="x", pady=6)

btn_sort = tk.Button(controls_frame, text="Sort Records", command=sort_records_action)
btn_sort.pack(fill="x", pady=6)

btn_highest = tk.Button(controls_frame, text="Show Highest", command=highest_action)
btn_highest.pack(fill="x", pady=6)

btn_lowest = tk.Button(controls_frame, text="Show Lowest", command=lowest_action)
btn_lowest.pack(fill="x", pady=6)

btn_reload = tk.Button(controls_frame, text="Reload File", command=reload_action)
btn_reload.pack(fill="x", pady=6)

# right panel
right_panel = tk.Frame(content_frame, bg=THEMES[CURRENT_THEME]["bg"])
right_panel.pack(side="left", fill="both", expand=True)

# optional background image label (placed underneath right panel content)
if bg_photo_img:
    bg_label = tk.Label(right_panel, image=bg_photo_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# treeview table
table_frame = tk.Frame(right_panel, bg=THEMES[CURRENT_THEME]["bg"])
table_frame.pack(fill="both", expand=True, padx=(0,10), pady=6)

cols = ("ID", "Name", "C1", "C2", "C3", "Exam", "Coursework", "Total", "Percentage", "Grade")
tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse", height=14)
for c in cols:
    tree.heading(c, text=c, anchor="w")
    tree.column(c, anchor="w", width=80 if c != "Name" else 220, stretch=True)

# add vertical scrollbar
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")
hsb.grid(row=1, column=0, sticky="ew")
table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

# bind selection
tree.bind("<<TreeviewSelect>>", on_tree_select)

# column header click => sort
def heading_click(event):
    region = tree.identify_region(event.x, event.y)
    if region == "heading":
        col = tree.identify_column(event.x)
        # map to our column names
        col_idx = int(col.replace("#", "")) - 1
        col_name = cols[col_idx]
        numeric = col_name in ("ID", "C1", "C2", "C3", "Exam", "Coursework", "Total", "Percentage")
        treeview_sort_column(tree, col_name, numeric=numeric)

tree.bind("<Button-1>", heading_click)

# detail card
detail_card = tk.Frame(right_panel, bg=THEMES[CURRENT_THEME]["card"], relief="raised", bd=0)
detail_card.pack(fill="x", padx=(0,10), pady=(6,12))
show_detail(None)

# status bar
status_bar = tk.Frame(main_frame, bg=THEMES[CURRENT_THEME]["panel"])
status_bar.pack(fill="x", padx=12, pady=(0,12))
status_var = tk.StringVar()
status_label = tk.Label(status_bar, textvariable=status_var, anchor="w", font=("Helvetica", 9), bg=THEMES[CURRENT_THEME]["panel"], fg=THEMES[CURRENT_THEME]["subtext"])
status_label.pack(fill="x", padx=8, pady=6)

# menu
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Reload", command=reload_action)
filemenu.add_command(label="Save", command=save_student_data)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

viewmenu = tk.Menu(menubar, tearoff=0)
# (typo avoided; create view menu)
viewmenu = tk.Menu(menubar, tearoff=0)
viewmenu.add_command(label="View All", command=view_all_action)
viewmenu.add_command(label="Find Student", command=find_student_action)
menubar.add_cascade(label="View", menu=viewmenu)

editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Add Student", command=add_student_action)
editmenu.add_command(label="Update Selected", command=update_student_action)
editmenu.add_command(label="Delete Selected", command=delete_student_action)
menubar.add_cascade(label="Edit", menu=editmenu)

toolsmenu = tk.Menu(menubar, tearoff=0)
toolsmenu.add_command(label="Sort Records", command=sort_records_action)
toolsmenu.add_command(label="Highest", command=highest_action)
toolsmenu.add_command(label="Lowest", command=lowest_action)
toolsmenu.add_separator()
toolsmenu.add_command(label="Toggle Theme", command=toggle_theme)
menubar.add_cascade(label="Tools", menu=toolsmenu)

root.config(menu=menubar)

# apply theme and populate
apply_theme(CURRENT_THEME)
populate_tree()
set_status("Ready.")

# run
root.mainloop()


