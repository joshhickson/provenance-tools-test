import logging
import time
from payments.provider import Provider, ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
INITIAL_BACKOFF_SECONDS = 1


def charge(provider: Provider, card: str, amount_cents: int) -> str:
    """Charge a card via the provider and return the charge id."""
    card_last_four = card[-4:] if len(card) >= 4 else "****"
    logger.info("charge_start", extra={"amount_cents": amount_cents, "card_last_four": card_last_four})

    last_timeout = None
    for attempt in range(MAX_RETRIES):
        try:
            charge_id = provider.charge(card, amount_cents)
            logger.info("charge_success", extra={"charge_id": charge_id, "amount_cents": amount_cents})
            return charge_id
        except ProviderTimeout as e:
            last_timeout = e
            if attempt < MAX_RETRIES - 1:
                backoff = INITIAL_BACKOFF_SECONDS * (2 ** attempt)
                logger.warning("charge_timeout_retry", extra={"attempt": attempt + 1, "backoff_seconds": backoff, "amount_cents": amount_cents})
                time.sleep(backoff)
            else:
                logger.error("charge_timeout", extra={"amount_cents": amount_cents, "card_last_four": card_last_four})
        except ProviderError as e:
            logger.error("charge_error", extra={"amount_cents": amount_cents, "error": str(e)})
            raise

    raise last_timeout
