"""Refund implementation."""

import logging

from payments.provider import Provider, ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)


def refund(provider: Provider, charge_id: str, amount_cents: int) -> str:
    """Refund part or all of a charge; ProviderTimeout is surfaced because the provider doesn't support idempotency keys."""
    logger.info("Attempting refund", extra={"charge_id": charge_id, "amount_cents": amount_cents})

    try:
        refund_id = provider.refund(charge_id, amount_cents)
        logger.info("Refund successful", extra={"refund_id": refund_id, "charge_id": charge_id, "amount_cents": amount_cents})
        return refund_id
    except ProviderTimeout:
        logger.warning(
            "Refund timed out",
            extra={"charge_id": charge_id, "amount_cents": amount_cents},
        )
        raise
    except ProviderError as e:
        logger.error(
            "Refund failed",
            extra={"error": str(e), "charge_id": charge_id, "amount_cents": amount_cents},
        )
        raise
