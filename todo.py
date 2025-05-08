import sqlite3
import os
import logging
import tkinter as tk
from tkinter import messagebox

# ——— Logger kurulumu ———
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# Veritabanı dosyasını bu script’in bulunduğu klasöre sabitleyelim
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.getenv("TODO_DB", os.path.join(BASE_DIR, "todo.db"))

current_user_id = None  # Global kullanıcı ID'si

def get_connection():
    """Veritabanına bağlan ve hata durumunda logla."""
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Exception as e:
        logging.exception("Veritabanı bağlantı hatası:")
        raise

# Kullanıcı tablosunu oluştur
def create_users_table():
    conn = get_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
    conn.close()

# Görev tablosunu oluştur
def init_db():
    conn = get_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                completed_date DATETIME,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
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
        nonlocal username_entry, password_entry, login_win
        global current_user_id
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        row = cur.fetchone()
        conn.close()
        if row:
            current_user_id = row[0]
            login_win.destroy()
            start_app()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre.")

    def register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Uyarı", "Boş alan bırakmayın.")
            return
        conn = get_connection()
        try:
            with conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            messagebox.showinfo("Başarılı", "Kayıt oluşturuldu, şimdi giriş yapabilirsiniz.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut.")
        finally:
            conn.close()

    tk.Button(login_win, text="Giriş Yap", command=login).pack(pady=5)
    tk.Button(login_win, text="Kayıt Ol", command=register).pack(pady=5)
    login_win.mainloop()

# Yeni görev ekleme
def add_task_db(name):
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "INSERT INTO tasks (name, completed, user_id) VALUES (?, 0, ?)",
                (name, current_user_id)
            )
        logging.info("Görev eklendi: %s", name)
    except Exception:
        logging.exception("Görev eklenirken hata oluştu:")
    finally:
        conn.close()

# Görevleri getir
def get_tasks_db():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('''
            SELECT id, name, completed, created_at, completed_date
            FROM tasks
            WHERE user_id = ?
            ORDER BY created_at
        ''', (current_user_id,))
        return cur.fetchall()
    finally:
        conn.close()

# Görevi tamamla
def complete_task_db(task_id):
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "UPDATE tasks SET completed = 1, completed_date = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?",
                (task_id, current_user_id)
            )
        logging.info("Görev tamamlandı: ID %s", task_id)
    except Exception:
        logging.exception("Görev tamamlama hatası:")
    finally:
        conn.close()

# Görevi sil
def delete_task_db(task_id):
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, current_user_id)
            )
        logging.info("Görev silindi: ID %s", task_id)
    except Exception:
        logging.exception("Görev silme hatası:")
    finally:
        conn.close()

# Listeyi yenile
def refresh_list():
    listbox.delete(0, tk.END)
    try:
        tasks = get_tasks_db()
        for idx, (tid, name, done, created, comp) in enumerate(tasks, start=1):
            status = "✅" if done else "❌"
            created_at = created[:16]
            completed_at = comp[:16] if comp else "—"
            listbox.insert(
                tk.END,
                f"{idx}. {name} {status} (Oluşturuldu: {created_at}, Tamamlandı: {completed_at}) (ID:{tid})"
            )
    except Exception:
        logging.exception("Liste yenileme hatası:")

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
    if not sel:
        messagebox.showwarning("Uyarı", "Tamamlanacak görevi seçin.")
        return
    item = listbox.get(sel[0])
    task_id = int(item.split("ID:")[1].rstrip(')'))
    complete_task_db(task_id)
    refresh_list()

def on_delete():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Uyarı", "Silinecek görevi seçin.")
        return
    item = listbox.get(sel[0])
    task_id = int(item.split("ID:")[1].rstrip(')'))
    delete_task_db(task_id)
    refresh_list()

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
        list_frame, width=100, height=15,
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

if __name__ == "__main__":
    create_users_table()
    init_db()
    login_screen()


