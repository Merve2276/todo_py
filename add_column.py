import sqlite3

# Veritabanı dosyasını aç
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# 'completed_date' sütununu ekle (eğer yoksa)
try:
    cursor.execute("ALTER TABLE tasks ADD COLUMN completed_date TEXT")
    print("completed_date alanı eklendi.")
except sqlite3.OperationalError:
    print("completed_date zaten mevcut.")

# Değişiklikleri kaydet
conn.commit()

# Bağlantıyı kapat
conn.close()

