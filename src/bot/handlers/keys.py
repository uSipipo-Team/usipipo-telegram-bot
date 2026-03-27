"""Handlers para gestión de claves VPN."""

import io
import logging
from typing import TYPE_CHECKING, Any

from telegram import Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

from src.bot.keyboards.keys import KeysKeyboard
from src.bot.keyboards.messages_keys import KeysMessages
from src.infrastructure.api_client import APIClient
from src.infrastructure.token_storage import TokenStorage

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class KeysHandler:
    """Handler para gestión de claves VPN."""

    def __init__(self, api_client: APIClient, token_storage: TokenStorage):
        self.api = api_client
        self.tokens = token_storage
        logger.info("KeysHandler initialized")

    async def _get_auth_headers(self, telegram_id: int) -> dict[str, str]:
        """Obtiene headers de autenticación para el usuario."""
        tokens = await self.tokens.get(telegram_id)
        if not tokens:
            raise PermissionError("User not authenticated")
        return {"Authorization": f"Bearer {tokens['access_token']}"}

    async def _safe_answer_query(self, query: Any) -> None:
        """Responde a callback query de forma segura."""
        try:
            await query.answer()
        except Exception as e:
            logger.error(f"Error answering query: {e}")

    async def _safe_edit_message(
        self,
        query: Any,
        context: ContextTypes.DEFAULT_TYPE,
        text: str,
        reply_markup: Any = None,
        parse_mode: str = "Markdown",
    ) -> None:
        """Edita mensaje de forma segura."""
        try:
            await query.edit_message_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        except Exception as e:
            logger.error(f"Error editing message: {e}")

    async def show_keys_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Muestra el menú principal de gestión de claves."""
        if update.effective_user is None:
            return

        telegram_id = update.effective_user.id
        logger.info(f"User {telegram_id} viewing keys menu")

        try:
            # Check authentication
            if not await self.tokens.is_authenticated(telegram_id):
                if update.message:
                    await update.message.reply_text(
                        KeysMessages.Error.KEY_NOT_ACCESSIBLE,
                        parse_mode="Markdown",
                    )
                return

            # Get user keys
            headers = await self._get_auth_headers(telegram_id)
            response = await self.api.api_client.get("/vpn/keys", headers=headers)

            keys = response if isinstance(response, list) else []

            # Count by type
            total_keys = len(keys)
            outline_count = len([k for k in keys if k.get("key_type", "").lower() == "outline"])
            wireguard_count = len(
                [k for k in keys if k.get("key_type", "").lower() == "wireguard"]
            )

            if total_keys == 0:
                message = KeysMessages.NO_KEYS
            else:
                message = KeysMessages.MAIN_MENU.format(
                    total_keys=total_keys,
                    outline_count=outline_count,
                    wireguard_count=wireguard_count,
                )

            keyboard = KeysKeyboard.main_menu(total_keys, outline_count, wireguard_count)

            if update.callback_query:
                await self._safe_edit_message(
                    update.callback_query, context, message, keyboard
                )
            elif update.message:
                await update.message.reply_text(message, reply_markup=keyboard, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Error showing keys menu: {e}")
            if update.callback_query:
                await self._safe_edit_message(
                    update.callback_query,
                    context,
                    KeysMessages.Error.SYSTEM_ERROR,
                    KeysKeyboard.back_to_menu(),
                )
            elif update.message:
                await update.message.reply_text(
                    KeysMessages.Error.SYSTEM_ERROR,
                    reply_markup=KeysKeyboard.back_to_menu(),
                    parse_mode="Markdown",
                )

    async def show_keys_by_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Muestra claves filtradas por tipo."""
        query = update.callback_query
        if query is None or query.data is None:
            return

        await self._safe_answer_query(query)

        # Extract type from callback_data
        key_type = query.data.replace("vpn_keys_", "")
        telegram_id = update.effective_user.id if update.effective_user else 0

        logger.info(f"User {telegram_id} viewing keys by type: {key_type}")

        try:
            headers = await self._get_auth_headers(telegram_id)
            response = await self.api.api_client.get("/vpn/keys", headers=headers)

            keys = response if isinstance(response, list) else []
            filtered_keys = [k for k in keys if k.get("key_type", "").lower() == key_type.lower()]

            if not filtered_keys:
                message = KeysMessages.NO_KEYS_TYPE.format(type=key_type.upper())
                keyboard = KeysKeyboard.back_to_menu()
            else:
                message = KeysMessages.KEYS_LIST_HEADER.format(type=key_type.upper())
                keyboard = KeysKeyboard.keys_list(filtered_keys, key_type)

                # Add key info
                for key in filtered_keys:
                    status = "🟢 Activa" if key.get("status", "active") == "active" else "🔴 Inactiva"
                    message += (
                        f"\n🔑 {key.get('name', 'Unknown')}\n"
                        f"   📊 {key.get('data_used_gb', 0):.2f}/{key.get('data_limit_gb', 0):.2f} GB\n"
                        f"   {status}\n"
                    )

            await self._safe_edit_message(query, context, message, keyboard)

        except Exception as e:
            logger.error(f"Error showing keys by type: {e}")
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.Error.SYSTEM_ERROR,
                KeysKeyboard.back_to_menu(),
            )

    async def show_key_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Muestra detalles de una clave específica."""
        query = update.callback_query
        if query is None or query.data is None:
            return

        await self._safe_answer_query(query)

        # Extract key_id from callback_data
        key_id = query.data.split("_")[-1]
        telegram_id = update.effective_user.id if update.effective_user else 0

        logger.info(f"User {telegram_id} viewing details for key {key_id}")

        try:
            headers = await self._get_auth_headers(telegram_id)
            response = await self.api.api_client.get(f"/vpn/keys/{key_id}", headers=headers)

            key = response
            status = "Activa" if key.get("status", "active") == "active" else "Inactiva"
            status_icon = "🟢" if key.get("status", "active") == "active" else "🔴"

            usage_percentage = (
                (key.get("data_used_gb", 0) / key.get("data_limit_gb", 1)) * 100
                if key.get("data_limit_gb", 0) > 0
                else 0
            )

            # Generate progress bar
            usage_bar = self._generate_progress_bar(usage_percentage)

            message = KeysMessages.KEY_DETAILS.format(
                name=key.get("name", "Unknown"),
                type=key.get("key_type", "UNKNOWN").upper(),
                server=key.get("server", "N/A"),
                usage_bar=usage_bar,
                usage=f"{key.get('data_used_gb', 0):.1f}",
                limit=f"{key.get('data_limit_gb', 0):.1f}",
                percentage=f"{usage_percentage:.0f}",
                status=status,
                status_icon=status_icon,
                expires=key.get("expires_at", "N/A")[:10] if key.get("expires_at") else "N/A",
            )

            keyboard = KeysKeyboard.key_actions(
                key_id,
                key.get("status", "active") == "active",
                key.get("key_type", "wireguard"),
            )

            await self._safe_edit_message(query, context, message, keyboard)

        except Exception as e:
            logger.error(f"Error showing key details: {e}")
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.Error.SYSTEM_ERROR,
                KeysKeyboard.back_to_menu(),
            )

    async def create_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Inicia el flujo de creación de nueva clave."""
        query = update.callback_query
        if query is None:
            return

        await self._safe_answer_query(query)
        telegram_id = update.effective_user.id if update.effective_user else 0

        logger.info(f"User {telegram_id} creating new key")

        try:
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.CREATE_KEY_PROMPT,
                None,
            )

            # Store state for next step
            if context.user_data is not None:
                context.user_data["creating_key"] = True

        except Exception as e:
            logger.error(f"Error starting key creation: {e}")
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.Error.SYSTEM_ERROR,
                KeysKeyboard.back_to_menu(),
            )

    async def rename_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Inicia el flujo de renombrado de clave."""
        query = update.callback_query
        if query is None or query.data is None:
            return

        await self._safe_answer_query(query)

        key_id = query.data.split("_")[-1]
        telegram_id = update.effective_user.id if update.effective_user else 0

        logger.info(f"User {telegram_id} renaming key {key_id}")

        try:
            # Store state for next step
            if context.user_data is not None:
                context.user_data["rename_key_id"] = key_id

            message = "✏️ *Renombrar Clave*\n\n" "Por favor, escribe el nuevo nombre para tu clave:"

            await self._safe_edit_message(
                query,
                context,
                message,
                KeysKeyboard.cancel_rename(),
            )

        except Exception as e:
            logger.error(f"Error starting rename: {e}")
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.Error.SYSTEM_ERROR,
                KeysKeyboard.back_to_menu(),
            )

    async def process_rename_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesa el mensaje de texto con el nuevo nombre para la clave."""
        if context.user_data is None:
            return

        key_id = context.user_data.get("rename_key_id")
        if not key_id:
            return

        if update.message is None or update.message.text is None:
            return

        new_name = update.message.text.strip()
        telegram_id = update.effective_user.id if update.effective_user else 0

        try:
            logger.info(f"User {telegram_id} renaming key {key_id} to '{new_name}'")

            # Clear state
            del context.user_data["rename_key_id"]

            # Update key
            headers = await self._get_auth_headers(telegram_id)
            await self.api.api_client.put(
                f"/vpn/keys/{key_id}",
                headers=headers,
                json={"name": new_name},
            )

            message = KeysMessages.Actions.KEY_RENAMED.format(new_name=new_name)

            await update.message.reply_text(
                text=message,
                reply_markup=KeysKeyboard.back_to_menu(),
                parse_mode="Markdown",
            )

            logger.info(f"User {telegram_id} renamed key {key_id} to '{new_name}'")

        except Exception as e:
            logger.error(f"Error renaming key: {e}")
            if update.message:
                await update.message.reply_text(
                    text=KeysMessages.Error.SYSTEM_ERROR,
                    reply_markup=KeysKeyboard.back_to_menu(),
                    parse_mode="Markdown",
                )

    async def cancel_rename(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancela el proceso de renombrado."""
        query = update.callback_query
        if query is None:
            return

        await self._safe_answer_query(query)

        if context.user_data is not None and "rename_key_id" in context.user_data:
            del context.user_data["rename_key_id"]

        await self.show_keys_menu(update, context)

    async def delete_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Inicia el flujo de eliminación de clave."""
        query = update.callback_query
        if query is None or query.data is None:
            return

        await self._safe_answer_query(query)

        key_id = query.data.split("_")[-1]
        telegram_id = update.effective_user.id if update.effective_user else 0

        logger.warning(f"User {telegram_id} deleting key {key_id}")

        try:
            message = "⚠️ *¿Eliminar clave?*\n\n" "Esta acción no se puede deshacer."

            await self._safe_edit_message(
                query,
                context,
                message,
                KeysKeyboard.confirm_delete(key_id),
            )

        except Exception as e:
            logger.error(f"Error starting delete: {e}")
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.Error.SYSTEM_ERROR,
                KeysKeyboard.back_to_menu(),
            )

    async def confirm_delete_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Confirma y ejecuta la eliminación de clave."""
        query = update.callback_query
        if query is None or query.data is None:
            return

        await self._safe_answer_query(query)

        key_id = query.data.split("_")[-1]
        telegram_id = update.effective_user.id if update.effective_user else 0

        logger.warning(f"User {telegram_id} confirming delete key {key_id}")

        try:
            # Delete key
            headers = await self._get_auth_headers(telegram_id)
            await self.api.api_client.delete(f"/vpn/keys/{key_id}", headers=headers)

            message = KeysMessages.Actions.KEY_DELETED

            await self._safe_edit_message(
                query,
                context,
                message,
                KeysKeyboard.back_to_menu(),
            )

            logger.info(f"User {telegram_id} successfully deleted key {key_id}")

        except Exception as e:
            logger.error(f"Error deleting key: {e}")
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.Error.OPERATION_FAILED.format(error=str(e)),
                KeysKeyboard.back_to_menu(),
            )

    async def cancel_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancela el proceso de eliminación."""
        query = update.callback_query
        if query is None:
            return

        await self._safe_answer_query(query)
        await self.show_keys_menu(update, context)

    async def download_wireguard_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Envía el archivo .conf de una clave WireGuard."""
        query = update.callback_query
        if query is None or query.data is None:
            return

        await self._safe_answer_query(query)

        key_id = query.data.split("_")[-1]
        telegram_id = update.effective_user.id if update.effective_user else 0

        logger.info(f"User {telegram_id} downloading WireGuard config for key {key_id}")

        try:
            headers = await self._get_auth_headers(telegram_id)
            response = await self.api.api_client.get(
                f"/vpn/keys/{key_id}/config", headers=headers
            )

            config_str = response.get("config_string", "")
            key_name = response.get("external_id", "wg_config")

            if not config_str:
                await self._safe_edit_message(
                    query,
                    context,
                    "❌ La configuración no está disponible.",
                    KeysKeyboard.back_to_menu(),
                )
                return

            bio = io.BytesIO(config_str.encode("utf-8"))
            bio.name = f"{key_name}.conf"

            if update.effective_chat:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=bio,
                    filename=f"{key_name}.conf",
                    caption=(
                        f"📄 Configuración WireGuard: *{key_name}*\n\n"
                        "Importa este archivo en tu aplicación WireGuard."
                    ),
                    parse_mode="Markdown",
                )

            logger.info(f"User {telegram_id} downloaded WireGuard config for key {key_id}")

        except Exception as e:
            logger.error(f"Error downloading config: {e}")
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.Error.SYSTEM_ERROR,
                KeysKeyboard.back_to_menu(),
            )

    async def get_outline_link(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Muestra el enlace de acceso ss:// para una clave Outline."""
        query = update.callback_query
        if query is None or query.data is None:
            return

        await self._safe_answer_query(query)

        key_id = query.data.split("_")[-1]
        telegram_id = update.effective_user.id if update.effective_user else 0

        logger.info(f"User {telegram_id} getting Outline link for key {key_id}")

        try:
            headers = await self._get_auth_headers(telegram_id)
            response = await self.api.api_client.get(
                f"/vpn/keys/{key_id}/config", headers=headers
            )

            access_url = response.get("access_url", "")

            if not access_url:
                await self._safe_edit_message(
                    query,
                    context,
                    "❌ El enlace no está disponible.",
                    KeysKeyboard.back_to_menu(),
                )
                return

            message = (
                f"🔗 **Tu Clave de Acceso Outline**\n\n"
                f"Copia el siguiente código y pégalo en tu aplicación Outline:\n\n"
                f"`{access_url}`"
            )

            await self._safe_edit_message(
                query,
                context,
                message,
                KeysKeyboard.back_to_menu(),
            )

            logger.info(f"User {telegram_id} retrieved Outline link for key {key_id}")

        except Exception as e:
            logger.error(f"Error getting Outline link: {e}")
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.Error.SYSTEM_ERROR,
                KeysKeyboard.back_to_menu(),
            )

    async def show_key_statistics(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Muestra estadísticas detalladas de las claves."""
        query = update.callback_query
        if query is None:
            return

        await self._safe_answer_query(query)

        telegram_id = update.effective_user.id if update.effective_user else 0

        logger.info(f"User {telegram_id} viewing key statistics")

        try:
            headers = await self._get_auth_headers(telegram_id)
            response = await self.api.api_client.get("/vpn/keys", headers=headers)

            keys = response if isinstance(response, list) else []

            if not keys:
                message = KeysMessages.NO_KEYS
                keyboard = KeysKeyboard.back_to_menu()
            else:
                total_keys = len(keys)
                active_keys = len([k for k in keys if k.get("status", "active") == "active"])
                total_usage = sum(k.get("data_used_gb", 0) for k in keys)
                total_limit = sum(k.get("data_limit_gb", 0) for k in keys)
                overall_percentage = (total_usage / total_limit * 100) if total_limit > 0 else 0

                outline_keys = [k for k in keys if k.get("key_type", "").lower() == "outline"]
                wireguard_keys = [
                    k for k in keys if k.get("key_type", "").lower() == "wireguard"
                ]

                usage_bar = self._generate_progress_bar(overall_percentage)

                message = KeysMessages.STATISTICS.format(
                    total_keys=str(total_keys),
                    active_keys=str(active_keys),
                    total_usage=f"{total_usage:.1f}",
                    total_limit=f"{total_limit:.1f}",
                    percentage=f"{overall_percentage:.0f}",
                    usage_bar=usage_bar,
                    outline_count=str(len(outline_keys)),
                    wireguard_count=str(len(wireguard_keys)),
                    outline_usage=f"{sum(k.get('data_used_gb', 0) for k in outline_keys):.1f}",
                    wireguard_usage=f"{
                        sum(k.get('data_used_gb', 0) for k in wireguard_keys):.1f}",
                )

                keyboard = KeysKeyboard.back_to_menu()

            await self._safe_edit_message(query, context, message, keyboard)

        except Exception as e:
            logger.error(f"Error showing statistics: {e}")
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.Error.SYSTEM_ERROR,
                KeysKeyboard.back_to_menu(),
            )

    def _generate_progress_bar(self, percentage: float, width: int = 10) -> str:
        """Genera una barra de progreso."""
        filled = int((percentage / 100) * width)
        empty = width - filled

        filled_char = "█"
        empty_char = "░"

        return filled_char * filled + empty_char * empty


def get_keys_handlers(api_client: APIClient, token_storage: TokenStorage):
    """Retorna los handlers de gestión de claves."""
    handler = KeysHandler(api_client, token_storage)

    return [
        CommandHandler("keys", handler.show_keys_menu),
        CommandHandler("newkey", handler.create_key),
        MessageHandler(filters.TEXT & ~filters.COMMAND, handler.process_rename_key),
    ]


def get_keys_callback_handlers(api_client: APIClient, token_storage: TokenStorage):
    """Retorna los handlers de callbacks para gestión de claves."""
    handler = KeysHandler(api_client, token_storage)

    return [
        CallbackQueryHandler(handler.show_keys_menu, pattern="^vpn_keys_menu$"),
        CallbackQueryHandler(handler.show_keys_by_type, pattern="^vpn_keys_"),
        CallbackQueryHandler(handler.show_key_details, pattern="^vpn_key_details_"),
        CallbackQueryHandler(handler.show_key_statistics, pattern="^vpn_key_stats$"),
        CallbackQueryHandler(handler.create_key, pattern="^vpn_create_key$"),
        CallbackQueryHandler(handler.rename_key, pattern="^vpn_rename_"),
        CallbackQueryHandler(handler.delete_key, pattern="^vpn_delete_"),
        CallbackQueryHandler(handler.confirm_delete_key, pattern="^vpn_confirm_delete_"),
        CallbackQueryHandler(handler.cancel_delete, pattern="^vpn_cancel_delete$"),
        CallbackQueryHandler(handler.cancel_rename, pattern="^vpn_cancel_rename$"),
        CallbackQueryHandler(handler.download_wireguard_config, pattern="^vpn_download_wg_"),
        CallbackQueryHandler(handler.get_outline_link, pattern="^vpn_get_link_"),
    ]
