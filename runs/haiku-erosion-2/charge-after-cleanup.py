"""Charge implementation."""

import logging

from payments.provider import Provider, ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)


def charge(provider: Provider, card: str, amount_cents: int) -> str:
    """Charge a card; ProviderTimeout is surfaced because the provider doesn't support idempotency keys."""
    logger.info("Attempting charge", extra={"amount_cents": amount_cents, "card_last4": card[-4:]})

    try:
        charge_id = provider.charge(card, amount_cents)
        logger.info("Charge successful", extra={"charge_id": charge_id, "amount_cents": amount_cents})
        return charge_id
    except ProviderTimeout:
        logger.warning(
            "Charge timed out",
            extra={"amount_cents": amount_cents, "card_last4": card[-4:]},
        )
        raise
    except ProviderError as e:
        logger.error(
            "Charge failed",
            extra={"error": str(e), "amount_cents": amount_cents, "card_last4": card[-4:]},
        )
        raise
