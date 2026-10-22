"""Charging logic on top of the payment provider client."""

import logging

from payments.provider import Provider, ProviderError, ProviderTimeout

logger = logging.getLogger(__name__)


def _masked(card: str) -> str:
    return f"***{card[-4:]}" if len(card) >= 4 else "***"


def charge(provider: Provider, card: str, amount_cents: int) -> str:
    """Charge a card for amount_cents via provider and return the charge id."""
    logger.info("charge.attempt card=%s amount_cents=%d", _masked(card), amount_cents)
    try:
        charge_id = provider.charge(card, amount_cents)
    except ProviderTimeout:
        # No idempotency keys on the provider side, and a timed-out request may
        # have still gone through; retrying here risks double-charging the card.
        logger.error(
            "charge.timeout card=%s amount_cents=%d", _masked(card), amount_cents
        )
        raise
    except ProviderError as exc:
        logger.error(
            "charge.error card=%s amount_cents=%d error=%s",
            _masked(card),
            amount_cents,
            exc,
        )
        raise
    logger.info(
        "charge.success card=%s amount_cents=%d charge_id=%s",
        _masked(card),
        amount_cents,
        charge_id,
    )
    return charge_id
