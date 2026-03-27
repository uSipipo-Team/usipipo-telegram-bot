# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.4.0] - 2026-03-27

### 🎉 Operations + Profile Complete

#### Added
- **Operations Menu System**
  - Main operations menu with credits display
  - Shop menu with purchase options
  - Transactions history with pagination
  - Referrals program display

- **New Commands**
  - `/operaciones` - Operations menu

- **New Handlers** (`src/bot/handlers/operations.py`)
  - `OperationsHandler` class with all operations
  - Operations menu with credits integration
  - Credits display and redemption flow
  - Shop menu
  - Transactions history
  - Referrals program

- **New Keyboards** (`src/bot/keyboards/operations.py`)
  - `OperationsKeyboard` class with inline keyboards
  - Operations menu with credits
  - Credits redemption options
  - Shop categories
  - Transactions pagination
  - Referrals display

- **New Messages** (`src/bot/keyboards/messages_operations.py`)
  - `OperationsMessages` class with UI messages
  - Menu messages with credits
  - Credits display and redemption
  - Shop welcome message
  - Transactions history format
  - Referrals program info

- **Testing**
  - 21 new unit tests for operations
  - Tests for keyboards, messages, and handlers
  - 128 tests total (128 passed)

#### Changed
- Updated `src/main.py` to register OperationsHandler and callback handlers
- Enhanced bot structure with operations module

#### Technical Details
- **Backend Integration:**
  - `GET /api/v1/referrals/me` - Get referral stats
  - `GET /api/v1/transactions` - Get transactions history
- **Quality:** ruff (passed), pytest (128/128 passed)
- **Files Created:** 4 (handlers, keyboards, messages, tests)
- **Files Modified:** 1 (main.py)

---

## [0.3.0] - 2026-03-27

### 🎉 VPN Key Management Complete

#### Added
- **VPN Key Management System**
  - Full CRUD operations for VPN keys
  - Support for Outline and WireGuard protocols
  - Inline keyboards for key actions

- **New Commands**
  - `/keys` - List user's VPN keys with summary
  - `/newkey` - Create new VPN key (flow starter)

- **New Handlers** (`src/bot/handlers/keys.py`)
  - `KeysHandler` class with all VPN operations
  - List keys by type (Outline/WireGuard)
  - Show key details with usage statistics
  - Create new keys
  - Delete keys with confirmation
  - Rename keys
  - Download WireGuard .conf files
  - Get Outline access links
  - View key statistics

- **New Keyboards** (`src/bot/keyboards/keys.py`)
  - `KeysKeyboard` class with inline keyboards
  - Main menu with key counts
  - Key list by type
  - Key actions (download, rename, delete)
  - Confirmation dialogs

- **New Messages** (`src/bot/keyboards/messages_keys.py`)
  - `KeysMessages` class with UI messages
  - Main menu, key details, statistics
  - Action success/error messages
  - Progress bars for data usage

- **Testing**
  - 25 new unit tests for VPN key management
  - Tests for keyboards, messages, and handlers
  - 107 tests total (107 passed)

#### Changed
- Updated `src/main.py` to register KeysHandler and callback handlers
- Enhanced bot structure with VPN key management module

#### Technical Details
- **Backend Integration:**
  - `GET /api/v1/vpn/keys` - List keys
  - `POST /api/v1/vpn/keys` - Create key
  - `DELETE /api/v1/vpn/keys/{id}` - Delete key
  - `GET /api/v1/vpn/keys/{id}/config` - Get config
- **Quality:** ruff (passed), pytest (107/107 passed)
- **Files Created:** 4 (handlers, keyboards, messages, tests)
- **Files Modified:** 1 (main.py)

---

## [0.2.0] - 2026-03-24

### 📦 Project Structure + Metadata

#### Added
- **CHANGELOG.md** - Keep a Changelog format
- **README.md** - Updated with production status + version info
- **GitHub Topics** - 10 topics for discoverability
- **Repository Description** - Updated

#### Changed
- Updated project metadata
- Enhanced documentation

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
| 0.4.0 | 2026-03-27 | Operations + Profile Complete (21 tests, 128 total) |
| 0.3.0 | 2026-03-27 | VPN Key Management Complete (25 tests, 107 total) |
| 0.2.0 | 2026-03-24 | Project Structure + Metadata |
| 0.1.0 | 2026-03-24 | Invisible Authentication + CI/CD + Integration Tests |
| 0.0.1 | 2026-03-23 | Project Setup + Basic Commands |

---

## Upcoming Features

### v0.5.0 - Consumption Billing
- `/consumo` - Consumption menu
- `/activar` - Activate consumption mode
- `/cancelar` - Cancel consumption mode
- `/factura` - View invoices

### v0.6.0 - Data Packages
- `/comprar` - Buy data packages
- `/paquetes` - View available packages
- Payment with crypto and Telegram Stars

### v0.7.0 - Payments Integration
- Crypto payments (TronDealer)
- Telegram Stars
- Subscription activation

---

**Links:**
- **Repository:** https://github.com/uSipipo-Team/usipipo-telegram-bot
- **Releases:** https://github.com/uSipipo-Team/usipipo-telegram-bot/releases
- **PRs:** https://github.com/uSipipo-Team/usipipo-telegram-bot/pulls
