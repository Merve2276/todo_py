import sqlite3

# Veritabanına bağlan
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Güncellemek istediğiniz task_id'yi burada belirtin
task_id = 1  # Buraya uygun bir ID girin

# completed_date'i güncelle
cursor.execute("UPDATE tasks SET completed_date = CURRENT_TIMESTAMP WHERE id = ?", (task_id,))

# Değişiklikleri kaydet
conn.commit()

# Bağlantıyı kapat
conn.close()

print(f"Task ID {task_id} için completed_date güncellendi.")
