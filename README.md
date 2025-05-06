# 📝 Basit Görev Takip Uygulaması (todo.py)

Bu proje Python, SQLite ve Tkinter kullanılarak geliştirilmiş basit bir grafik arayüzlü görev takip (ToDo) uygulamasıdır.

---

## 🚀 Özellikler

- Görev ekleme  
- Görev listeleme  
- Görev tamamlama  
- Tamamlanma tarihi (completed date) gösterimi  
- SQLite veritabanı kullanımı  
- Grafik arayüz (GUI) ile kullanıcı dostu deneyim

---

## 🧰 Gereksinimler

- Python 3.x  
- `sqlite3` (Python ile birlikte gelir)  
- `tkinter` (GUI için)

---

## 🛠️ Kurulum

1. Depoyu klonlayın:

```bash
git clone https://github.com/KULLANICIADIN/todo-app.git
cd todo-app
```

2. Gerekirse GUI modülünü kurun (Linux için):

```bash
sudo apt update
sudo apt install python3-tk
```

3. Uygulamayı başlatın:

```bash
python3 todo.py
```

---

## 🖼️ Ekran Görüntüleri

**Görev Takip Arayüzü:**

![GUI Görseli](assets/GUI.png)

**SQLite Veritabanı Yapısı:**

![SQLite Görseli](assets/SQLite.png)

---

## 📂 Veritabanı Yapısı

**Görevler (tasks) tablosu:**

- `id`: Birincil anahtar  
- `name`: Görev adı  
- `completed`: Görev tamamlandı mı? (`0` veya `1`)  
- `created_at`: Oluşturulma tarihi  
- `completed_date`: Tamamlandığı tarih  

**Kullanıcılar (users) tablosu:**

- `id`: Birincil anahtar  
- `username`: Kullanıcı adı  
- `email`: Kullanıcı e-posta adresi  

---

## 👨‍💻 Geliştirici

Bu proje, öğrenme ve uygulama amacıyla geliştirilmiştir.

---

## 📜 Lisans

MIT Lisansı