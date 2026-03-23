# uSipipo Telegram Bot - Project Context

## 📋 Overview

**usipipo-telegram-bot** is the Telegram bot for user interaction in the uSipipo VPN ecosystem. It handles user commands, notifications, and provides access to VPN services via Telegram.

**Current Version:** v0.1.0  
**Status:** Pending Refactor  
**Framework:** python-telegram-bot v21+

---

## 🏗️ Architecture

### Project Structure

```
src/
├── __init__.py
├── __main__.py
├── main.py               # Bot entry point, handlers registration
├── core/
│   ├── config/
│   │   └── settings.py   # Pydantic settings
│   └── domain/
│       └── entities/     # Bot-specific entities
├── handlers/
│   ├── __init__.py
│   ├── start.py          # /start command
│   ├── help.py           # /help command
│   ├── keys.py           # VPN key management
│   ├── payments.py       # Payment handling
│   ├── subscriptions.py  # Subscription management
│   └── admin.py          # Admin commands
├── keyboards/
│   ├── __init__.py
│   ├── inline.py         # Inline keyboards
│   └── reply.py          # Reply keyboards
├── services/
│   ├── __init__.py
│   ├── backend_client.py # HTTP client to backend API
│   ├── notification_service.py
│   └── auth_service.py
└── utils/
    ├── __init__.py
    └── helpers.py        # Helper functions
```

### Communication Flow

```
┌──────────────┐     ┌─────────────────────┐     ┌────────────────┐
│   Telegram   │────▶│  usipipo-telegram   │────▶│ usipipo-backend│
│     User     │◀────│        -bot         │◀────│     (API)      │
└──────────────┘     └─────────────────────┘     └────────────────┘
                                                    │
                                                    ▼
                                             ┌────────────┐
                                             │ PostgreSQL │
                                             └────────────┘
```

---

## 🚀 Building and Running

### Prerequisites

- Python 3.13+
- uv package manager
- Telegram Bot Token

### Local Development

```bash
cd usipipo-telegram-bot

# Install dependencies
uv sync --dev

# Configure environment
cp example.env .env
# Edit .env with TELEGRAM_BOT_TOKEN and BACKEND_URL

# Run tests
uv run pytest

# Start bot
uv run python -m src
```

### Docker

```bash
# Build
docker build -t usipipo-telegram-bot .

# Run
docker run --env-file .env usipipo-telegram-bot
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | ✅ |
| `BACKEND_URL` | Backend API URL | ✅ |
| `APP_ENV` | Environment (development/production) | ❌ |
| `DEBUG` | Enable debug logging | ❌ |

---

## 🧪 Testing

### Run Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=src --cov-report=html

# Specific test file
uv run pytest tests/handlers/test_start.py -v
```

### Test Structure

```
tests/
├── unit/
│   ├── test_handlers/
│   ├── test_services/
│   └── test_keyboards/
├── integration/
│   └── test_backend_client.py
└── conftest.py
```

---

## 📦 Planned Features

### User Commands

| Command | Description | Status |
|---------|-------------|--------|
| `/start` | Welcome message, main menu | ⏳ |
| `/help` | Help information | ⏳ |
| `/mykeys` | List user's VPN keys | ⏳ |
| `/newkey` | Create new VPN key | ⏳ |
| `/usage` | Check data usage | ⏳ |
| `/plans` | View subscription plans | ⏳ |
| `/balance` | Check account balance | ⏳ |
| `/support` | Create support ticket | ⏳ |

### Admin Commands

| Command | Description | Status |
|---------|-------------|--------|
| `/admin` | Admin panel | ⏳ |
| `/stats` | System statistics | ⏳ |
| `/broadcast` | Send broadcast message | ⏳ |
| `/users` | User management | ⏳ |

### Notifications

| Type | Trigger | Status |
|------|---------|--------|
| Key Expiring | 3 days before expiry | ⏳ |
| Data Limit | Usage >= limit | ⏳ |
| Payment Confirmed | Payment processed | ⏳ |
| Subscription Active | Subscription activated | ⏳ |

---

## 🔧 Development Conventions

### Code Style

- **Line Length:** 100 characters
- **Quote Style:** Double quotes
- **Indent:** 4 spaces
- **Type Hints:** Required for all public functions

### Handler Pattern

```python
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    await update.message.reply_text(
        f"Welcome {user.first_name}! Use /help for commands."
    )
```

### Keyboard Pattern

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_keyboard() -> InlineKeyboardMarkup:
    """Create main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔑 My Keys", callback_data="keys")],
        [InlineKeyboardButton("📊 Usage", callback_data="usage")],
        [InlineKeyboardButton("💳 Plans", callback_data="plans")],
    ]
    return InlineKeyboardMarkup(keyboard)
```

### Backend Client Pattern

```python
import httpx
from typing import Optional

class BackendClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
    
    async def get_user_keys(self, user_id: int) -> list:
        """Fetch user's VPN keys from backend"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/vpn-keys",
                headers={"Authorization": f"Bearer {self.token}"},
                params={"user_id": user_id}
            )
            return response.json()
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/main.py` | Bot entry point |
| `src/__main__.py` | Python module entry |
| `src/handlers/` | Command handlers |
| `src/keyboards/` | Keyboard layouts |
| `src/services/backend_client.py` | HTTP client to backend |
| `pyproject.toml` | Project configuration |

---

## 🔗 Dependencies

### Runtime

- `usipipo-commons>=0.1.0`
- `python-telegram-bot>=21.0`
- `pydantic-settings>=2.0.0`

### Development

- `pytest>=8.0.0`
- `pytest-asyncio>=0.23.0`
- `pytest-cov>=4.0.0`
- `mypy>=1.0.0`
- `ruff>=0.1.0`
- `httpx>=0.27.0`
- `pre-commit>=3.6.0`

---

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Commands](docs/COMMANDS.md)
- [Deployment](docs/DEPLOYMENT.md)

---

## 🔗 Links

- **GitHub:** https://github.com/uSipipo-Team/usipipo-telegram-bot
- **Telegram:** https://t.me/uSipipo_Bot
- **Backend:** ../usipipo-backend/QWEN.md
- **Migration Tracker:** ../plans/MIGRATION-PROGRESS.md

---

**Last Updated:** 2026-03-21  
**Maintained By:** uSipipo Team <dev@usipipo.com>
