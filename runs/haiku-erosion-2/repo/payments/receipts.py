"""Receipt formatting."""


def format_receipt(charge_id: str, card_last4: str, amount_cents: int) -> str:
    """Format a charge receipt as a one-line string."""
    dollars = amount_cents // 100
    cents = amount_cents % 100
    amount_str = f"${dollars}.{cents:02d}"
    return f"Charged {amount_str} to card ending {card_last4} ({charge_id})"
