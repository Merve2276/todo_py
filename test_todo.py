import sqlite3
import todo  # Uygulamanızın ana dosyasını import edin

# Test veritabanı
TEST_DB = "test_todo.db"

# Test öncesi veritabanı başlatma
def init_test_db():
    conn = sqlite3.connect(TEST_DB)
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

# Görev ekleme testi
def test_add_task():
    init_test_db()  # Test veritabanını başlat
    todo.add_task("Test Görevi")  # Görev ekle
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name, completed FROM tasks")
    task = cursor.fetchone()  # Veritabanından görev al
    conn.close()
    print(f"Added task: {task}")  # Görev eklenip eklenmediğini kontrol et
    assert task == ("Test Görevi", 0)  # Beklenen sonucu kontrol et

# Görev silme testi
def test_delete_task():
    init_test_db()  # Test veritabanını başlat
    todo.add_task("Silinecek Görev")  # Görev ekle
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE name = 'Silinecek Görev'")
    task = cursor.fetchone()  # Silinecek görevin ID'sini al
    conn.close()

    task_id = task[0] if task else None
    assert task_id is not None, "Görev bulunamadı"  # Görevin eklenip eklenmediğini kontrol et
    print(f"Task ID for deletion: {task_id}")

    todo.delete_task(task_id)  # Görev sil
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    deleted_task = cursor.fetchone()  # Silinmiş görevi kontrol et
    conn.close()
    print(f"Deleted task: {deleted_task}")
    assert deleted_task is None, "Görev silinemedi"  # Silinen görev bulunmamalı

# Görev tamamlama testi
def test_complete_task():
    init_test_db()  # Test veritabanını başlat
    todo.add_task("Tamamlama Testi Görevi")  # Görev ekle
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE name = 'Tamamlama Testi Görevi'")
    task = cursor.fetchone()  # Görevin ID'sini al
    conn.close()

    task_id = task[0] if task else None
    assert task_id is not None, "Görev bulunamadı"  # Görev eklenmediği için test başarısız olabilir
    print(f"Task ID for completion: {task_id}")

    todo.complete_task(task_id)  # Görevi tamamla
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
    completed = cursor.fetchone()[0]  # Görevin tamamlanma durumunu kontrol et
    conn.close()
    print(f"Task completion status: {completed}")
    assert completed == 1, "Görev tamamlanamadı"  # Tamamlanmış görev bekleniyor

