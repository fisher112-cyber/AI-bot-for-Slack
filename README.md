# AI bot for Slack

AI‑бот для корпоративного Slack:

- Публикует новости → `/newsbot`
- Принимает DM от сотрудников
- Отвечает через GPT‑4.1
- Эскалирует запросы в канал ИТ
- Работает через Socket Mode (не нужен публичный URL)
- Запускается как systemd‑сервис на Ubuntu 22.04

---

## 🚀 Установка

### 1. Клонировать репозиторий

git clone [https://github.com/your-user/AI-bot-for-Slack.git](https://github.com/fisher112-cyber/AI-bot-for-Slack)
cd AI-bot-for-Slack

### 2. Установить зависимости

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 3. Создать .env

cp .env.example .env

### 4. Запуск локально

python app.py

### 5. Установка как systemd сервис

sudo cp systemd/aibotforslack.service /etc/systemd/system/aibotforslack.service
sudo systemctl daemon-reload
sudo systemctl enable aibotforslack
sudo systemctl start aibotforslack
sudo systemctl status aibotforslack

---

## ✨ Возможности

### `/newsbot`
Формирует и публикует корпоративные новости.

### DM
Бот отвечает напрямую сотруднику.

### Упоминания `@CompanyInfoBot`
Рассматривает вопросы прямо в канале.

### Эскалация
Если GPT отвечает `ESCALATE: ...` → вопрос попадает в ИТ‑канал.

---

## 🧩 Требования
- Python 3.9+
- Slack App с включенным Socket Mode
- OpenAI API key

---

MIT License
