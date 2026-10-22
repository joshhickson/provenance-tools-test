"""Refund a charge through the payment provider."""

import logging

from payments.provider import Provider, ProviderError, ProviderTimeout

logger = logging.getLogger(__name__)


def refund(provider: Provider, charge_id: str, amount_cents: int) -> str:
    """Refund part or all of a charge and return the resulting refund id.

    Like charge(), this never retries on ProviderTimeout - the provider
    doesn't support idempotency keys, so a timed-out refund may have
    already gone through. The timeout is surfaced to the caller.
    """
    logger.info(
        "refund.start charge_id=%s amount_cents=%d", charge_id, amount_cents
    )
    try:
        refund_id = provider.refund(charge_id, amount_cents)
    except ProviderTimeout:
        logger.warning(
            "refund.timeout charge_id=%s amount_cents=%d", charge_id, amount_cents
        )
        raise
    except ProviderError as e:
        logger.error(
            "refund.error charge_id=%s amount_cents=%d error=%s",
            charge_id,
            amount_cents,
            e,
        )
        raise
    logger.info(
        "refund.success charge_id=%s amount_cents=%d refund_id=%s",
        charge_id,
        amount_cents,
        refund_id,
    )
    return refund_id
