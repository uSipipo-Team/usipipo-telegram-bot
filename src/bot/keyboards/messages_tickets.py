"""Messages for Tickets feature."""


class TicketsMessages:
    """Messages for ticket system."""

    class Menu:
        """Menu messages."""

        TICKETS_LIST = (
            "🎫 *Tus Tickets*\n\n"
            "{tickets}\n\n"
            "Usa /nuevoticket para crear un nuevo ticket."
        )

        NO_TICKETS = (
            "📭 *No Tenés Tickets*\n\n"
            "No tenés tickets abiertos en este momento.\n\n"
            "Usa /nuevoticket para crear uno nuevo."
        )

        TICKET_DETAIL = (
            "🎫 *Ticket #{ticket_number}*\n\n"
            "📋 *Estado:* {status}\n"
            "📝 *Asunto:* {subject}\n"
            "📂 *Categoría:* {category}\n"
            "📅 *Creado:* {created_at}\n\n"
            "💬 *Último mensaje:* {last_message}"
        )

        TICKET_MESSAGES_LIST = (
            "💬 *Historial del Ticket #{ticket_number}*\n\n"
            "{messages}"
        )

        CREATE_TICKET = (
            "🎫 *Crear Nuevo Ticket*\n\n"
            "Por favor, seleccioná una categoría:\n\n"
            "• 🖥️ Técnico - Problemas con VPN, conexión\n"
            "• 💳 Pagos - Problemas con pagos, facturación\n"
            "• 📦 Servicios - Planes, paquetes de datos\n"
            "• ❓ General - Otras consultas"
        )

        TICKET_CREATED = (
            "✅ *Ticket Creado Exitosamente!*\n\n"
            "Número de ticket: *#{ticket_number}*\n"
            "Asunto: {subject}\n\n"
            "Te responderemos lo antes posible.\n"
            "Usa /tickets para ver el estado."
        )

        MESSAGE_SENT = (
            "✅ *Mensaje Enviado*\n\n"
            "Tu mensaje ha sido agregado al ticket #{ticket_number}.\n"
            "Te notificaremos cuando haya una respuesta."
        )

        TICKET_CLOSED = (
            "✅ *Ticket Cerrado*\n\n"
            "Tu ticket #{ticket_number} ha sido cerrado.\n"
            "Gracias por contactar soporte."
        )

    class Error:
        """Error messages."""

        NOT_FOUND = "❌ Ticket no encontrado."
        NOT_AUTHORIZED = "❌ No tenés permiso para ver este ticket."
        INVALID_CATEGORY = "❌ Categoría inválida."
        SUBJECT_TOO_SHORT = "❌ El asunto debe tener al menos 5 caracteres."
        MESSAGE_TOO_SHORT = "❌ El mensaje debe tener al menos 10 caracteres."
        SYSTEM_ERROR = "❌ Error del sistema. Por favor intenta de nuevo."
