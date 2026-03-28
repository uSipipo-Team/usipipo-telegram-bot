"""Handlers for Referral system."""

import logging
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes

from src.bot.keyboards.messages_referrals import ReferralsMessages
from src.bot.keyboards.referrals import ReferralsKeyboard
from src.infrastructure.api_client import APIClient
from src.infrastructure.token_storage import TokenStorage

logger = logging.getLogger(__name__)


class ReferralsHandler:
    """Handler for referral system."""

    def __init__(self, api_client: APIClient, token_storage: TokenStorage):
        self.api = api_client
        self.tokens = token_storage
        logger.info("🎯 ReferralsHandler initialized")

    async def _get_auth_headers(self, telegram_id: int) -> dict[str, str]:
        """Get authentication headers for user."""
        tokens = await self.tokens.get(telegram_id)
        if not tokens:
            raise PermissionError("User not authenticated")
        return {"Authorization": f"Bearer {tokens['access_token']}"}

    async def _safe_answer_query(self, query: Any) -> None:
        """Answer callback query safely."""
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
        """Edit message safely."""
        try:
            await query.edit_message_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        except Exception as e:
            logger.error(f"Error editing message: {e}")
            # Fallback: send new message
            await query.message.reply_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )

    async def show_referrals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show referral stats and menu."""
        if update.effective_user is None:
            return

        telegram_id = update.effective_user.id
        logger.info(f"🎯 User {telegram_id} viewing referrals")

        try:
            # Check authentication
            if not await self.tokens.is_authenticated(telegram_id):
                if update.message:
                    await update.message.reply_text(
                        ReferralsMessages.Error.NOT_AUTHENTICATED,
                        parse_mode="Markdown",
                    )
                return

            # Get referral stats
            headers = await self._get_auth_headers(telegram_id)
            response = await self.api.api_client.get(
                "/referrals/me",
                headers=headers,
            )

            # Format message
            message = ReferralsMessages.Menu.REFERRAL_STATS.format(
                referral_code=response["referral_code"],
                total_referrals=response["total_referrals"],
                referral_credits=response["referral_credits"],
            )

            # Send with keyboard
            if update.message:
                await update.message.reply_text(
                    text=message,
                    reply_markup=ReferralsKeyboard.menu(),
                    parse_mode="Markdown",
                )

        except Exception as e:
            logger.error(f"Error showing referrals: {e}")
            if update.message:
                await update.message.reply_text(
                    ReferralsMessages.Error.SYSTEM_ERROR,
                    parse_mode="Markdown",
                )
