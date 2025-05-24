
# ☕ Coffee App: FastAPI + Vue 3 + PostgreSQL

This project is a modern full-stack coffee-themed web app built with:
- 🔥 FastAPI backend
- 🎨 Vue 3 + Vuetify frontend
- 🐘 PostgreSQL (Dockerized)
- 🛠️ Makefile for easy dev setup
- ☁️ Docker + Colima support for macOS

---

## 🧰 Prerequisites

Install [Homebrew](https://brew.sh) if you haven't already.

```bash
brew install docker colima
```

---

## 🐳 Set Up Docker + Colima (macOS)

1. Start Colima with Docker runtime:

```bash
colima start --runtime docker
```

2. Set Docker to use Colima's socket:

```bash
export DOCKER_HOST=unix://${HOME}/.colima/default/docker.sock
```

To make it permanent, add that line to your shell profile (e.g., `.zshrc` or `.bash_profile`).

3. Run the database:

```bash
docker compose up -d
```

---

## ⚙️ Backend Setup (FastAPI)

```bash
python3 -m venv venv
source venv/bin/activate
make install
make run
```

You can also run the backend and frontend manually:

```bash
uvicorn backend.main:app --reload
cd frontend
npm run dev
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🌐 Frontend Setup (Vue 3 + Vuetify)

```bash
cd frontend
npm install
npm run dev
```

Visit: [http://localhost:5173](http://localhost:5173)

---

## 🛠️ Available Make Commands

```bash
make help
```

Will print:

- `make install` → set up virtualenv + frontend deps
- `make run` → run backend and frontend
- `make format` → run Black + Prettier
- `make help` → show all commands

---

## 📡 API Endpoints

| Endpoint              | Method | Description             |
|-----------------------|--------|-------------------------|
| `/coffees`            | GET    | List all coffees        |
| `/coffees`            | POST   | Add a new coffee        |
| `/coffees/{id}`       | DELETE | Delete a coffee         |
| `/brew/{id}`          | GET    | Brew selected coffee ✨  |

---


## 🛠️ Troubleshooting