import sqlite3

def update_completed_date(task_id):
    # Veritabanına bağlan
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    # completed_date'i güncelle
    cursor.execute("UPDATE tasks SET completed_date = CURRENT_TIMESTAMP WHERE id = ?", (task_id,))

    # Değişiklikleri kaydet
    conn.commit()
    conn.close()
    
    print(f"Task ID {task_id} için completed_date güncellendi.")

# Burada hangi task_id'yi güncellemek istediğinizi belirleyebilirsiniz
task_id = 1  # Örneğin task_id 1 olan görevi günceller

update_completed_date(task_id)
