import sqlite3
import argparse

# Veritabanını oluştur
def init_db():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

# Görev ekle
def add_task(name):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name, completed) VALUES (?, ?)", (name, 0))
    conn.commit()
    conn.close()
    print(f"Görev eklendi: {name}")

# Görevleri listele
def list_tasks():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    if tasks:
        print("Görevler:")
        for task in tasks:
            status = "Tamamlandı" if task[2] else "Tamamlanmadı"
            print(f"{task[0]}. {task[1]} - {status}")
    else:
        print("Hiç görev bulunmamaktadır.")

# Görevi tamamla
def complete_task(task_id):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"Görev {task_id} tamamlandı.")

# Menü (opsiyonel)
def interactive_menu():
    while True:
        print("\n1. Görev Ekle")
        print("2. Görev Listele")
        print("3. Görev Tamamla")
        print("4. Çık")
        choice = input("Seçiminizi yapın: ")

        if choice == "1":
            task_name = input("Görev adı: ")
            add_task(task_name)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            task_id = int(input("Görev numarası: "))
            complete_task(task_id)
        elif choice == "4":
            break
        else:
            print("Geçersiz seçim!")

# Ana fonksiyon (komut satırı desteği)
def main():
    init_db()

    parser = argparse.ArgumentParser(description="Görev yönetim uygulaması")
    parser.add_argument("command", nargs="?", help="Komut: add, list, complete")
    parser.add_argument("value", nargs="?", help="Görev adı veya ID")

    args = parser.parse_args()

    if args.command == "add" and args.value:
        add_task(args.value)
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete" and args.value:
        try:
            complete_task(int(args.value))
        except ValueError:
            print("Lütfen geçerli bir ID girin.")
    else:
        interactive_menu()

if __name__ == "__main__":
    main()

