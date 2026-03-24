"""Handlers de autenticación invisible para el bot uSipipo."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from src.infrastructure.api_client import APIClient
from src.infrastructure.token_storage import TokenStorage
from src.bot.keyboards.auth import AuthMessages

logger = logging.getLogger(__name__)


class AuthHandler:
    """
    Handler para autenticación invisible.
    
    Gestiona el flujo de autenticación automática de usuarios,
    almacenamiento de tokens en Redis y auto-refresh silencioso.
    """
    
    def __init__(self, api_client: APIClient, token_storage: TokenStorage):
        self.api = api_client
        self.tokens = token_storage
    
    async def start_handler(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """
        Maneja /start - registro y autenticación automática.
        
        Si el usuario ya está autenticado, muestra mensaje de bienvenida.
        Si no, registra y autentica automáticamente.
        """
        if update.effective_user is None:
            logger.warning("start_handler called without effective_user")
            return
            
        telegram_id = update.effective_user.id
        
        # Check if already authenticated
        if await self.tokens.is_authenticated(telegram_id):
            if update.message:
                await update.message.reply_text(AuthMessages.WELCOME_RETURNING_USER)
            return
        
        # Register and auto-authenticate new user
        await self._register_and_auth(telegram_id, update, context)
    
    async def _register_and_auth(
        self,
        telegram_id: int,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """
        Registra y autentica usuario automáticamente.
        
        Llama al backend para crear usuario y obtener tokens.
        """
        try:
            # Backend genera código y lo envía por Telegram Bot API
            # Luego auto-verificamos con endpoint especial
            response = await self.api.post(
                "/auth/telegram/auto-register",
                {"telegram_id": telegram_id},
            )
            
            if "access_token" in response:
                await self.tokens.store(telegram_id, response)
                if update.message:
                    await update.message.reply_text(AuthMessages.WELCOME_NEW_USER)
            else:
                if update.message:
                    await update.message.reply_text(AuthMessages.AUTH_ERROR)
                
        except Exception as e:
            logger.error(f"Error en registro/auto-auth: {e}")
            if update.message:
                await update.message.reply_text(AuthMessages.AUTH_ERROR)
    
    async def me_handler(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """
        Maneja /me - muestra perfil del usuario.
        
        Verifica autenticación, hace auto-refresh si es necesario,
        y obtiene perfil del backend.
        """
        if update.effective_user is None:
            logger.warning("me_handler called without effective_user")
            return
            
        telegram_id = update.effective_user.id
        
        if not await self.tokens.is_authenticated(telegram_id):
            if update.message:
                await update.message.reply_text(AuthMessages.ME_NOT_AUTHENTICATED)
            return
        
        # Auto-refresh si es necesario
        if await self.tokens.needs_refresh(telegram_id):
            await self._refresh_tokens(telegram_id)
        
        try:
            tokens = await self.tokens.get(telegram_id)
            if tokens is None:
                if update.message:
                    await update.message.reply_text(AuthMessages.ME_ERROR)
                return
                
            response = await self.api.get("/users/me")
            
            username = update.effective_user.username or "N/A"
            message = AuthMessages.ME_AUTHENTICATED.format(
                user_id=response.get("id", "N/A")[:8],
                username=username,
                plan_name=response.get("plan", "Free"),
                keys_count=response.get("active_keys", 0),
                max_keys=response.get("max_keys", 2),
            )
            
            if update.message:
                await update.message.reply_text(message, parse_mode="HTML")
            
        except Exception as e:
            logger.error(f"Error al obtener perfil: {e}")
            if update.message:
                await update.message.reply_text(AuthMessages.ME_ERROR)
    
    async def unlink_handler(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """
        Maneja /unlink - revoca acceso del bot.
        
        Elimina tokens de Redis y (opcionalmente) revoca en backend.
        """
        if update.effective_user is None:
            logger.warning("unlink_handler called without effective_user")
            return
            
        telegram_id = update.effective_user.id
        
        if not await self.tokens.is_authenticated(telegram_id):
            if update.message:
                await update.message.reply_text(AuthMessages.UNLINK_NOT_AUTHENTICATED)
            return
        
        # Delete tokens from Redis
        await self.tokens.delete(telegram_id)
        
        # TODO: Revocar tokens en backend (endpoint /auth/logout)
        
        if update.message:
            await update.message.reply_text(AuthMessages.UNLINK_SUCCESS)
    
    async def _refresh_tokens(self, telegram_id: int) -> bool:
        """
        Auto-refresh de tokens silencioso.
        
        Usa refresh_token para obtener nuevos tokens sin intervención del usuario.
        
        Returns:
            bool: True si el refresh fue exitoso, False si falló
        """
        try:
            tokens = await self.tokens.get(telegram_id)
            if tokens is None:
                logger.warning(f"Cannot refresh: no tokens found for telegram_id={telegram_id}")
                return False
            
            response = await self.api.post(
                "/auth/refresh",
                {"refresh_token": tokens["refresh_token"]},
            )
            
            if "access_token" in response:
                await self.tokens.store(telegram_id, response)
                logger.info(f"Tokens refreshed for telegram_id={telegram_id}")
                return True
            
            logger.warning(f"Refresh failed for telegram_id={telegram_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error en refresh: {e}")
            return False
