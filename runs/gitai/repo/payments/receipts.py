"""Human-readable receipt formatting."""


def format_receipt(charge_id: str, card_last4: str, amount_cents: int) -> str:
    """Return a one-line receipt string for a charge."""
    dollars = amount_cents / 100
    return f"Charged ${dollars:,.2f} to card ending {card_last4} ({charge_id})"
