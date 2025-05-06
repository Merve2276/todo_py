import sqlite3  # SQLite veritabanı işlemleri için
import os        # Ortam değişkenlerini okumak için
import tkinter as tk  # GUI oluşturmak için
from tkinter import messagebox

# Veritabanı dosyası; TODO_DB ortam değişkeni varsa onu, yoksa "todo.db" kullanır
DB_FILE = os.getenv("TODO_DB", "todo.db")

# ------ Veritabanı Kurulum Fonksiyonu ------
def init_db():
    """
    Veritabanı bağlantısı oluşturur ve
    'tasks' tablosu yoksa oluşturur.
    Eğer "created_at" sütunu yoksa tabloyu günceller.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Tabloyu oluştur (ilk kez)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )
    # Sütun bilgisini al
    cursor.execute("PRAGMA table_info(tasks)")
    cols = [col[1] for col in cursor.fetchall()]
    # Eğer created_at yoksa ekle
    if "created_at" not in cols:
        cursor.execute(
            "ALTER TABLE tasks ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"
        )
    conn.commit()
    conn.close()

# ------ Veritabanı İşlemleri ------

def add_task_db(name):
    """
    Yeni bir görev ekler (created_at otomatik).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name, completed) VALUES (?, 0)", (name,))
    conn.commit()
    conn.close()


def get_tasks_db():
    """
    Tüm görevleri oluşturulma tarihine göre döner.
    created_at küçükten büyüğe sıralama sağlar.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, completed, created_at FROM tasks ORDER BY created_at"
    )
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def complete_task_db(task_id):
    """
    Görevi tamamlanmış olarak işaretler.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def delete_task_db(task_id):
    """
    Görevi veritabanından siler.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# ------ GUI Bileşenleri ve Olaylar ------

def refresh_list():
    """
    Liste kutusunu günceller ve görevleri tarih sırasına göre numaralandırarak gösterir.
    """
    listbox.delete(0, tk.END)
    tasks = get_tasks_db()
    for index, task in enumerate(tasks, start=1):
        status = "✅" if task[2] else "❌"
        created_at = task[3][:16]  # Yıl-ay-gün saat:dakika
        listbox.insert(tk.END, f"{index}. {task[1]} {status} ({created_at}) (ID:{task[0]})")


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
root.geometry("500x400")

frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(frame, width=30)
entry.pack(side=tk.LEFT, padx=(0,10))

add_btn = tk.Button(frame, text="Ekle", command=on_add)
add_btn.pack(side=tk.LEFT)

listbox = tk.Listbox(root, width=70)
listbox.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

complete_btn = tk.Button(btn_frame, text="Tamamla", command=on_complete)
complete_btn.pack(side=tk.LEFT, padx=5)

delete_btn = tk.Button(btn_frame, text="Sil", command=on_delete)
delete_btn.pack(side=tk.LEFT, padx=5)

refresh_list()
root.mainloop()