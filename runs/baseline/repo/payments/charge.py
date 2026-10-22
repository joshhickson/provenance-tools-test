"""Charge a card through the payment provider."""

import logging

from payments.provider import Provider, ProviderError, ProviderTimeout

logger = logging.getLogger(__name__)


def charge(provider: Provider, card: str, amount_cents: int) -> str:
    """Charge a card and return the resulting charge id.

    The provider does not support idempotency keys, and a request that
    times out may still have gone through on their end. So a
    ProviderTimeout is never retried here - it's surfaced to the caller,
    who must decide how to handle the ambiguity (e.g. check charge
    history before trying again).
    """
    card_last4 = card[-4:]
    logger.info("charge.start card_last4=%s amount_cents=%d", card_last4, amount_cents)
    try:
        charge_id = provider.charge(card, amount_cents)
    except ProviderTimeout:
        logger.warning(
            "charge.timeout card_last4=%s amount_cents=%d", card_last4, amount_cents
        )
        raise
    except ProviderError as e:
        logger.error(
            "charge.error card_last4=%s amount_cents=%d error=%s",
            card_last4,
            amount_cents,
            e,
        )
        raise
    logger.info(
        "charge.success card_last4=%s amount_cents=%d charge_id=%s",
        card_last4,
        amount_cents,
        charge_id,
    )
    return charge_id
