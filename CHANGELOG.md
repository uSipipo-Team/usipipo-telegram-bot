# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-03-24

### 🎉 Initial Release - Invisible Authentication

#### Added
- **Invisible Authentication System**
  - Redis-based token storage with auto-refresh
  - AuthHandler with seamless auth flow
  - Auto-refresh 5 minutes before token expiry (30-day refresh tokens)
  
- **New Commands**
  - `/start` - Registration and automatic authentication
  - `/me` - Show user profile with auto-auth check
  - `/unlink` - Revoke bot access and delete tokens
  
- **Infrastructure**
  - `config.py` - pydantic-settings configuration
  - `redis.py` - RedisPool singleton with connection pooling
  - `token_storage.py` - TokenStorage for JWT management
  - `auth.py` (handlers) - AuthHandler class
  - `auth.py` (keyboards) - AuthMessages constants
  
- **CI/CD**
  - GitHub Actions workflow (ci.yml)
    - Lint (Ruff)
    - Type Check (Mypy)
    - Test (Pytest)
    - Security (Bandit)
  - Pre-commit configuration
  
- **Testing**
  - 45 tests total (44 passed, 1 skipped)
  - 6 integration tests with production backend
  - Unit tests for handlers, storage, and config
  
- **Documentation**
  - `INTEGRATION-TEST-SUMMARY.md` - Complete test documentation
  - Updated `README.md` with new commands

#### Changed
- Updated `main.py` to register auth handlers
- Enhanced `api_client.py` with production backend URL
- Updated `.env` with production configuration

#### Fixed
- Entry point duplication (`__main__.py`)
- Missing `__init__.py` files in packages
- mypy type errors in api_client, main, __main__
- ruff linting errors in tests

#### Technical Details
- **Backend Integration:** Production (https://usipipo.duckdns.org)
- **Token Storage:** Redis with 30-day expiry
- **Auto-Refresh:** 5 minutes before expiry
- **Quality:** mypy (0 errors), ruff (passed), pytest (44/45 passed)

---

## [0.0.1] - 2026-03-23

### 🌱 Project Setup

#### Added
- Initial project structure
- Basic commands (`/start`, `/help`, `/status`)
- API client for backend communication
- Logger and error handler
- Basic tests (11 tests)

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 0.1.0 | 2026-03-24 | Invisible Authentication + CI/CD + Integration Tests |
| 0.0.1 | 2026-03-23 | Project Setup + Basic Commands |

---

## Upcoming Features

### v0.2.0 - VPN Key Management
- `/keys` - List user's VPN keys
- `/newkey` - Create new VPN key
- `/delkey` - Delete VPN key
- `/qr` - Show QR code for key

### v0.3.0 - Payments Integration
- Crypto payments (TronDealer)
- Telegram Stars
- Subscription activation

### v0.4.0 - Advanced Features
- Ticket system
- Referral system
- Data packages
- Consumption billing

---

**Links:**
- **Repository:** https://github.com/uSipipo-Team/usipipo-telegram-bot
- **Releases:** https://github.com/uSipipo-Team/usipipo-telegram-bot/releases
- **PRs:** https://github.com/uSipipo-Team/usipipo-telegram-bot/pulls
