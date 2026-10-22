"""Human-readable receipt strings for charges."""


def format_receipt(charge_id: str, card_last4: str, amount_cents: int) -> str:
    """Return a one-line receipt like "Charged $12.34 to card ending 4242 (ch_123)"."""
    dollars = amount_cents / 100
    return f"Charged ${dollars:.2f} to card ending {card_last4} ({charge_id})"
