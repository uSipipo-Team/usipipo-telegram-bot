"""Almacenamiento de tokens en Redis para el bot uSipipo."""

import time
from typing import Optional, Dict, Any

from src.infrastructure.redis import RedisPool
from src.infrastructure.config import settings


class TokenStorage:
    """
    Gestión de tokens de autenticación en Redis.
    
    Almacena tokens JWT de usuarios con expiración automática.
    Los tokens se guardan con un prefijo único y tiempo de vida
    configurado (30 días para refresh token).
    """
    
    TOKEN_PREFIX = "usipipo:bot:tokens:"
    ACCESS_TOKEN_EXPIRY = 30 * 60  # 30 minutos
    REFRESH_TOKEN_EXPIRY = 30 * 24 * 60 * 60  # 30 días
    
    async def _get_redis(self) -> Any:
        """Obtiene cliente Redis del pool."""
        return await RedisPool.get_client()
    
    async def store(
        self,
        telegram_id: int,
        tokens: Dict[str, Any],
    ) -> None:
        """
        Guarda tokens en Redis con expiración automática.
        
        Args:
            telegram_id: ID de Telegram del usuario
            tokens: Diccionario con access_token, refresh_token, user_id, expires_in
        """
        key = f"{self.TOKEN_PREFIX}{telegram_id}"
        redis_client = await self._get_redis()
        
        async with redis_client.pipeline() as pipe:
            await pipe.hset(key, mapping={
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "user_id": tokens["user_id"],
                "expires_at": str(int(time.time()) + tokens["expires_in"]),
                "created_at": str(int(time.time())),
            })
            await pipe.expire(key, self.REFRESH_TOKEN_EXPIRY)
            await pipe.execute()
    
    async def get(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """
        Recupera tokens del usuario.
        
        Args:
            telegram_id: ID de Telegram del usuario
            
        Returns:
            Optional[Dict]: Tokens del usuario o None si no existe
        """
        key = f"{self.TOKEN_PREFIX}{telegram_id}"
        redis_client = await self._get_redis()
        data = await redis_client.hgetall(key)
        
        if not data:
            return None
        
        return {
            "access_token": data["access_token"],
            "refresh_token": data["refresh_token"],
            "user_id": data["user_id"],
            "expires_at": int(data["expires_at"]),
            "created_at": int(data["created_at"]),
        }
    
    async def delete(self, telegram_id: int) -> bool:
        """
        Elimina tokens del usuario (logout/unlink).
        
        Args:
            telegram_id: ID de Telegram del usuario
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        key = f"{self.TOKEN_PREFIX}{telegram_id}"
        redis_client = await self._get_redis()
        return await redis_client.delete(key) > 0
    
    async def is_authenticated(self, telegram_id: int) -> bool:
        """
        Verifica si el usuario tiene tokens válidos.
        
        Args:
            telegram_id: ID de Telegram del usuario
            
        Returns:
            bool: True si tiene tokens válidos, False si no
        """
        tokens = await self.get(telegram_id)
        
        if not tokens:
            return False
        
        # Check if access token expired
        if time.time() > tokens["expires_at"]:
            return False
        
        return True
    
    async def needs_refresh(self, telegram_id: int) -> bool:
        """
        Verifica si el token necesita refresh (5 min antes de expirar).
        
        Args:
            telegram_id: ID de Telegram del usuario
            
        Returns:
            bool: True si necesita refresh, False si no
        """
        tokens = await self.get(telegram_id)
        
        if not tokens:
            return False
        
        threshold = settings.TOKEN_REFRESH_THRESHOLD_SECONDS
        return time.time() > (tokens["expires_at"] - threshold)
