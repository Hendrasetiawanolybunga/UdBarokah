# 📚 Panduan Deployment UdBarokah - Hybrid Mode

## 🎯 Tujuan
Proyek ini telah dikonfigurasi untuk berjalan dalam **Hybrid Mode**:
- **Lokal (Full Features)**: Redis + Celery + WebSocket untuk notifikasi real-time
- **PythonAnywhere (Stable Mode)**: Tanpa Redis/WebSocket, menggunakan fallback yang aman

---

## 🔧 Perubahan yang Telah Dilakukan

### 1. **Settings.py - Environment Detection**
```python
ON_PYTHONANYWHERE = 'PYTHONANYWHERE_DOMAIN' in os.environ
```
- Deteksi otomatis apakah aplikasi berjalan di PythonAnywhere
- Konfigurasi menyesuaikan secara otomatis tanpa perlu edit manual

### 2. **Channel Layers (WebSocket)**
- **Lokal**: Menggunakan `RedisChannelLayer` untuk WebSocket real-time
- **PythonAnywhere**: Menggunakan `InMemoryChannelLayer` (fallback tanpa Redis)

### 3. **Celery Configuration**
- **Lokal**: Task berjalan async menggunakan Redis broker
- **PythonAnywhere**: `CELERY_TASK_ALWAYS_EAGER = True` (task berjalan sync)

### 4. **WebSocket Error Handling (base.html)**
- Menambahkan try-catch untuk koneksi WebSocket
- Menambahkan retry mechanism dengan exponential backoff
- Console log yang informatif (tidak crash aplikasi)
- Aplikasi tetap berfungsi normal jika WebSocket gagal

### 5. **.gitignore**
File-file berikut tidak akan ter-upload ke GitHub:
- `db.sqlite3` (database lokal)
- `__pycache__/` (Python cache)
- `media/` (file upload testing)
- `staticfiles/` (hasil collectstatic)
- `*.log`, `.env`, dll.

---

## 🚀 Cara Deploy ke PythonAnywhere

### **Step 1: Push ke GitHub**
```bash
cd f:\Hendra Skripsi\hosting\UdBarokah
git init
git add .
git commit -m "Initial commit - Hybrid deployment ready"
git branch -M main
git remote add origin https://github.com/USERNAME/udbarokah.git
git push -u origin main
```

### **Step 2: Setup di PythonAnywhere**

1. **Login ke PythonAnywhere** → Buka **Console** → Pilih **Bash**

2. **Clone Repository**
   ```bash
   git clone https://github.com/USERNAME/udbarokah.git
   cd udbarokah/UdBarokah
   ```

3. **Buat Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 udbarokah-env
   pip install -r requirements.txt
   ```

4. **Set Environment Variable (PENTING!)**
   Di **Web App Configuration** → **Environment variables**:
   ```
   PYTHONANYWHERE_DOMAIN = BlueCode46NttCode.pythonanywhere.com
   ```
   ✅ Ini akan mengaktifkan mode PythonAnywhere secara otomatis

5. **Collectstatic**
   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Migrate Database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. **WSGI Configuration**
   Di PythonAnywhere → **Web** → **WSGI configuration file**, edit:
   ```python
   import os
   import sys
   
   # Tambahkan path project
   path = '/home/BlueCode46NttCode/udbarokah/UdBarokah'
   if path not in sys.path:
       sys.path.append(path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'ProyekBarokah.settings'
   
   # Set environment variable untuk PythonAnywhere
   os.environ['PYTHONANYWHERE_DOMAIN'] = 'BlueCode46NttCode.pythonanywhere.com'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

8. **Static/Media Files Mapping**
   Di **Web** → **Static files**:
   ```
   URL: /static/
   Directory: /home/BlueCode46NttCode/udbarokah/UdBarokah/staticfiles
   
   URL: /media/
   Directory: /home/BlueCode46NttCode/udbarokah/UdBarokah/media
   ```

9. **Reload Web App**
   Klik tombol hijau **"Reload"** di Web tab

---

## 🧪 Testing

### **Di Lokal (Full Features)**
1. Jalankan Redis:
   ```bash
   redis-server
   ```

2. Jalankan Celery Worker:
   ```bash
   celery -A ProyekBarokah worker -l info
   ```

3. Jalankan Celery Beat (Scheduled Tasks):
   ```bash
   celery -A ProyekBarokah beat -l info
   ```

4. Jalankan Django dengan Daphne:
   ```bash
   daphne -b 0.0.0.0 -p 8000 ProyekBarokah.asgi:application
   ```

### **Di PythonAnywhere (Stable Mode)**
- WebSocket akan gagal gracefully (console log saja)
- Notifikasi tetap tersimpan di database
- Celery task berjalan synchronous (langsung saat dipanggil)
- Aplikasi berfungsi normal tanpa real-time notifications

---

## ⚠️ Catatan Penting

### **Limitasi PythonAnywhere Free Tier**
1. **WebSocket tidak didukung** → Notifikasi real-time tidak akan muncul (harus refresh manual)
2. **Celery Beat tidak berjalan** → Scheduled tasks (birthday discount) tidak otomatis
3. **File media terbatas** → Jangan upload file terlalu besar

### **Workaround untuk Birthday Discount**
Karena Celery Beat tidak jalan di Free Tier, Anda bisa:
- Jalankan manual: `python manage.py check_birthday` (buat custom command)
- Atau upgrade ke PythonAnywhere Paid Plan

### **Secret Key Production**
⚠️ **SEBELUM PRODUCTION**, ganti `SECRET_KEY` di settings.py dengan:
```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key')
```
Dan set environment variable `SECRET_KEY` di PythonAnywhere.

---

## 📞 Support

Jika ada masalah saat deployment:
1. Cek Error Log di PythonAnywhere: **Web** → **Log files**
2. Cek console.log di browser (F12) untuk WebSocket errors
3. Pastikan `PYTHONANYWHERE_DOMAIN` environment variable sudah di-set

---

## ✅ Checklist Sebelum Push

- [x] Environment detection sudah aktif
- [x] WebSocket error handling sudah ditambahkan
- [x] .gitignore sudah dibuat
- [x] STATIC_ROOT dan MEDIA_ROOT sudah benar
- [ ] Requirements.txt sudah ter-update (jalankan `pip freeze > requirements.txt`)
- [ ] Database lokal tidak ter-commit (cek .gitignore)
- [ ] Media files testing tidak ter-commit

---

**Happy Deployment! 🚀**
