"""Refund a charge via the payment provider."""

import logging

from payments.provider import ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)


def refund(provider, charge_id: str, amount_cents: int) -> str:
    """Refund a charge and return its refund id."""
    try:
        logger.info("refund_attempt", extra={"charge_id": charge_id, "amount_cents": amount_cents})
        refund_id = provider.refund(charge_id, amount_cents)
        logger.info("refund_success", extra={"charge_id": charge_id, "amount_cents": amount_cents, "refund_id": refund_id})
        return refund_id
    except ProviderTimeout as e:
        logger.warning("refund_timeout", extra={"charge_id": charge_id, "amount_cents": amount_cents, "error": str(e)})
        raise
    except ProviderError as e:
        logger.error("refund_error", extra={"charge_id": charge_id, "amount_cents": amount_cents, "error": str(e)})
        raise
