# 📚 Book Backend

**FastAPI + SQLAlchemy + MySQL** üzerine kurulmuş, hem **Admin Paneli** hem de **Kullanıcı Paneli (Panel API)** barındıran modern bir kitap yönetim sistemi.
JWT tabanlı kimlik doğrulama, soft-delete mimarisi, güçlü veri modelleri, pagination, favori sistemi ve temiz bir servis katmanı içerir.

---

## 🚀 Özellikler

### 🔐 Kimlik Doğrulama

- JWT Access Token
- Admin ve Panel kullanıcıları için ayrılmış giriş yapısı
- Şifre değiştirme
- Login history kaydı
- Hashleme (bcrypt)

### 📚 Kitap Yönetimi

- Kitap oluşturma, güncelleme, silme (soft-delete)
- Yazar & kategori ilişkileri
- Favori (wishlist) sistemi
- Favorite count (subquery)
- Pagination
- Arama & filtreleme özellikleri

### 🧑‍💼 Admin Panel

- Kullanıcı yönetimi
- Kitap yönetimi
- Yazar yönetimi
- Kategori yönetimi
- JWT ile korunan endpointler

### 👤 Panel (User)

- Üyelik sistemi (register, login)
- Profil işlemleri
- Aktif kategorileri listeleme
- Kitap listeleme & detay
- Favori işlemleri (ekle/çıkar)

---

# 🧱 Proje Yapısı

```
app/
├── core/               # İş kuralları (service/business layer)
│   ├── admin_user.py
│   ├── auth.py
│   ├── author.py
│   ├── book.py
│   ├── category.py
│   ├── favorite.py
│   └── user.py
│
├── database/           # Veritabanı bağlantısı ve Alembic migration yapısı
│   ├── database.py
│   └── migrations/
│       ├── versions/
│       ├── env.py
│       └── script.py.mako
│
├── enums/              # Projede kullanılan enum tanımları (Status vb.)
│   ├── base_enum.py
│   └── status_enum.py
│
├── helpers/            # Yardımcı fonksiyonlar (hash, error, jwt utils)
│   ├── error_helper.py
│   ├── hash_helper.py
│   └── secret_helper.py
│
├── models/             # SQLAlchemy ORM modelleri (tablolar)
│   ├── admin_user.py
│   ├── author.py
│   ├── book.py
│   ├── category.py
│   ├── favorite.py
│   └── user.py
│
├── schemas/            # Pydantic request/response modelleri
│   ├── admin/
│   ├── panel/
│   ├── base.py
│   └── pagination.py
│
├── views/             # API endpointleri (Admin & Panel)
│   ├── admin/
│   ├── panel/
│   ├── deps.py
│   └── config.py
│
└── main.py
```

---

# ⚙️ Kurulum

### 1️⃣ Depoyu klonla

```bash
git clone https://github.com/kullanici/book-backend.git
cd book-backend
```

### 2️⃣ Virtualenv oluştur

```bash
python -m venv venv
source venv/bin/activate
venv\Scripts\activate
```

### 3️⃣ Bağımlılıkları yükle

```bash
pip install -r requirements.txt
```

### 4️⃣ `.env` dosyasını oluştur

```
MYSQL_USER=root
MYSQL_ROOT_PASSWORD=your_mysql_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=bookdb

JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRES_TIME=15
```

### 5️⃣ Migration çalıştır

```bash
alembic upgrade head
```

### 6️⃣ Sunucuyu başlat

```bash
uvicorn app.main:app --reload
```

---

# 📍 Admin API Endpointleri

## 🔐 Auth

| Method | Endpoint                      |
| ------ | ----------------------------- |
| POST   | `/admin/auth/login`           |
| PUT    | `/admin/auth/change-password` |

## 📚 Book

| Method | Endpoint                |
| ------ | ----------------------- |
| GET    | `/admin/book`           |
| POST   | `/admin/book`           |
| GET    | `/admin/book/{book_id}` |
| PUT    | `/admin/book/{book_id}` |
| DELETE | `/admin/book/{book_id}` |

## ✍️ Author

| Method | Endpoint                    |
| ------ | --------------------------- |
| GET    | `/admin/author`             |
| POST   | `/admin/author`             |
| GET    | `/admin/author/{author_id}` |
| PUT    | `/admin/author/{author_id}` |
| DELETE | `/admin/author/{author_id}` |

## 🗂️ Category

| Method | Endpoint                        |
| ------ | ------------------------------- |
| GET    | `/admin/category`               |
| POST   | `/admin/category`               |
| GET    | `/admin/category/{category_id}` |
| PUT    | `/admin/category/{category_id}` |
| DELETE | `/admin/category/{category_id}` |

---

# 📍 Panel API Endpointleri

## 🔐 Auth

| Method | Endpoint          |
| ------ | ----------------- |
| POST   | `/panel/register` |
| POST   | `/panel/login`    |

## 🗂️ Category

| Method | Endpoint                        |
| ------ | ------------------------------- |
| GET    | `/panel/category`               |
| GET    | `/panel/category/{category_id}` |

## 📚 Book

| Method | Endpoint                         |
| ------ | -------------------------------- |
| GET    | `/panel/book`                    |
| GET    | `/panel/book/{book_id}`          |
| GET    | `/panel/book/favorite`           |
| POST   | `/panel/book/favorite/{book_id}` |
| DELETE | `/panel/book/favorite/{book_id}` |

## ✍️ Author

| Method | Endpoint                    |
| ------ | --------------------------- |
| GET    | `/panel/author`             |
| GET    | `/panel/author/{author_id}` |

---

# 🛠 Kullanılan Teknolojiler

- Python 3.13
- FastAPI 0.115+
- SQLAlchemy 2.x
- Pydantic 2.x
- MySQL
- Alembic
- JWT Authentication
- FastAPI Pagination

---

# 🗺 Yol Haritası (Roadmap)

- Refresh Token sistemi
- RBAC Role-Based Authorization
- Admin dashboard istatistik endpointleri
- Loglama sistemi
- Unit & integration test altyapısı
- ElasticSearch ile gelişmiş arama

---

# 📄 Lisans

MIT License
