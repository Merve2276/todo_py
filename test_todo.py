import sqlite3
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timezone, timedelta

DB_FILE = os.getenv("TODO_DB", "todo.db")
current_user_id = None  # Global kullanıcı ID'si

# Kullanıcı tablosunu oluştur
def create_users_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Görev tablosunu oluştur
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL,
            completed_date DATETIME,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# Kullanıcı girişi
def login_screen():
    login_win = tk.Tk()
    login_win.title("Giriş Yap")
    login_win.geometry("300x200")

    tk.Label(login_win, text="Kullanıcı Adı").pack()
    username_entry = tk.Entry(login_win)
    username_entry.pack()

    tk.Label(login_win, text="Şifre").pack()
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    def login():
        global current_user_id
        username = username_entry.get()
        password = password_entry.get()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            current_user_id = result[0]
            login_win.destroy()
            start_app()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre.")

    def register():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showwarning("Uyarı", "Boş alan bırakmayın.")
            return
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt oluşturuldu, şimdi giriş yapabilirsiniz.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut.")
        conn.close()

    tk.Button(login_win, text="Giriş Yap", command=login).pack(pady=5)
    tk.Button(login_win, text="Kayıt Ol", command=register).pack(pady=5)
    login_win.mainloop()

# Yeni görev ekleme (Türkiye saatiyle)
def add_task_db(name):
    turkiye_saati = datetime.now(timezone(timedelta(hours=3)))  # UTC+3
    created_at = turkiye_saati.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (name, completed, created_at, user_id) VALUES (?, 0, ?, ?)",
        (name, created_at, current_user_id)
    )
    conn.commit()
    conn.close()

# Görevleri getir
def get_tasks_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, completed, created_at, completed_date FROM tasks
        WHERE user_id = ?
        ORDER BY created_at
    ''', (current_user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Görevi tamamla
def complete_task_db(task_id):
    turkiye_saati = datetime.now(timezone(timedelta(hours=3)))
    completed_at = turkiye_saati.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET completed = 1, completed_date = ? WHERE id = ? AND user_id = ?",
        (completed_at, task_id, current_user_id)
    )
    conn.commit()
    conn.close()

# Görevi sil
def delete_task_db(task_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, current_user_id))
    conn.commit()
    conn.close()

# Listeyi yenile
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

# Ana uygulama arayüzü
def start_app():
    global listbox, entry
    root = tk.Tk()
    root.title("Görev Takip Uygulaması")
    root.geometry("700x500")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    entry = tk.Entry(frame, width=40)
    entry.pack(side=tk.LEFT, padx=(0, 10))

    tk.Button(frame, text="Ekle", command=on_add).pack(side=tk.LEFT)

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

    tk.Button(btn_frame, text="Tamamla", command=on_complete).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Sil", command=on_delete).pack(side=tk.LEFT, padx=10)

    refresh_list()
    root.mainloop()

# Giriş ekranı başlat
create_users_table()
init_db()
login_screen()


