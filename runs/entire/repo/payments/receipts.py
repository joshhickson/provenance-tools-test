"""Human-readable receipt formatting."""


def format_receipt(charge_id: str, card_last4: str, amount_cents: int) -> str:
    """Return a one-line receipt, e.g. "Charged $12.34 to card ending 4242 (ch_123)"."""
    dollars, cents = divmod(amount_cents, 100)
    return f"Charged ${dollars}.{cents:02d} to card ending {card_last4} ({charge_id})"
