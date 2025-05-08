# 📝 Basit Görev Takip Uygulaması (todo.py)

Bu proje Python, SQLite ve Tkinter kullanılarak geliştirilmiş basit bir grafik arayüzlü görev takip (ToDo) uygulamasıdır.

## 🚀 Özellikler

- **Görev ekleme**  
- **Görev listeleme**  
- **Görev tamamlama**  
- **Tamamlanma tarihi (completed date) gösterimi**  
- **SQLite veritabanı kullanımı**  
- **Grafik arayüz (GUI) ile kullanıcı dostu deneyim**  
- **Kullanıcı girişi (Login) desteği**  
- **Kullanıcı adı ve şifre doğrulama**  
- **Kullanıcı tablosu (users) ile giriş yapan kullanıcıya göre görev takibi**  
- **Görevlerin tamamlanma durumunu güncelleme**  

## 🧰 Gereksinimler

- Python 3.x  
- sqlite3 (Python ile birlikte gelir)  
- tkinter (GUI için)  

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

## 🖼️ Ekran Görüntüleri

### Görev Takip Arayüzü
![Kullanıcı 1 Görev Listesi](Assets/GUIuser1GörevlerListesi.png)

![Kullanıcı 2 Görev Listesi](Assets/GUIuser2GörevlerListesi.png)

### Kullanıcı Giriş Ekranı
![Kullanıcı Giriş Bilgileri](Assets/KullaniciGirişBilgileri.png)

### SQLite Veritabanı Yapısı
![SQLite Veritabanı Yapısı](Assets/SQLiteVeritabanıYapisi.png)

### Veritabanı Kullanıcı Tanımları
![Veritabanı Kullanıcı Tanımları](Assets/VeritabaniKullaniciTanimlari.png)

## 📂 Veritabanı Yapısı

**Görevler (tasks) tablosu:**  
- `id`: Birincil anahtar  
- `name`: Görev adı  
- `completed`: Görev tamamlandı mı? (0 veya 1)  
- `created_at`: Oluşturulma tarihi  
- `completed_date`: Tamamlandığı tarih  
- `user_id`: Görevi oluşturan kullanıcıya ait yabancı anahtar (foreign key)

**Kullanıcılar (users) tablosu:**  
- `id`: Birincil anahtar  
- `username`: Kullanıcı adı  
- `email`: Kullanıcı e-posta adresi  
- `password`: Kullanıcı şifresi  

## 👨‍💻 Geliştirici

Bu proje, öğrenme ve uygulama amacıyla geliştirilmiştir.

## 📜 Lisans

MIT Lisansı