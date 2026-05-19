# ⚡ 30 SEGUNDOS PARA EMPEZAR

## Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edita .env con PostgreSQL
python init_db.py
uvicorn app.main:app --reload
```

✅ http://localhost:8000/docs

## Frontend

```bash
cd frontend
npm install
npm start
```

✅ http://localhost:4200

## Usuarios

```
juan@elpoli.edu.co / juan123
maria@elpoli.edu.co / maria123
carlos@elpoli.edu.co / carlos123
ana@elpoli.edu.co / ana123
admin@elpoli.edu.co / admin123
```

---

**¡Listo! 🚀**
