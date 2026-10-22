"""Charge a card through the payment provider."""

import logging

from payments.provider import Provider, ProviderError, ProviderTimeout

logger = logging.getLogger(__name__)


# The provider does not support idempotency keys, and a request that times
# out may still have gone through on their end. Retrying after a
# ProviderTimeout could double-charge the card, so we never retry here —
# ProviderTimeout is left to propagate to the caller to decide what to do.
def charge(provider: Provider, card: str, amount_cents: int) -> str:
    """Charge `card` for `amount_cents` and return the resulting charge id."""
    card_last4 = card[-4:] if card else card
    logger.info("event=charge.start amount_cents=%s card_last4=%s", amount_cents, card_last4)
    try:
        charge_id = provider.charge(card, amount_cents)
    except ProviderTimeout:
        logger.error("event=charge.timeout amount_cents=%s card_last4=%s", amount_cents, card_last4)
        raise
    except ProviderError as exc:
        logger.error(
            "event=charge.error amount_cents=%s card_last4=%s error=%s", amount_cents, card_last4, exc
        )
        raise
    logger.info("event=charge.success amount_cents=%s charge_id=%s", amount_cents, charge_id)
    return charge_id
