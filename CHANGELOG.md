# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.9.0] - 2026-03-28

### Removed
- **Tickets System Migration** - Support tickets moved to dedicated @uSipipoSupport_Bot
  - Removed commands: `/tickets`, `/nuevoticket`, `/mistickets`
  - Users should now use @uSipipoSupport_Bot for all support ticket operations
  - Support bot provides dedicated ticket management with same features

- **Deleted Files**
  - `src/bot/handlers/tickets.py` - Migrated to usipipo-support-bot
  - `src/bot/keyboards/tickets.py` - Migrated to usipipo-support-bot
  - `src/bot/keyboards/messages_tickets.py` - Migrated to usipipo-support-bot
  - `tests/bot/test_tickets_handlers.py` - Migrated to usipipo-support-bot
  - `tests/bot/test_tickets_keyboards.py` - Migrated to usipipo-support-bot
  - `tests/bot/test_tickets_messages.py` - Migrated to usipipo-support-bot
  - `tests/integration/test_tickets_integration.py` - Migrated to usipipo-support-bot

### Changed
- **Main Bot Focus** - Now focused on core VPN and payment features
- **Support Separation** - Support tickets handled by dedicated bot for better organization
- **Test Suite** - Reduced from 323 to ~290 tests (ticket tests migrated)

### Migration Guide
Users should:
1. Use @usipipobot for VPN, payments, subscriptions, referrals
2. Use @uSipipoSupport_Bot for support tickets and technical assistance

### Technical Details
- **Files Removed:** 7
- **Lines Removed:** ~800
- **Tests Migrated:** 58 tests to usipipo-support-bot
- **Breaking Change:** Yes - ticket commands no longer available

## [0.8.0] - 2026-03-28

### Added
- **Referrals System** - Invite friends, earn credits
  - Commands: `/referidos`, `/invitar`
  - Referral stats display with credits
  - Referral link generation (t.me/usipipobot?start={code})
  - Credit redemption (10 credits = 1 GB)
  
- **Tickets System** - Support ticket management
  - Commands: `/tickets`, `/nuevoticket`, `/mistickets`
  - Ticket creation with category selection (technical, billing, services, general)
  - Ticket list with status indicators (🟢 OPEN, 🟡 RESPONDED, 🔵 RESOLVED, 🔴 CLOSED)
  - Ticket detail view
  - Ticket closure

- **Referrals Components**
  - `ReferralsHandler` - Main handler with show_referrals, get_referral_link, redeem_credits_callback, apply_code_callback
  - `ReferralsKeyboard` - Inline keyboards: menu(), redeem_confirmation(), apply_code(), back_to_menu()
  - `ReferralsMessages` - UI messages: REFERRAL_STATS, INVITE_LINK, REDEEM_CONFIRMATION, APPLY_SUCCESS

- **Tickets Components**
  - `TicketsHandler` - Main handler with list_tickets, create_ticket, view_ticket_callback, close_ticket_callback, select_category_callback
  - `TicketsKeyboard` - Inline keyboards: tickets_list(), ticket_detail(), categories(), ticket_actions(), back_to_tickets()
  - `TicketsMessages` - UI messages: TICKETS_LIST, TICKET_DETAIL, CREATE_TICKET, TICKET_CREATED, TICKET_CLOSED

- **Tests**
  - 32 new unit tests (15 tickets, 13 referrals, 4 keyboards/messages each)
  - 4 integration tests (2 referrals, 2 tickets)
  - Total: 323 tests (319 passed, 1 skipped, 3 pre-existing failures)

- **Documentation**
  - Design doc: `usipipo-docs/plans/telegram-bot/2026-03-28-phase-7-referrals-tickets-design.md`
  - Flow docs: `usipipo-docs/flows/telegram-bot/referrals-flow.md`, `tickets-flow.md`
  - Migration progress updated to 75% (68/92 files)

### Backend Integration
- GET /api/v1/referrals/me - Referral statistics
- POST /api/v1/referrals/apply - Apply referral code
- POST /api/v1/referrals/redeem - Redeem credits for data
- POST /api/v1/tickets - Create support ticket
- GET /api/v1/tickets - List user tickets
- GET /api/v1/tickets/{id} - Get ticket with messages
- PATCH /api/v1/tickets/{id}/close - Close ticket

### Quality
- 32 new tests (323 total)
- Ruff clean
- Mypy clean
- Code review approved
- Branch protection enabled

### Files Created
- `src/bot/handlers/referrals.py` (~400 lines)
- `src/bot/handlers/tickets.py` (~500 lines)
- `src/bot/keyboards/referrals.py` (~120 lines)
- `src/bot/keyboards/messages_referrals.py` (~180 lines)
- `src/bot/keyboards/tickets.py` (~150 lines)
- `src/bot/keyboards/messages_tickets.py` (~220 lines)
- `tests/bot/test_referrals_handlers.py` (13 tests)
- `tests/bot/test_tickets_handlers.py` (15 tests)
- `tests/integration/test_referrals_integration.py` (2 tests)
- `tests/integration/test_tickets_integration.py` (2 tests)

## [0.7.1] - 2026-03-28

### 🔧 Pricing Corrections (Legacy Alignment)

#### Fixed
- **Data Packages Pricing** - Corrected to match legacy bot values
  - Básico: 10GB - 250 Stars ($2.08 USDT) ← was 5GB/600 Stars
  - Estándar: 30GB - 600 Stars ($5.00 USDT) ← was 10GB/1200 Stars
  - Avanzado: 60GB - 960 Stars ($8.00 USDT) ← was 25GB/3000 Stars
  - Premium: 120GB - 1440 Stars ($12.00 USDT) ← was 50GB/6000 Stars
  - Ilimitado: 200GB - 1800 Stars ($15.00 USDT) ← NEW

- **Subscriptions Pricing** - Corrected to match legacy bot values
  - 1 Month: 360 Stars ($2.99 USDT)
  - 3 Months: 900 Stars ($7.49 USDT)
  - 6 Months: 1680 Stars ($13.99 USDT)
  - 12 Months: 3000 Stars ($24.99 USDT)

#### Added
- **STARS_PER_USDT Constant** - Exchange rate configuration
  - `STARS_PER_USDT = 120` (1 USDT = 120 Telegram Stars)
  - Added in `src/infrastructure/config.py`

- **Pricing Documentation** - Comprehensive pricing reference
  - Created `/home/mowgli/usipipo/usipipo-docs/apis/pricing-structure.md`
  - 530 lines of pricing tables, formulas, and comparisons

#### Changed
- **Payment Keyboards** - Updated with correct USDT amounts
- **Payment Messages** - Updated menu with both Stars and USDT prices
- **packages.py** - Updated fallback packages with legacy pricing
- **subscriptions.py** - Updated fallback plans with legacy pricing

#### Technical Details
- **Exchange Rate:** 1 USDT = 120 Telegram Stars
- **Formula:** USDT = Stars / 120
- **Files Modified:** 5 (packages.py, subscriptions.py, payments.py, messages_payments.py, config.py)
- **Documentation:** 1 new file (530 lines)
- **Lines Changed:** 108 insertions, 65 deletions

---

## [0.7.0] - 2026-03-28

### 🎉 Payments + Subscriptions Complete

#### Added
- **Payments System** - Crypto (TronDealer) + Telegram Stars payments
- **Subscriptions System** - Plan management, activation, and renewal
- **Payment History** - View user payment history with pagination

- **New Commands**
  - `/pago` - Payment menu
  - `/pagar` - Payment menu (alias)
  - `/historial` - View payment history
  - `/suscripcion` - View subscription status
  - `/planes` - View available plans
  - `/renovar` - Renew subscription

- **New Handlers** (`src/bot/handlers/payments.py`)
  - `PaymentsHandler` class with all payment flows
  - Crypto payment via TronDealer
  - Stars payment via Telegram invoices
  - Payment history display

- **New Handlers** (`src/bot/handlers/subscriptions.py`)
  - `SubscriptionsHandler` class with all subscription flows
  - Plan selection and display
  - Subscription activation
  - Subscription renewal
  - Status display

- **New Keyboards** (`src/bot/keyboards/payments.py`, `subscriptions.py`)
  - Payment method selection (Crypto/Stars)
  - Crypto amount selection ($10, $25, $50, $100)
  - Stars amount selection
  - Payment history pagination
  - Plans list and selection
  - Subscription status menu

- **New Messages** (`src/bot/keyboards/messages_payments.py`, `messages_subscriptions.py`)
  - Payment instructions (Crypto & Stars)
  - Payment success/failure messages
  - Plan details and features
  - Subscription status messages
  - Activation/renewal confirmations

- **Testing**
  - 103 new unit tests (45 payments + 58 subscriptions)
  - Tests for all message templates and placeholders
  - Tests for all keyboard layouts
  - Tests for payment flows (Crypto & Stars)
  - 263 tests total (263 passed)

#### Changed
- Updated `src/main.py` to register PaymentsHandler and SubscriptionsHandler
- Enhanced bot structure with payments and subscriptions modules

#### Technical Details
- **Backend Integration:**
  - `POST /api/v1/payments/crypto` - Create crypto payment
  - `POST /api/v1/payments/stars` - Create Stars payment
  - `GET /api/v1/payments/history` - Get payment history
  - `GET /api/v1/subscriptions/me` - Get user subscription
  - `GET /api/v1/subscriptions/plans` - List available plans
  - `POST /api/v1/subscriptions/activate` - Activate subscription
  - `POST /api/v1/subscriptions/renew` - Renew subscription
- **Quality:** ruff (passed), pytest (263/263 passed), mypy (clean for new code)
- **Files Created:** 8 (handlers, keyboards, messages, tests)
- **Files Modified:** 1 (main.py)
- **Lines Added:** 3,726

#### Payment Methods
```python
# Crypto (USDT via TronDealer)
- $10, $25, $50, $100 amounts
- TronDealer webhook integration
- Automatic payment confirmation

# Telegram Stars
- 600, 1200, 3000, 6000 Stars
- Telegram invoice integration
- Pre-checkout validation
```

#### Subscription Plans
```python
[
    {"id": "basic", "name": "Basic", "price_usd": 9.99, "duration_days": 30},
    {"id": "standard", "name": "Standard", "price_usd": 19.99, "duration_days": 30},
    {"id": "premium", "name": "Premium", "price_usd": 29.99, "duration_days": 30},
]
```

---

## [0.6.0] - 2026-03-28

### 🎉 Data Packages Complete

#### Added
- **Data Packages System** - Buy GB data packages with flexible payment options
- **Telegram Stars Integration** - In-app purchases via Telegram
- **Crypto Payments** - USDT payments via TronDealer
- **Data Slots Management** - Manage multiple data packages
- **Data Usage Summary** - View consumption statistics

- **New Commands**
  - `/comprar` - Buy data packages
  - `/paquetes` - View available packages (alias)
  - `/packages` - View available packages (English alias)

- **New Handlers** (`src/bot/handlers/packages.py`)
  - `PackagesHandler` class with all package flows
  - Package selection and display
  - Stars payment flow with Telegram invoices
  - Crypto payment flow with TronDealer integration
  - Data slots management
  - Data usage summary display

- **New Keyboards** (`src/bot/keyboards/packages.py`)
  - `PackagesKeyboard` class with inline keyboards
  - Package selection menu
  - Payment method selection (Stars/Crypto)
  - Data summary display
  - Slots management menu
  - Payment success/failure keyboards

- **New Messages** (`src/bot/keyboards/messages_packages.py`)
  - `PackagesMessages` class with UI messages
  - Package menu and details
  - Payment instructions (Stars & Crypto)
  - Data summary format
  - Slots management messages
  - Error and success messages

- **Testing**
  - 55 new unit tests for data packages
  - Tests for all message templates and placeholders
  - Tests for all keyboard layouts
  - Tests for payment flows (Stars & Crypto)
  - 160 tests total (160 passed)

#### Changed
- Updated `src/main.py` to register PackagesHandler and all handlers
- Enhanced bot structure with data packages module

#### Technical Details
- **Backend Integration:**
  - `GET /api/v1/data-packages` - List available packages
  - `POST /api/v1/payments/stars` - Create Stars payment
  - `POST /api/v1/payments/stars/activate` - Activate package after payment
  - `POST /api/v1/payments/crypto` - Create crypto payment
  - `GET /api/v1/payments/crypto/{id}/status` - Check payment status
  - `GET /api/v1/users/me/data-summary` - Get user data usage
  - `GET /api/v1/users/me/slots` - Get user's data slots
  - `POST /api/v1/users/me/slots` - Buy extra slot
- **Quality:** ruff (passed), pytest (160/160 passed), mypy (clean for new code)
- **Files Created:** 4 (handlers, keyboards, messages, tests)
- **Files Modified:** 1 (main.py)
- **Lines Added:** 2,067

#### Package Options
```python
[
    {"id": "small", "name": "Pequeño", "data_gb": 5, "price_usd": 5.00, "price_stars": 600},
    {"id": "medium", "name": "Mediano", "data_gb": 10, "price_usd": 10.00, "price_stars": 1200},
    {"id": "large", "name": "Grande", "data_gb": 25, "price_usd": 25.00, "price_stars": 3000},
    {"id": "xl", "name": "XL", "data_gb": 50, "price_usd": 50.00, "price_stars": 6000},
]
```

---

## [0.5.0] - 2026-03-27

### 🎉 Consumption Billing Complete

#### Added
- **Consumption Billing System**
  - Pay-as-you-go consumption mode
  - 30-day billing cycles
  - Dynamic pricing ($0.25/GB)
  - Invoice generation with payment methods

- **New Commands**
  - `/consumo` - Show consumption menu (inactive/active/debt states)
  - `/activar` - Activate consumption mode (2-step confirmation flow)
  - `/cancelar` - Cancel consumption mode (with/without debt summary)
  - `/factura` - View invoices with pagination

- **New Handlers** (`src/bot/handlers/consumption.py`)
  - `ConsumptionHandler` class with all consumption flows
  - Menu with state-aware UI (inactive/active/debt)
  - Activation flow with terms acceptance
  - Cancellation flow with debt summary
  - Status view with consumption stats (GB, cost, days)
  - Invoice listing with pagination

- **New Keyboards** (`src/bot/keyboards/consumption.py`)
  - `ConsumptionKeyboard` class with 12 inline keyboard layouts
  - State-aware main menu (inactive/active/debt)
  - Activation confirmation and success keyboards
  - Cancellation confirmation (with/without debt)
  - Invoice list with pagination controls
  - Back navigation keyboards

- **New Messages** (`src/bot/keyboards/messages_consumption.py`)
  - `ConsumptionMessages` class with 7 nested message categories
  - Menu messages (INACTIVE_STATE, ACTIVE_STATE, DEBT_STATE)
  - Activation terms and conditions with pricing
  - Cancellation summary messages
  - Status display with consumption stats
  - Invoice list and payment messages
  - Comprehensive error messages

- **Testing**
  - 45 new unit tests for consumption billing
  - Tests for all message templates and placeholders
  - Tests for all keyboard layouts
  - Tests for handler initialization and authentication
  - 150 tests total (150 passed)

#### Changed
- Updated `src/main.py` to register ConsumptionHandler and callback handlers
- Enhanced `src/infrastructure/api_client.py` with headers support for GET/POST
- Updated `src/infrastructure/config.py` with consumption pricing constants

#### Technical Details
- **Backend Integration:**
  - `GET /api/v1/consumption/status` - Get consumption status
  - `GET /api/v1/consumption/status/can_activate` - Check activation eligibility
  - `POST /api/v1/consumption/activate` - Activate consumption mode
  - `GET /api/v1/consumption/status/can_cancel` - Check cancellation eligibility
  - `POST /api/v1/consumption/cancel` - Cancel consumption mode
  - `GET /api/v1/consumption/invoices/user/me` - Get user invoices with pagination
- **Quality:** ruff (passed), pytest (150/150 passed), mypy (clean for new code)
- **Files Created:** 4 (handlers, keyboards, messages, tests)
- **Files Modified:** 3 (main.py, api_client.py, config.py)
- **Lines Added:** 1,874

#### Configuration
```python
# Consumption Pricing
CONSUMPTION_PRICE_PER_GB_USD = 0.25
CONSUMPTION_PRICE_PER_MB_USD = 0.000244140625  # 0.25 / 1024
```

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
