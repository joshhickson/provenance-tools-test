"""Charge orchestration on top of the payment provider client."""

import logging
import time
import uuid

from payments.provider import Provider, ProviderError, ProviderTimeout

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = 0.5


def _masked(card: str) -> str:
    return f"***{card[-4:]}" if len(card) >= 4 else "***"


def charge(provider: Provider, card: str, amount_cents: int) -> str:
    """Charge a card for ``amount_cents`` and return the charge id."""
    logger.info("event=charge_attempt card=%s amount_cents=%d", _masked(card), amount_cents)
    # Reused across retries: lets the provider recognize a retried request
    # from the same logical charge and avoid billing the card twice.
    idempotency_key = uuid.uuid4().hex
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            charge_id = provider.charge(card, amount_cents, idempotency_key=idempotency_key)
        except ProviderTimeout:
            logger.warning(
                "event=charge_timeout card=%s amount_cents=%d attempt=%d",
                _masked(card),
                amount_cents,
                attempt,
            )
            if attempt == MAX_ATTEMPTS:
                raise
            time.sleep(RETRY_BACKOFF_SECONDS * attempt)
            continue
        except ProviderError as exc:
            logger.error(
                "event=charge_error card=%s amount_cents=%d error=%s",
                _masked(card),
                amount_cents,
                exc,
            )
            raise
        logger.info(
            "event=charge_success card=%s amount_cents=%d charge_id=%s",
            _masked(card),
            amount_cents,
            charge_id,
        )
        return charge_id
