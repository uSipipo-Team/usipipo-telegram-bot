"""Mensajes para gestión de claves VPN."""


class KeysMessages:
    """Mensajes para gestión de claves VPN."""

    # ============================================
    # MAIN MENU
    # ============================================

    MAIN_MENU = (
        "🔐 *Mis Claves VPN*\n\n"
        "📊 Resumen:\n"
        "🔑 Total: {total_keys}\n"
        "🌐 Outline: {outline_count}\n"
        "🔒 WireGuard: {wireguard_count}\n\n"
        "⚡ *Elige una opción:*"
    )

    NO_KEYS = "📭 *Sin claves*\n\n🔒 No tienes claves activas\n\n💡 Crea tu primera clave segura 🚀"

    # ============================================
    # KEYS LIST
    # ============================================

    KEYS_LIST_HEADER = "🔑 *Tus claves {type}*\n\n"

    NO_KEYS_TYPE = "📭 Sin claves {type}\n\n💡 Crea una nueva clave para comenzar."

    # ============================================
    # KEY DETAILS
    # ============================================

    KEY_DETAILS = (
        "💎 *{name}*\n\n"
        "📡 {type} • 🖥️ {server}\n"
        "━━━━━━━━━━━━━\n\n"
        "📊 Tu Consumo: {usage}/{limit}GB ({percentage}%)\n"
        "{usage_bar}\n\n"
        "{status_icon} Estado: *{status}*\n"
        "📅 Expira: {expires}\n"
        "🕐 Última vez: {last_seen}\n\n"
        "━━━━━━━━━━━━━\n"
        "🌐 Estado del Servidor\n"
        "{server_status_line}\n"
        "📈 {server_bandwidth} transferidos (total)\n"
        "⏱️ {server_uptime}\n"
        "━━━━━━━━━━━━━\n\n"
        "⚡ *Acciones:*"
    )

    # Server metrics constants
    SERVER_METRICS_ONLINE = "🟢 Online • {active_keys} claves activas"
    SERVER_METRICS_OFFLINE = "🔴 Offline • Sin conexión"
    SERVER_METRICS_UNAVAILABLE = "📡 Métricas no disponibles"
    SERVER_UPTIME_GOOD = "99%+ uptime (30 días)"
    SERVER_UPTIME_UNKNOWN = "Uptime desconocido"

    # WireGuard metrics constants
    WG_METRICS_CONNECTED = "🟢 Conectado • 📥 {rx} 📤 {tx}"
    WG_METRICS_DISCONNECTED = "🔴 Desconectado • 📥 {rx} 📤 {tx}"
    WG_METRICS_UNAVAILABLE = "📡 Métricas no disponibles"
    WG_LAST_HANDSHAKE = "🤝 Last handshake: {time}"
    WG_NO_HANDSHAKES = "🤝 Sin handshakes"

    KEY_NOT_FOUND = "❌ *Clave no encontrada*\n\nNo existe o no te pertenece a tu cuenta."

    # ============================================
    # STATISTICS
    # ============================================

    STATISTICS = (
        "📊 Mis Estadísticas\n\n"
        "🔐 Claves: {total_keys} (🟢 {active_keys} activas)\n\n"
        "📡 Datos: {total_usage}/{total_limit}GB "
        "({percentage}%)\n"
        "{usage_bar}\n\n"
        "🔌 Protocolos:\n"
        "🌐 Outline {outline_count} 💾 {outline_usage}GB\n"
        "🔒 WireGuard {wireguard_count} 💾 {wireguard_usage}GB\n\n"
        "💡 ¡Excelente! Uso menor al 80% 🎯"
    )

    # ============================================
    # ACTIONS
    # ============================================

    class Actions:
        """Mensajes de acciones."""

        KEY_SUSPENDED = (
            "⏸️ *Clave suspendida*\n\n"
            "🔒 Modo reposo activado\n\n"
            "🔄 Puedes reactivarla cuando quieras ⚡"
        )

        KEY_REACTIVATED = "✅ *Clave activada*\n\n🚀 Conexión lista\n\n🌐 ¡A navegar seguro! 🔥"

        KEY_DELETED = (
            "🗑️ *Clave eliminada*\n\n"
            "💥 Destruida permanentemente\n\n"
            "🔌 Dispositivos desconectados ⚡"
        )

        KEY_RENAMED = "✏️ *Renombrada*\n\n✨ {new_name}\n\n✅ Cambio guardado 🎯"

        KEY_CREATED = (
            "✅ *Clave creada*\n\n"
            "🔑 Nombre: {name}\n"
            "📡 Tipo: {type}\n"
            "💾 Límite: {limit}GB\n\n"
            "🚀 ¡Lista para usar!"
        )

    # ============================================
    # ERRORS
    # ============================================

    class Error:
        """Mensajes de error."""

        SYSTEM_ERROR = (
            "🚨 *Error del sistema*\n\n💥 Fallo temporal\n\n🔄 Intenta de nuevo en un momento 📡"
        )

        KEY_NOT_ACCESSIBLE = "🚫 *Acceso denegado*\n\n🔒 No tienes permisos para esta clave 🔐"

        OPERATION_FAILED = "❌ *Operación fallida*\n\n💥 No se pudo completar\n\n📟 {error}"

        INVALID_ACTION = "⛔ *Acción inválida*\n\n🚫 No disponible en este momento"

        QUOTA_EXCEEDED = (
            "⚠️ *Cuota excedida*\n\n"
            "💥 Has alcanzado tu límite\n\n"
            "💡 ⬆️ Mejora tu plan o compra slots extra ⚡"
        )

        MAX_KEYS_REACHED = (
            "⚠️ *Límite alcanzado*\n\n"
            "🔒 Has alcanzado el máximo de claves permitidas\n\n"
            "💡 Elimina una clave existente o mejora tu plan ⚡"
        )

    # ============================================
    # SUCCESS
    # ============================================

    class Success:
        """Mensajes de éxito."""

        OPERATION_COMPLETED = "✅ *Listo*\n\n⚡ Operación completada 🎯"

        CHANGES_SAVED = "💾 *Guardado*\n\n✨ Cambios actualizados"

    # ============================================
    # CREATE KEY
    # ============================================

    CREATE_KEY_PROMPT = (
        "➕ *Nueva Clave VPN*\n\n"
        "Elige el protocolo que deseas crear:\n\n"
        "🌐 *Outline* - Ideal para móviles, fácil configuración\n"
        "🔒 *WireGuard* - Máxima velocidad, soporte nativo\n\n"
        "Selecciona una opción:"
    )

    ENTER_KEY_NAME = (
        "✏️ *Nombre para tu clave*\n\n"
        "Escribe un nombre para identificar esta clave (ej: 'Casa', 'Móvil'):"
    )

    SELECT_DATA_LIMIT = "📊 *Límite de datos*\n\nElige el límite de datos para esta clave:"
