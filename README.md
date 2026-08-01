# Account Management System

This project is a simple system for **account management**, including:
- Authentication (login, logout)
- Authorization (permissions, roles)

<br>

---

### Tech Stack

- Python 3.14
- Django 6
- Django rest framework 3
- PostgreSQL 18
- Docker & Docker-compose

<br>

---

### Run with Docker

You can start the project using Docker:

```bash
./scripts/docker.sh
```

This script will:
- Navigate to the `docker` folder
- Copy `.env.example` to `.env` if it does not exist
- Run Docker with build in detached mode

<br>

---

### Run with Script

You can start the project using the provided script:

```bash
./scripts/run.sh
```

You will be asked to enter a port:

```bash
Enter port (default 8000):
```

- Press **Enter** to use default port `8000`
- Or enter a custom port (e.g. `9000`)

<br>

---

### Run Manually

Follow these steps:

```bash
cd src
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

You can change the port if needed:

```bash
python manage.py runserver 0.0.0.0:<your_port>
```

<br>

---

### Result
- Admin site: Visit `/admin`
- API document: Visit `/api/docs`
- Check run tests result and coverage in [Github action summary](https://github.com/phamquiduong/account-management-system/actions), example: [Refactor project testing](https://github.com/phamquiduong/account-management-system/actions/runs/30657331518)
