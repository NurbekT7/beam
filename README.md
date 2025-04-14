# Beam

Проект `beam` — это Django-бэкенд с поддержкой WebSocket, REST API и админ-панели.

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/NurbekT7/beam.git
cd beam
```

### 2. Поднимите контейнеры

```bash
docker-compose up --build
```

### 3. Откройте новый терминал и войдите в контейнер `web`

```bash
docker exec -it web sh
```

### 4. Создайте суперпользователя (админа)

```bash
python manage.py createsuperuser
```

Пример:
- Email: `admin@gmail.com`
- Пароль: (введите при создании)

---

## 🔗 Полезные ссылки (для локального запуска)

- **REST API (Swagger):** [http://localhost](http://localhost)
- **API Endpoint Base URL:** `http://localhost/api`
- **WebSocket:** `ws://localhost/ws/orders`
- **Админ-панель Django:** [http://localhost/admin](http://localhost/admin)

---

## 🛠 Используемые технологии

- Python / Django
- Django REST Framework
- WebSockets
- Docker / Docker Compose
- Swagger (drf-yasg или аналог)

---

## 💬 От автора

Хотел бы добавить доп тулы, такие как Celery и другие, но спать охота 😴  
Обязательно допилю позже! За .env напишите мне в телеграм @talantbekow

---

## 📬 Контакты

Автор: [NurbekT7](https://github.com/NurbekT7)
