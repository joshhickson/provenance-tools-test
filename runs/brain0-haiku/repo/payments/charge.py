"""Charge a card using a payment provider."""

import logging
import time

from payments.provider import Provider, ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
INITIAL_BACKOFF = 0.1


def charge(provider: Provider, card: str, amount_cents: int) -> str:
    """Charge a card using the provider and return the charge id."""
    logger.info("charge_started", extra={"card": card, "amount_cents": amount_cents})

    last_exception = None
    backoff = INITIAL_BACKOFF

    for attempt in range(MAX_RETRIES + 1):
        try:
            charge_id = provider.charge(card, amount_cents)
            logger.info("charge_succeeded", extra={"card": card, "amount_cents": amount_cents, "charge_id": charge_id})
            return charge_id
        except ProviderError as e:
            logger.error("charge_failed", extra={"card": card, "amount_cents": amount_cents, "error": str(e)})
            raise
        except ProviderTimeout:
            last_exception = ProviderTimeout("Request timed out")
            if attempt < MAX_RETRIES:
                logger.warning("charge_timeout_retrying", extra={"card": card, "amount_cents": amount_cents, "attempt": attempt + 1, "backoff_seconds": backoff})
                time.sleep(backoff)
                backoff *= 2
            else:
                logger.error("charge_timeout", extra={"card": card, "amount_cents": amount_cents})

    raise last_exception
