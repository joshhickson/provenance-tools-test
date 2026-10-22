"""Format receipts for completed charges."""


def format_receipt(charge_id: str, card_last4: str, amount_cents: int) -> str:
    """Return a one-line receipt string for a charge."""
    dollars = amount_cents // 100
    cents = amount_cents % 100
    return f"Charged ${dollars}.{cents:02d} to card ending {card_last4} ({charge_id})"
