"""Charge a card using a payment provider."""

import logging

from payments.provider import Provider, ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)


def charge(provider: Provider, card: str, amount_cents: int) -> str:
    """Charge a card using the provider and return the charge id."""
    logger.info("charge_started", extra={"card": card, "amount_cents": amount_cents})
    try:
        charge_id = provider.charge(card, amount_cents)
        logger.info("charge_succeeded", extra={"card": card, "amount_cents": amount_cents, "charge_id": charge_id})
        return charge_id
    except ProviderTimeout:
        logger.error("charge_timeout", extra={"card": card, "amount_cents": amount_cents})
        raise
    except ProviderError as e:
        logger.error("charge_failed", extra={"card": card, "amount_cents": amount_cents, "error": str(e)})
        raise
