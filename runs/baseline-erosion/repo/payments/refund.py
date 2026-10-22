"""Refund a charge through the payment provider."""

import logging

from payments.provider import Provider, ProviderError, ProviderTimeout

logger = logging.getLogger(__name__)


# Same no-retry rule as charge.py: the provider does not support idempotency
# keys, so a ProviderTimeout here is left to propagate to the caller instead
# of being retried, since the refund may have already gone through.
def refund(provider: Provider, charge_id: str, amount_cents: int) -> str:
    """Refund `amount_cents` of `charge_id` and return the resulting refund id."""
    logger.info("event=refund.start charge_id=%s amount_cents=%s", charge_id, amount_cents)
    try:
        refund_id = provider.refund(charge_id, amount_cents)
    except ProviderTimeout:
        logger.error("event=refund.timeout charge_id=%s amount_cents=%s", charge_id, amount_cents)
        raise
    except ProviderError as exc:
        logger.error(
            "event=refund.error charge_id=%s amount_cents=%s error=%s", charge_id, amount_cents, exc
        )
        raise
    logger.info("event=refund.success charge_id=%s amount_cents=%s refund_id=%s", charge_id, amount_cents, refund_id)
    return refund_id
