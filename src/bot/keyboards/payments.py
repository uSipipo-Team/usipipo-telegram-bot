"""Teclados para gestión de pagos y suscripciones (Payments & Subscriptions)."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class PaymentsKeyboard:
    """Teclados para gestión de pagos y suscripciones."""

    @staticmethod
    def payment_menu(payment_methods: list) -> InlineKeyboardMarkup:
        """
        Teclado del menú principal de pagos.

        Args:
            payment_methods: Lista de métodos de pago disponibles

        Returns:
            InlineKeyboardMarkup: Teclado del menú de pagos
        """
        keyboard = []

        # Crypto payment button
        keyboard.append([
            InlineKeyboardButton(
                "🪙 Pagar con Criptomonedas (USDT)",
                callback_data="pay_crypto_10",
            ),
        ])

        # Stars payment button
        keyboard.append([
            InlineKeyboardButton(
                "⭐ Pagar con Telegram Stars",
                callback_data="pay_stars_600",
            ),
        ])

        # Payment history
        keyboard.append([
            InlineKeyboardButton(
                "📜 Ver Historial de Pagos",
                callback_data="payment_history_0",
            ),
        ])

        # Back to main menu
        keyboard.append([
            InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="main_menu"),
        ])

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def crypto_amounts() -> InlineKeyboardMarkup:
        """
        Teclado para seleccionar monto de pago crypto.

        Returns:
            InlineKeyboardMarkup: Teclado de montos
        """
        keyboard = [
            [
                InlineKeyboardButton("$5 USDT", callback_data="pay_crypto_5"),
                InlineKeyboardButton("$10 USDT", callback_data="pay_crypto_10"),
            ],
            [
                InlineKeyboardButton("$25 USDT", callback_data="pay_crypto_25"),
                InlineKeyboardButton("$50 USDT", callback_data="pay_crypto_50"),
            ],
            [
                InlineKeyboardButton("$100 USDT", callback_data="pay_crypto_100"),
            ],
            [
                InlineKeyboardButton("🔙 Volver", callback_data="payment_menu"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def stars_amounts() -> InlineKeyboardMarkup:
        """
        Teclado para seleccionar monto de pago con Stars.

        Returns:
            InlineKeyboardMarkup: Teclado de montos
        """
        keyboard = [
            [
                InlineKeyboardButton("⭐ 300 Stars", callback_data="pay_stars_300"),
                InlineKeyboardButton("⭐ 600 Stars", callback_data="pay_stars_600"),
            ],
            [
                InlineKeyboardButton("⭐ 1500 Stars", callback_data="pay_stars_1500"),
                InlineKeyboardButton("⭐ 3000 Stars", callback_data="pay_stars_3000"),
            ],
            [
                InlineKeyboardButton("⭐ 6000 Stars", callback_data="pay_stars_6000"),
            ],
            [
                InlineKeyboardButton("🔙 Volver", callback_data="payment_menu"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def crypto_payment_status(payment_id: str) -> InlineKeyboardMarkup:
        """
        Teclado para verificar estado de pago crypto.

        Args:
            payment_id: ID del pago

        Returns:
            InlineKeyboardMarkup: Teclado de verificación
        """
        keyboard = [
            [
                InlineKeyboardButton(
                    "🔄 Verificar Estado",
                    callback_data=f"check_crypto_status_{payment_id}",
                ),
            ],
            [
                InlineKeyboardButton("🔙 Volver a Pagos", callback_data="payment_menu"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def payment_history_list(has_next: bool = False, page: int = 0) -> InlineKeyboardMarkup:
        """
        Teclado para navegación del historial de pagos.

        Args:
            has_next: Si hay más páginas
            page: Página actual

        Returns:
            InlineKeyboardMarkup: Teclado de navegación
        """
        keyboard = []

        if has_next:
            keyboard.append([
                InlineKeyboardButton(
                    "📄 Página Siguiente",
                    callback_data=f"payment_history_{page + 1}",
                ),
            ])

        keyboard.append([
            InlineKeyboardButton("🔙 Volver a Pagos", callback_data="payment_menu"),
        ])

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def back_to_menu() -> InlineKeyboardMarkup:
        """
        Teclado para volver al menú de pagos.

        Returns:
            InlineKeyboardMarkup: Teclado de retorno
        """
        keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="payment_menu")]]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def back_to_payments() -> InlineKeyboardMarkup:
        """
        Teclado para volver a la lista de pagos.

        Returns:
            InlineKeyboardMarkup: Teclado de retorno
        """
        keyboard = [[InlineKeyboardButton("💳 Ver Pagos", callback_data="payment_menu")]]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def back_to_main_menu() -> InlineKeyboardMarkup:
        """
        Teclado para volver al menú principal.

        Returns:
            InlineKeyboardMarkup: Teclado de retorno principal
        """
        keyboard = [
            [InlineKeyboardButton("🔙 Volver al Menú Principal", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)
