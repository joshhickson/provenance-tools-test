"""Format payment receipts."""


def format_receipt(charge_id: str, card_last4: str, amount_cents: int) -> str:
    """Format a charge receipt as a single-line string."""
    amount_dollars = amount_cents / 100.0
    return f"Charged ${amount_dollars:.2f} to card ending {card_last4} ({charge_id})"
