"""Handlers para gestión de claves VPN."""

import io
import logging
from typing import TYPE_CHECKING, Any

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.bot.keyboards.keys import KeysKeyboard
from src.bot.keyboards.messages_keys import KeysMessages
from src.infrastructure.api_client import APIClient
from src.infrastructure.token_storage import TokenStorage

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# Estados de la conversación para creación de claves
SELECT_PROTOCOL, INPUT_NAME = range(2)


class KeysHandler:
    """Handler para gestión de claves VPN."""

    def __init__(self, api_client: APIClient, token_storage: TokenStorage):
        self.api = api_client
        self.tokens = token_storage
        logger.info("🔑 KeysHandler initialized")

    async def start_creation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Inicia el flujo de creación preguntando el protocolo."""
        if not update.effective_user:
            return ConversationHandler.END

        telegram_id = update.effective_user.id
        logger.info(f"🔑 User {telegram_id} started key creation flow")

        try:
            # Check authentication
            if not await self.tokens.is_authenticated(telegram_id):
                if update.callback_query:
                    await update.callback_query.answer()
                    await update.callback_query.edit_message_text(
                        text="⚠️ No estás autenticado. Usa /start para iniciar sesión.",
                    )
                elif update.message:
                    await update.message.reply_text(
                        text="⚠️ No estás autenticado. Usa /start para iniciar sesión.",
                    )
                return ConversationHandler.END

            # Show protocol selection
            if update.callback_query:
                await update.callback_query.answer()
                await update.callback_query.edit_message_text(
                    text=KeysMessages.CREATE_KEY_PROMPT,
                    reply_markup=KeysKeyboard.protocol_selection(),
                    parse_mode="Markdown",
                )
            elif update.message:
                await update.message.reply_text(
                    text=KeysMessages.CREATE_KEY_PROMPT,
                    reply_markup=KeysKeyboard.protocol_selection(),
                    parse_mode="Markdown",
                )

            return SELECT_PROTOCOL

        except Exception as e:
            logger.error(f"Error starting key creation: {e}")
            if update.callback_query:
                await update.callback_query.edit_message_text(
                    text=KeysMessages.Error.SYSTEM_ERROR,
                )
            elif update.message:
                await update.message.reply_text(text=KeysMessages.Error.SYSTEM_ERROR)
            return ConversationHandler.END

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
            response = await self.api.get("/vpn/keys", headers=headers)

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
            response = await self.api.get("/vpn/keys", headers=headers)

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
            response = await self.api.get(f"/vpn/keys/{key_id}", headers=headers)

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

        logger.info(f"User {telegram_id} starting key creation flow")

        try:
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.CREATE_KEY_PROMPT,
                KeysKeyboard.protocol_selection(),
            )

        except Exception as e:
            logger.error(f"Error starting key creation: {e}")
            await self._safe_edit_message(
                query,
                context,
                KeysMessages.Error.SYSTEM_ERROR,
                KeysKeyboard.back_to_menu(),
            )

    async def protocol_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja selección de protocolo VPN."""
        query = update.callback_query
        if query is None or query.data is None:
            return ConversationHandler.END

        await query.answer()
        telegram_id = update.effective_user.id if update.effective_user else 0

        # Extract protocol from callback_data
        # Format: "vpn_create_outline" or "vpn_create_wireguard"
        protocol = query.data.replace("vpn_create_", "")

        logger.info(f"User {telegram_id} selected {protocol} protocol")

        try:
            # Store selected protocol
            context.user_data["vpn_protocol"] = protocol

            # Ask for key name
            await query.edit_message_text(
                text=KeysMessages.ENTER_KEY_NAME,
                parse_mode="Markdown",
            )

            return INPUT_NAME

        except Exception as e:
            logger.error(f"Error selecting protocol: {e}")
            await query.edit_message_text(text=KeysMessages.Error.SYSTEM_ERROR)
            return ConversationHandler.END

    async def name_received(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Finaliza la creación de la clave con el nombre proporcionado."""
        if not update.effective_user or not update.message or not update.message.text:
            return ConversationHandler.END

        key_name = update.message.text.strip()
        telegram_id = update.effective_user.id
        protocol = context.user_data.get("vpn_protocol")

        logger.info(f"User {telegram_id} naming {protocol} key: '{key_name}'")

        try:
            # Validate name (minimum 3 characters)
            if len(key_name) < 3:
                await update.message.reply_text(
                    text="❌ El nombre debe tener al menos 3 caracteres.\n\nPor favor, escribe un nombre válido:",
                    parse_mode="Markdown",
                )
                return INPUT_NAME  # Stay in INPUT_NAME state

            # Get auth headers
            tokens = await self.tokens.get(telegram_id)
            if not tokens:
                await update.message.reply_text(
                    text="❌ Error de autenticación. Por favor iniciá sesión con /start",
                )
                return ConversationHandler.END

            headers = {"Authorization": f"Bearer {tokens['access_token']}"}

            # Map protocol to KeyType enum
            vpn_type = "OUTLINE" if protocol.lower() == "outline" else "WIREGUARD"

            # Create key via API
            response = await self.api.post(
                "/vpn/keys",
                data={
                    "name": key_name,
                    "vpn_type": vpn_type,
                    "data_limit_gb": 5.0,  # Default 5GB
                },
                headers=headers,
            )

            # Clear protocol from user_data
            del context.user_data["vpn_protocol"]

            logger.info(f"✅ {vpn_type} key '{key_name}' created: {response.get('id')}")

            # Get key data from response
            key_id = response.get("id")
            key_config = response.get("config", "")
            data_limit = response.get("data_limit_gb", 5.0)

            # Send success message based on protocol
            if protocol.lower() == "outline":
                # Outline: Show access URL
                escaped_name = key_name.replace("_", r"\_").replace("*", r"\*")
                escaped_config = key_config.replace("_", r"\_").replace("*", r"\*")

                caption = (
                    f"✅ *Clave {vpn_type.title()} Creada*\n\n"
                    f"🔑 Nombre: *{escaped_name}*\n"
                    f"💾 Límite: *{data_limit}GB*\n\n"
                    f"Copia el siguiente código en tu aplicación Outline:\n\n"
                    f"```\n{escaped_config}\n```"
                )

                await update.message.reply_text(
                    text=caption,
                    parse_mode="Markdown",
                )

            elif protocol.lower() == "wireguard":
                # WireGuard: Send .conf file
                escaped_name = key_name.replace("_", r"\_").replace("*", r"\*")

                caption = (
                    f"✅ *Clave {vpn_type.title()} Creada*\n\n"
                    f"🔑 Nombre: *{escaped_name}*\n"
                    f"💾 Límite: *{data_limit}GB*\n\n"
                    f"Descargá el archivo .conf adjunto e importalo en WireGuard."
                )

                # Create .conf file
                conf_filename = f"{key_name}.conf"
                conf_content = key_config  # Backend returns full WireGuard config

                await update.message.reply_document(
                    document=io.BytesIO(conf_content.encode("utf-8")),
                    filename=conf_filename,
                    caption=caption,
                    parse_mode="Markdown",
                )

            logger.info(f"✅ Key delivered to user {telegram_id}")

        except Exception as e:
            logger.error(f"Error creating key: {e}")
            if update.message:
                await update.message.reply_text(
                    text=f"❌ Error al crear la clave: {str(e)}",
                    reply_markup=KeysKeyboard.back_to_menu(),
                )

        return ConversationHandler.END

    async def cancel_creation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancela la creación de la clave."""
        query = update.callback_query
        if query is None:
            return ConversationHandler.END

        await query.answer()
        telegram_id = update.effective_user.id if update.effective_user else 0

        logger.info(f"User {telegram_id} cancelled key creation")

        try:
            await query.edit_message_text(
                text="❌ Creación de clave cancelada.",
                reply_markup=KeysKeyboard.back_to_menu(),
            )
        except Exception as e:
            logger.error(f"Error cancelling creation: {e}")

        return ConversationHandler.END

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

    async def process_create_key_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesa el mensaje de texto con el nombre para nueva clave."""
        if context.user_data is None:
            return

        # Verificar que está en flujo de creación
        if not context.user_data.get("creating_key"):
            return

        if update.message is None or update.message.text is None:
            return

        key_name = update.message.text.strip()
        telegram_id = update.effective_user.id if update.effective_user else 0
        protocol = context.user_data.get("vpn_protocol")

        try:
            logger.info(f"User {telegram_id} creating {protocol} key with name '{key_name}'")

            # Validar nombre (mínimo 3 caracteres)
            if len(key_name) < 3:
                await update.message.reply_text(
                    text="❌ El nombre debe tener al menos 3 caracteres.\n\nPor favor, escribe un nombre válido:",
                    parse_mode="Markdown",
                )
                return

            # Clear creation state
            del context.user_data["creating_key"]
            del context.user_data["vpn_protocol"]

            # TODO: Create key via API
            # headers = await self._get_auth_headers(telegram_id)
            # response = await self.api.post(
            #     "/vpn/keys",
            #     headers=headers,
            #     json={"name": key_name, "protocol": protocol},
            # )

            # Mensaje temporal hasta implementar creación real
            message = (
                f"✅ *Clave {protocol.title()} Creada*\n\n"
                f"🔑 Nombre: *{key_name}*\n"
                f"📡 Protocolo: {protocol.title()}\n\n"
                f"La clave está siendo generada. Te notificaremos cuando esté lista."
            )

            await update.message.reply_text(
                text=message,
                reply_markup=KeysKeyboard.back_to_menu(),
                parse_mode="Markdown",
            )

            logger.info(f"User {telegram_id} created {protocol} key named '{key_name}'")

        except Exception as e:
            logger.error(f"Error creating key: {e}")
            if update.message:
                await update.message.reply_text(
                    text=KeysMessages.Error.SYSTEM_ERROR,
                    reply_markup=KeysKeyboard.back_to_menu(),
                    parse_mode="Markdown",
                )

    async def process_text_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Procesa input de texto y dirige al handler correcto.

        Verifica el estado en user_data y dirige a:
        - process_create_key_name() si está creando clave
        - process_rename_key() si está renombrando clave
        """
        if context.user_data is None:
            return

        # Check if creating new key
        if context.user_data.get("creating_key"):
            await self.process_create_key_name(update, context)
            return

        # Check if renaming key
        if context.user_data.get("rename_key_id"):
            await self.process_rename_key(update, context)
            return

        # No active operation, ignore message
        logger.debug(f"User {update.effective_user.id} sent text but no active operation")

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
            await self.api.put(
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
            await self.api.delete(f"/vpn/keys/{key_id}", headers=headers)

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
            response = await self.api.get(
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
            response = await self.api.get(
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
            response = await self.api.get("/vpn/keys", headers=headers)

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
                    wireguard_usage=f"{sum(k.get('data_used_gb', 0) for k in wireguard_keys):.1f}",
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
        get_key_creation_conversation_handler(handler),
    ]


def get_key_creation_conversation_handler(handler: KeysHandler) -> ConversationHandler:
    """
    Configuración del ConversationHandler para creación de claves VPN.

    Returns:
        ConversationHandler: Handler configurado para creación de claves
    """
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(handler.start_creation, pattern="^vpn_create_key$"),
            CommandHandler("newkey", handler.start_creation),
        ],
        states={
            SELECT_PROTOCOL: [
                CallbackQueryHandler(handler.protocol_selected, pattern="^vpn_create_"),
                CallbackQueryHandler(handler.cancel_creation, pattern="^cancel_create$"),
            ],
            INPUT_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler.name_received),
                CallbackQueryHandler(handler.cancel_creation, pattern="^cancel_create$"),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(handler.cancel_creation, pattern="^cancel_create$"),
        ],
        per_user=True,
        allow_reentry=True,
    )


def get_keys_callback_handlers(api_client: APIClient, token_storage: TokenStorage):
    """Retorna los handlers de callbacks para gestión de claves."""
    handler = KeysHandler(api_client, token_storage)

    return [
        CallbackQueryHandler(handler.show_keys_menu, pattern="^vpn_keys_menu$"),
        CallbackQueryHandler(handler.show_keys_by_type, pattern="^vpn_keys_"),
        CallbackQueryHandler(handler.show_key_details, pattern="^vpn_key_details_"),
        CallbackQueryHandler(handler.show_key_statistics, pattern="^vpn_key_stats$"),
        CallbackQueryHandler(handler.rename_key, pattern="^vpn_rename_"),
        CallbackQueryHandler(handler.delete_key, pattern="^vpn_delete_"),
        CallbackQueryHandler(handler.confirm_delete_key, pattern="^vpn_confirm_delete_"),
        CallbackQueryHandler(handler.cancel_delete, pattern="^vpn_cancel_delete$"),
        CallbackQueryHandler(handler.cancel_rename, pattern="^vpn_cancel_rename$"),
        CallbackQueryHandler(handler.download_wireguard_config, pattern="^vpn_download_wg_"),
        CallbackQueryHandler(handler.get_outline_link, pattern="^vpn_get_link_"),
    ]
