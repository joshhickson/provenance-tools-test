"""Charge a card via the payment provider."""

import logging
import time

from payments.provider import ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
INITIAL_BACKOFF = 0.5


def charge(provider, card: str, amount_cents: int) -> str:
    """Charge a card and return its charge id."""
    backoff = INITIAL_BACKOFF
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("charge_attempt", extra={"card": card, "amount_cents": amount_cents, "attempt": attempt})
            charge_id = provider.charge(card, amount_cents)
            logger.info("charge_success", extra={"card": card, "amount_cents": amount_cents, "charge_id": charge_id, "attempt": attempt})
            return charge_id
        except ProviderTimeout as e:
            last_error = e
            if attempt < MAX_RETRIES:
                logger.warning("charge_timeout_retrying", extra={"card": card, "amount_cents": amount_cents, "error": str(e), "attempt": attempt, "backoff": backoff})
                time.sleep(backoff)
                backoff *= 2
            else:
                logger.warning("charge_timeout_exhausted", extra={"card": card, "amount_cents": amount_cents, "error": str(e), "attempts": attempt})
        except ProviderError as e:
            logger.error("charge_error", extra={"card": card, "amount_cents": amount_cents, "error": str(e)})
            raise

    raise last_error
