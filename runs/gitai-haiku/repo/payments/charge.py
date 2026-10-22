"""Charge a card using a payment provider."""

import logging
import time
from payments.provider import Provider, ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)


def charge(provider: Provider, card: str, amount_cents: int, max_retries: int = 3) -> str:
    """Charge a card using the provider and return the charge id.

    Retries on transient timeout errors with exponential backoff.
    Fails immediately on provider errors (non-transient).
    """
    logger.info("charge_started", extra={"card": card, "amount_cents": amount_cents})

    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            charge_id = provider.charge(card=card, amount_cents=amount_cents)
            logger.info("charge_succeeded", extra={"card": card, "amount_cents": amount_cents, "charge_id": charge_id})
            return charge_id
        except ProviderTimeout as e:
            last_exception = e
            if attempt < max_retries:
                backoff_seconds = 2 ** attempt
                logger.warning("charge_timeout", extra={"card": card, "amount_cents": amount_cents, "attempt": attempt + 1, "max_retries": max_retries + 1, "backoff_seconds": backoff_seconds})
                time.sleep(backoff_seconds)
            else:
                logger.error("charge_timeout", extra={"card": card, "amount_cents": amount_cents})
        except ProviderError as e:
            logger.error("charge_failed", extra={"card": card, "amount_cents": amount_cents, "error": str(e)})
            raise

    raise last_exception
