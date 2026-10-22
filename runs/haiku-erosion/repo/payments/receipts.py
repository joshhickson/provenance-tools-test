def format_receipt(charge_id: str, card_last4: str, amount_cents: int) -> str:
    """Format a charge receipt as a one-line string."""
    dollars = amount_cents / 100
    return f"Charged ${dollars:.2f} to card ending {card_last4} ({charge_id})"
