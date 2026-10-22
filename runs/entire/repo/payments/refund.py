"""Refund orchestration on top of the payment provider client."""

import logging

from payments.provider import Provider, ProviderError, ProviderTimeout

logger = logging.getLogger(__name__)


def refund(provider: Provider, charge_id: str, amount_cents: int) -> str:
    """Refund part or all of ``charge_id`` for ``amount_cents`` and return the refund id."""
    logger.info(
        "event=refund_attempt charge_id=%s amount_cents=%d", charge_id, amount_cents
    )
    try:
        refund_id = provider.refund(charge_id, amount_cents)
    except ProviderTimeout:
        logger.warning(
            "event=refund_timeout charge_id=%s amount_cents=%d", charge_id, amount_cents
        )
        raise
    except ProviderError as exc:
        logger.error(
            "event=refund_error charge_id=%s amount_cents=%d error=%s",
            charge_id,
            amount_cents,
            exc,
        )
        raise
    logger.info(
        "event=refund_success charge_id=%s amount_cents=%d refund_id=%s",
        charge_id,
        amount_cents,
        refund_id,
    )
    return refund_id
