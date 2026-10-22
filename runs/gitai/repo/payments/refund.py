"""Refund logic on top of the payment provider client."""

import logging

from payments.provider import Provider, ProviderError, ProviderTimeout

logger = logging.getLogger(__name__)


def refund(provider: Provider, charge_id: str, amount_cents: int) -> str:
    """Refund part or all of a charge via provider and return the refund id."""
    logger.info(
        "refund.attempt charge_id=%s amount_cents=%d", charge_id, amount_cents
    )
    try:
        refund_id = provider.refund(charge_id, amount_cents)
    except ProviderTimeout:
        # Same no-retry rule as charge(): no idempotency keys on the provider
        # side, so a timed-out refund is left to propagate instead of retried.
        logger.error(
            "refund.timeout charge_id=%s amount_cents=%d", charge_id, amount_cents
        )
        raise
    except ProviderError as exc:
        logger.error(
            "refund.error charge_id=%s amount_cents=%d error=%s",
            charge_id,
            amount_cents,
            exc,
        )
        raise
    logger.info(
        "refund.success charge_id=%s amount_cents=%d refund_id=%s",
        charge_id,
        amount_cents,
        refund_id,
    )
    return refund_id
