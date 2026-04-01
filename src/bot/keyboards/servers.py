"""Server selection inline keyboards."""

from typing import TYPE_CHECKING

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

if TYPE_CHECKING:
    from usipipo_commons.domain.entities.server import Server


class ServerKeyboards:
    """Factory for server selection inline keyboards."""

    LOAD_EMOJIS = {
        "low": "🟢",
        "medium": "🟡",
        "high": "🔴",
    }

    @staticmethod
    def server_selection(servers: list["Server"]) -> InlineKeyboardMarkup:
        """Create inline keyboard for server selection.

        Args:
            servers: List of servers sorted by load (lowest first)

        Returns:
            InlineKeyboardMarkup with server buttons
        """
        keyboard = []

        # Show top 5 recommended servers
        recommended = servers[:5]

        for server in recommended:
            # Calculate load percentage
            load_pct = int((server.current_connections / max(server.max_connections, 1)) * 100)

            # Determine load level and emoji
            if load_pct <= 50:
                load_level = "low"
            elif load_pct <= 80:
                load_level = "medium"
            else:
                load_level = "high"

            load_emoji = ServerKeyboards.LOAD_EMOJIS[load_level]

            # Button text: Flag + Country + City + Load
            city_text = f" - {server.city}" if server.city else ""
            button_text = f"{server.country_code}{city_text} {load_emoji}"

            # Callback data: server_select:{server_id}
            callback_data = f"server_select:{server.id}"

            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

        # Add "Show all servers" button if more than 5 servers
        if len(servers) > 5:
            keyboard.append([
                InlineKeyboardButton("🔍 Ver todos los servidores", callback_data="servers_show_all")
            ])

        # Add back button
        keyboard.append([
            InlineKeyboardButton("🔙 Volver", callback_data="vpn_keys_menu")
        ])

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def server_selection_full(servers: list["Server"]) -> InlineKeyboardMarkup:
        """Create inline keyboard showing all servers.

        Args:
            servers: List of all available servers

        Returns:
            InlineKeyboardMarkup with all server buttons
        """
        keyboard = []

        for server in servers:
            load_pct = int((server.current_connections / max(server.max_connections, 1)) * 100)

            if load_pct <= 50:
                load_level = "low"
            elif load_pct <= 80:
                load_level = "medium"
            else:
                load_level = "high"

            load_emoji = ServerKeyboards.LOAD_EMOJIS[load_level]

            city_text = f" - {server.city}" if server.city else ""
            button_text = f"{server.country_code}{city_text} {load_emoji}"

            callback_data = f"server_select:{server.id}"

            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

        # Add back button
        keyboard.append([
            InlineKeyboardButton("🔙 Volver", callback_data="vpn_keys_menu")
        ])

        return InlineKeyboardMarkup(keyboard)
