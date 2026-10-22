"""Charge a card via the payment provider."""

import logging

from payments.provider import ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)


def charge(provider, card: str, amount_cents: int) -> str:
    """Charge a card and return its charge id."""
    try:
        logger.info("charge_attempt", extra={"card": card, "amount_cents": amount_cents})
        charge_id = provider.charge(card, amount_cents)
        logger.info("charge_success", extra={"card": card, "amount_cents": amount_cents, "charge_id": charge_id})
        return charge_id
    except ProviderTimeout as e:
        logger.warning("charge_timeout", extra={"card": card, "amount_cents": amount_cents, "error": str(e)})
        raise
    except ProviderError as e:
        logger.error("charge_error", extra={"card": card, "amount_cents": amount_cents, "error": str(e)})
        raise
