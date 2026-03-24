"""Mensajes de autenticación para el bot uSipipo."""


class AuthMessages:
    """Mensajes para autenticación invisible."""
    
    # /start command
    WELCOME_NEW_USER = (
        "✅ ¡Bienvenido a uSipipo!\n\n"
        "Tu cuenta ha sido creada y estás autenticado.\n\n"
        "Usa /help para ver los comandos disponibles."
    )
    
    WELCOME_RETURNING_USER = (
        "👋 ¡Bienvenido de nuevo!\n\n"
        "Ya tienes una cuenta activa.\n\n"
        "Usa /help para ver los comandos disponibles."
    )
    
    # Auth errors
    AUTH_ERROR = (
        "❌ Error de autenticación.\n\n"
        "Intenta de nuevo en unos minutos."
    )
    
    # /unlink command
    UNLINK_CONFIRMATION = (
        "⚠️ ¿Estás seguro de que quieres desvincular tu cuenta?\n\n"
        "Esto cerrará todas tus sesiones y tendrás que volver a autenticarte.\n\n"
        "Escribe /confirm_unlink para confirmar."
    )
    
    UNLINK_SUCCESS = "✅ Tu cuenta ha sido desvinculada correctamente."
    
    UNLINK_NOT_AUTHENTICATED = "ℹ️ No tenías sesión iniciada."
    
    # /me command
    ME_AUTHENTICATED = (
        "👤 <b>Tu Perfil</b>\n\n"
        "ID: {user_id}\n"
        "Telegram: @{username}\n"
        "Plan: {plan_name}\n"
        "Keys activas: {keys_count}/{max_keys}"
    )
    
    ME_NOT_AUTHENTICATED = (
        "🔒 No autenticado\n\n"
        "Usa /start para iniciar sesión."
    )
    
    ME_ERROR = (
        "❌ Error al obtener perfil.\n\n"
        "Intenta de nuevo."
    )
