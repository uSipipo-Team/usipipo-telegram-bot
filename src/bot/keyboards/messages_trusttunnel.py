"""Mensajes para gestión de TrustTunnel VPN."""


class TrustTunnelMessages:
    """Mensajes para gestión de TrustTunnel VPN."""

    # ============================================
    # KEY DETAILS
    # ============================================

    KEY_DETAILS = (
        "🛡️ *{name}*\n\n"
        "📡 TrustTunnel • 🖥️ {server}\n"
        "━━━━━━━━━━━━━\n\n"
        "📊 Tu Consumo: {usage}/{limit}GB ({percentage}%)\n"
        "{usage_bar}\n\n"
        "{status_icon} Estado: *{status}*\n"
        "📅 Expira: {expires}\n"
        "🕐 Última vez: {last_seen}\n\n"
        "━━━━━━━━━━━━━\n"
        "🛡️ TrustTunnel Server Status\n"
        "{server_status_line}\n"
        "📈 {total_bandwidth} transferidos (total)\n"
        "👥 {active_clients} clientes activos\n"
        "━━━━━━━━━━━━━\n\n"
        "⚡ *Acciones:*"
    )

    # ============================================
    # METRICS DISPLAY
    # ============================================

    METRICS_DISPLAY = (
        "🛡️ *TrustTunnel Metrics*\n\n"
        "👥 Clientes activos: {active_clients}\n"
        "📈 Total transferido: {total_bandwidth}\n\n"
        "{client_breakdown}"
    )

    METRICS_CLIENT_ROW = "  {rank}. {client_name} — {bandwidth}"
    METRICS_NO_CLIENTS = "  Sin datos de clientes"

    # ============================================
    # CONFIG EXPORT
    # ============================================

    CONFIG_EXPORT_SUCCESS = "📥 *Configuración lista*\n\n📄 Archivo TOML generado\n\n⬇️ Descargalo abajo:"
    CONFIG_EXPORT_CAPTION = "🛡️ TrustTunnel config — {key_name}"

    # ============================================
    # SERVER STATUS
    # ============================================

    SERVER_ONLINE = "🟢 Online • {active_clients} clientes activos"
    SERVER_OFFLINE = "🔴 Offline • Sin conexión"
    SERVER_METRICS_UNAVAILABLE = "📡 Métricas no disponibles"

    # ============================================
    # CREATE KEY
    # ============================================

    KEY_CREATED = (
        "✅ *Clave TrustTunnel creada*\n\n"
        "🔑 Nombre: {name}\n"
        "🛡️ Tipo: TrustTunnel\n"
        "💾 Límite: {limit}GB\n\n"
        "🚀 ¡Lista para usar! Descargá la configuración ⬇️"
    )

    # ============================================
    # ERRORS
    # ============================================

    class Error:
        """Mensajes de error."""

        SERVICE_UNAVAILABLE = (
            "🔴 *Servicio no disponible*\n\n"
            "💥 TrustTunnel no responde en el servidor\n\n"
            "🔄 Intenta de nuevo en unos minutos 📡"
        )

        CONFIG_EXPORT_FAILED = (
            "❌ *Error al generar config*\n\n"
            "💥 No se pudo crear el archivo TOML\n\n"
            "🔄 Intenta de nuevo 📡"
        )

        NO_SERVERS = (
            "⚠️ *Sin servidores*\n\n"
            "🛡️ No hay servidores TrustTunnel disponibles\n\n"
            "💡 Probá otro protocolo ⚡"
        )

        KEY_NOT_FOUND = (
            "❌ *Clave no encontrada*\n\n"
            "🔒 No existe o no te pertenece 🔐"
        )
