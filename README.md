
# SABI - Recipe Recommendation Backend

Backend Model 2 untuk merekomendasikan resep berdasarkan bahan
yang tersedia pada pengguna.

## Requirements

- Python 3.10 atau versi kompatibel
- pip

## Instalasi

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan di Windows CMD:

```bat
.venv\Scripts\activate.bat
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Menjalankan API

Masuk ke folder model:

```bash
cd sabi_recipe_model
```

Jalankan server:

```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Dokumentasi API:

http://127.0.0.1:8000/docs

## Endpoint rekomendasi

POST /recommend

Contoh request:

```json
{
  "ingredients": ["potatoes", "cheese", "milk"],
  "top_n": 5
}
```

Response berisi daftar rekomendasi resep, bahan yang cocok,
bahan yang kurang, dan langkah memasak.
