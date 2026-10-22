"""Format receipt strings for charges."""


def format_receipt(charge_id: str, card_last4: str, amount_cents: int) -> str:
    """Format a receipt string for a charge."""
    amount_dollars = amount_cents / 100
    return f"Charged ${amount_dollars:.2f} to card ending {card_last4} ({charge_id})"
