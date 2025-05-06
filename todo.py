import sqlite3
import os
import tkinter as tk
from tkinter import messagebox

DB_FILE = os.getenv("TODO_DB", "todo.db")

# ------ Veritabanı Kurulum Fonksiyonu ------
def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                completed_date DATETIME
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Veritabanı Hatası", f"Veritabanı hatası: {e}")
        exit(1)

# ------ Veritabanı İşlemleri ------
def add_task_db(name):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (name, completed) VALUES (?, 0)", (name,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Veritabanı Hatası", f"Görev eklerken hata oluştu: {e}")

def get_tasks_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, completed, created_at, completed_date FROM tasks ORDER BY created_at")
        tasks = cursor.fetchall()
        conn.close()
        return tasks
    except sqlite3.Error as e:
        messagebox.showerror("Veritabanı Hatası", f"Veritabanı hatası: {e}")
        return []

def complete_task_db(task_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = 1, completed_date = CURRENT_TIMESTAMP WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Veritabanı Hatası", f"Görev tamamlama hatası: {e}")

def delete_task_db(task_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Veritabanı Hatası", f"Görev silme hatası: {e}")

# ------ GUI Bileşenleri ve Olaylar ------
def refresh_list():
    listbox.delete(0, tk.END)
    tasks = get_tasks_db()
    if not tasks:
        messagebox.showinfo("Bilgi", "Görev bulunmamaktadır.")
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

# ------ Uygulamayı Başlat ------
init_db()
root = tk.Tk()
root.title("Görev Takip Uygulaması")
root.geometry("700x500")

# Giriş çerçevesi
frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(frame, width=40)
entry.pack(side=tk.LEFT, padx=(0, 10))

add_btn = tk.Button(frame, text="Ekle", command=on_add)
add_btn.pack(side=tk.LEFT)

# Liste çerçevesi (scrollbar'lı)
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

# Buton çerçevesi
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

complete_btn = tk.Button(btn_frame, text="Tamamla", command=on_complete)
complete_btn.pack(side=tk.LEFT, padx=10)

delete_btn = tk.Button(btn_frame, text="Sil", command=on_delete)
delete_btn.pack(side=tk.LEFT, padx=10)

# Listeyi yenile
refresh_list()
root.mainloop()

