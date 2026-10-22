"""Charge orchestration on top of the payment provider client."""

import logging

from payments.provider import Provider, ProviderError, ProviderTimeout

logger = logging.getLogger(__name__)


def _masked(card: str) -> str:
    return f"***{card[-4:]}" if len(card) >= 4 else "***"


def charge(provider: Provider, card: str, amount_cents: int) -> str:
    """Charge a card for ``amount_cents`` and return the charge id."""
    logger.info("event=charge_attempt card=%s amount_cents=%d", _masked(card), amount_cents)
    try:
        charge_id = provider.charge(card, amount_cents)
    except ProviderTimeout:
        # Not retried: the provider lacks idempotency keys, so a timed-out
        # request may have already gone through and retrying risks a double charge.
        logger.warning(
            "event=charge_timeout card=%s amount_cents=%d", _masked(card), amount_cents
        )
        raise
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
