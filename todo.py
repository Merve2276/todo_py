import sqlite3
import os
import tkinter as tk
from tkinter import messagebox

DB_FILE = os.getenv("TODO_DB", "todo.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    cursor.execute("PRAGMA table_info(tasks)")
    cols = [col[1] for col in cursor.fetchall()]
    if "created_at" not in cols:
        cursor.execute("ALTER TABLE tasks ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP")
    if "completed_date" not in cols:
        cursor.execute("ALTER TABLE tasks ADD COLUMN completed_date DATETIME")
    conn.commit()
    conn.close()

def add_task_db(name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name, completed) VALUES (?, 0)", (name,))
    conn.commit()
    conn.close()

def get_tasks_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, completed, created_at, completed_date FROM tasks ORDER BY created_at")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def complete_task_db(task_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1, completed_date = CURRENT_TIMESTAMP WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def delete_task_db(task_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def refresh_list():
    listbox.delete(0, tk.END)
    tasks = get_tasks_db()
    for index, task in enumerate(tasks, start=1):
        status = "✅" if task[2] else "❌"
        created_at = task[3][:16]
        completed_at = task[4][:16] if task[4] else "—"
        listbox.insert(tk.END, f"{index}. {task[1]} {status} (Oluşturuldu: {created_at}, Tamamlandı: {completed_at}) (ID:{task[0]})")

def on_add():
    name = entry.get().strip()
    if name:
        add_task_db(name)
        entry.delete(0, tk.END)
        refresh_list()
    else:
        messagebox.showwarning("Uyarı", "Lütfen görev adı girin.")

def on_complete():
    sel = listbox.curselection()
    if sel:
        item = listbox.get(sel[0])
        task_id = int(item.split("ID:")[1].rstrip(')'))
        complete_task_db(task_id)
        refresh_list()
    else:
        messagebox.showwarning("Uyarı", "Tamamlanacak görevi seçin.")

def on_delete():
    sel = listbox.curselection()
    if sel:
        item = listbox.get(sel[0])
        task_id = int(item.split("ID:")[1].rstrip(')'))
        delete_task_db(task_id)
        refresh_list()
    else:
        messagebox.showwarning("Uyarı", "Silinecek görevi seçin.")

init_db()
root = tk.Tk()
root.title("Görev Takip Uygulaması")
root.geometry("700x500")

frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(frame, width=40)
entry.pack(side=tk.LEFT, padx=(0, 10))

add_btn = tk.Button(frame, text="Ekle", command=on_add)
add_btn.pack(side=tk.LEFT)

list_frame = tk.Frame(root)
list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar_y = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = tk.Scrollbar(root, orient=tk.HORIZONTAL)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

listbox = tk.Listbox(
    list_frame,
    width=100,
    height=15,
    yscrollcommand=scrollbar_y.set,
    xscrollcommand=scrollbar_x.set
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_y.config(command=listbox.yview)
scrollbar_x.config(command=listbox.xview)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

complete_btn = tk.Button(btn_frame, text="Tamamla", command=on_complete)
complete_btn.pack(side=tk.LEFT, padx=10)

delete_btn = tk.Button(btn_frame, text="Sil", command=on_delete)
delete_btn.pack(side=tk.LEFT, padx=10)

refresh_list()
root.mainloop()
