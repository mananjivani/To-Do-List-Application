
import tkinter as tk
from tkinter import messagebox
import json
import os

# File used to save tasks
FILE_NAME = "tasks.json"

# Python list to store tasks
tasks = []


# Load tasks from file
def load_tasks():
    global tasks

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                tasks = json.load(file)

            if not isinstance(tasks, list):
                tasks = []

        except (json.JSONDecodeError, OSError):
            tasks = []

    refresh_tasks()


# Save tasks to file
def save_tasks():
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError as error:
        messagebox.showerror("File Error", str(error))


# Refresh task list in GUI
def refresh_tasks():
    task_list.delete(0, tk.END)

    for i, task in enumerate(tasks):
        status = "DONE" if task["completed"] else "PENDING"
        task_list.insert(
            tk.END, f"{i + 1}. {task['title']} [{status}]"
        )


# Add a task
def add_task():
    title = task_entry.get().strip()

    if not title:
        messagebox.showwarning(
            "Warning", "Please enter a task."
        )
        return

    tasks.append({
        "title": title,
        "completed": False
    })

    task_entry.delete(0, tk.END)
    save_tasks()
    refresh_tasks()


# Mark task completed or pending
def toggle_task():
    selection = task_list.curselection()

    if not selection:
        messagebox.showwarning(
            "Warning", "Please select a task."
        )
        return

    index = selection[0]
    tasks[index]["completed"] = not tasks[index]["completed"]

    save_tasks()
    refresh_tasks()


# Delete selected task
def delete_task():
    selection = task_list.curselection()

    if not selection:
        messagebox.showwarning(
            "Warning", "Please select a task."
        )
        return

    index = selection[0]

    if messagebox.askyesno(
        "Confirm", "Delete the selected task?"
    ):
        tasks.pop(index)
        save_tasks()
        refresh_tasks()


# Create main GUI window
root = tk.Tk()
root.title("To-Do List Application")
root.geometry("500x500")
root.configure(bg="#eef2f7")

# Heading
tk.Label(
    root,
    text="MY TO-DO LIST",
    font=("Arial", 22, "bold"),
    bg="#eef2f7",
    fg="#243b53"
).pack(pady=20)

# Task input
task_entry = tk.Entry(
    root,
    font=("Arial", 13),
    width=32
)
task_entry.pack(pady=8)

task_entry.bind(
    "<Return>", lambda event: add_task()
)

# Add button
tk.Button(
    root,
    text="Add Task",
    command=add_task,
    width=20,
    bg="#2563eb",
    fg="white"
).pack(pady=5)

# Task display
task_list = tk.Listbox(
    root,
    font=("Arial", 12),
    width=43,
    height=12
)
task_list.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)

# Complete button
tk.Button(
    root,
    text="Complete / Undo",
    command=toggle_task,
    width=20,
    bg="#16a34a",
    fg="white"
).pack(pady=4)

# Delete button
tk.Button(
    root,
    text="Delete Selected Task",
    command=delete_task,
    width=20,
    bg="#dc2626",
    fg="white"
).pack(pady=4)

# Footer
tk.Label(
    root,
    text="Python | Lists | File Handling | Tkinter GUI",
    bg="#eef2f7",
    fg="#52606d"
).pack(pady=12)

# Load previously saved tasks
load_tasks()

# Start application
root.mainloop()
