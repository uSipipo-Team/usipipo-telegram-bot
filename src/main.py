"""Telegram bot main module."""

import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from src.bot.handlers.basic import BasicHandler
from src.bot.handlers.auth import AuthHandler
from src.bot.handlers.keys import KeysHandler, get_keys_callback_handlers
from src.bot.handlers.operations import (
    OperationsHandler,
    get_operations_callback_handlers,
)
from src.bot.handlers.consumption import (
    ConsumptionHandler,
    get_consumption_handlers,
    get_consumption_callback_handlers,
)
from src.bot.handlers.packages import (
    PackagesHandler,
    get_packages_handlers,
    get_packages_callback_handlers,
    get_packages_payment_handlers,
)
from src.infrastructure.api_client import APIClient
from src.infrastructure.config import settings
from src.infrastructure.error_handler import error_handler
from src.infrastructure.logger import get_logger
from src.infrastructure.redis import RedisPool
from src.infrastructure.token_storage import TokenStorage

logger = get_logger("main")

# Global instances (initialized in create_application)
_api_client: APIClient | None = None
_token_storage: TokenStorage | None = None
_auth_handler: AuthHandler | None = None
_keys_handler: KeysHandler | None = None
_operations_handler: OperationsHandler | None = None
_consumption_handler: ConsumptionHandler | None = None
_packages_handler: PackagesHandler | None = None


async def _init_dependencies() -> None:
    """Inicializa dependencias globales del bot."""
    global _api_client, _token_storage, _auth_handler, _keys_handler, _operations_handler, _consumption_handler, _packages_handler

    # Initialize Redis pool
    await RedisPool.get_instance(settings.REDIS_URL)
    logger.info("Redis pool initialized")

    # Initialize API client
    _api_client = APIClient(
        base_url=settings.BACKEND_URL,
        api_prefix=settings.API_PREFIX,
    )
    logger.info(f"API client initialized: {settings.backend_base_url}")

    # Initialize token storage
    _token_storage = TokenStorage()
    logger.info("Token storage initialized")

    # Initialize auth handler
    _auth_handler = AuthHandler(_api_client, _token_storage)
    logger.info("Auth handler initialized")

    # Initialize keys handler
    _keys_handler = KeysHandler(_api_client, _token_storage)
    logger.info("Keys handler initialized")

    # Initialize operations handler
    _operations_handler = OperationsHandler(_api_client, _token_storage)
    logger.info("Operations handler initialized")

    # Initialize consumption handler
    _consumption_handler = ConsumptionHandler(_api_client, _token_storage)
    logger.info("Consumption handler initialized")

    # Initialize packages handler
    _packages_handler = PackagesHandler(_api_client, _token_storage)
    logger.info("📦 Packages handler initialized")


def _get_auth_handler() -> AuthHandler:
    """Obtiene el AuthHandler inicializado."""
    if _auth_handler is None:
        raise RuntimeError("AuthHandler not initialized. Call _init_dependencies first.")
    return _auth_handler


def _get_keys_handler() -> KeysHandler:
    """Obtiene el KeysHandler inicializado."""
    if _keys_handler is None:
        raise RuntimeError("KeysHandler not initialized. Call _init_dependencies first.")
    return _keys_handler


def _get_operations_handler() -> OperationsHandler:
    """Obtiene el OperationsHandler inicializado."""
    if _operations_handler is None:
        raise RuntimeError("OperationsHandler not initialized. Call _init_dependencies first.")
    return _operations_handler


def _get_consumption_handler() -> ConsumptionHandler:
    """Obtiene el ConsumptionHandler inicializado."""
    if _consumption_handler is None:
        raise RuntimeError("ConsumptionHandler not initialized. Call _init_dependencies first.")
    return _consumption_handler


def _get_packages_handler() -> PackagesHandler:
    """Obtiene el PackagesHandler inicializado."""
    if _packages_handler is None:
        raise RuntimeError("PackagesHandler not initialized. Call _init_dependencies first.")
    return _packages_handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    logger.info(f"User {user.id if user else 'unknown'} executed /start")
    
    auth_handler = _get_auth_handler()
    await auth_handler.start_handler(update, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    user = update.effective_user
    logger.info(f"User {user.id if user else 'unknown'} executed /help")
    
    handler = BasicHandler()
    await handler.help_handler(update, context)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    user = update.effective_user
    logger.info(f"User {user.id if user else 'unknown'} executed /status")
    if update.message:
        await update.message.reply_text("✅ Todos los sistemas operativos")


async def me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /me command - show user profile."""
    user = update.effective_user
    logger.info(f"User {user.id if user else 'unknown'} executed /me")
    
    auth_handler = _get_auth_handler()
    await auth_handler.me_handler(update, context)


async def unlink(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /unlink command - revoke bot access."""
    user = update.effective_user
    logger.info(f"User {user.id if user else 'unknown'} executed /unlink")
    
    auth_handler = _get_auth_handler()
    await auth_handler.unlink_handler(update, context)


def create_application(token: str) -> Application:
    """Create and configure the Telegram application."""
    logger.info("Initializing Telegram bot application...")

    # Initialize dependencies (Redis, API, handlers)
    asyncio.run(_init_dependencies())

    app = Application.builder().token(token).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("me", me))
    app.add_handler(CommandHandler("unlink", unlink))
    app.add_handler(CommandHandler("keys", lambda u, c: _get_keys_handler().show_keys_menu(u, c)))
    app.add_handler(CommandHandler("operaciones", lambda u, c: _get_operations_handler().operations_menu(u, c)))

    # Consumption billing commands
    app.add_handler(CommandHandler("consumo", lambda u, c: _get_consumption_handler().show_consumption_menu(u, c)))
    app.add_handler(CommandHandler("activar", lambda u, c: _get_consumption_handler().start_activation(u, c)))
    app.add_handler(CommandHandler("cancelar", lambda u, c: _get_consumption_handler().start_cancellation(u, c)))
    app.add_handler(CommandHandler("factura", lambda u, c: _get_consumption_handler().view_invoices(u, c)))

    # Data packages commands
    app.add_handler(CommandHandler("comprar", lambda u, c: _get_packages_handler().show_packages(u, c)))
    app.add_handler(CommandHandler("paquetes", lambda u, c: _get_packages_handler().show_packages(u, c)))
    app.add_handler(CommandHandler("packages", lambda u, c: _get_packages_handler().show_packages(u, c)))

    # Register callback handlers for keys management
    for handler in get_keys_callback_handlers(_api_client, _token_storage):
        app.add_handler(handler)

    # Register callback handlers for operations
    for handler in get_operations_callback_handlers(_api_client, _token_storage):
        app.add_handler(handler)

    # Register callback handlers for consumption billing
    for handler in get_consumption_callback_handlers(_api_client, _token_storage):
        app.add_handler(handler)

    # Register callback handlers for data packages
    for handler in get_packages_callback_handlers(_api_client, _token_storage):
        app.add_handler(handler)

    # Register payment handlers for data packages (Stars payments)
    for handler in get_packages_payment_handlers(_api_client, _token_storage):
        app.add_handler(handler)

    app.add_error_handler(error_handler)  # type: ignore[arg-type]

    logger.info("Bot handlers registered successfully")
    return app
