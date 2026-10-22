import logging
from payments.provider import Provider, ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)


def refund(provider: Provider, charge_id: str, amount_cents: int) -> str:
    """Refund part or all of a charge via the provider and return the refund id."""
    logger.info("refund_start", extra={"charge_id": charge_id, "amount_cents": amount_cents})

    try:
        refund_id = provider.refund(charge_id, amount_cents)
        logger.info("refund_success", extra={"refund_id": refund_id, "charge_id": charge_id, "amount_cents": amount_cents})
        return refund_id
    except ProviderTimeout:
        logger.error("refund_timeout", extra={"charge_id": charge_id, "amount_cents": amount_cents})
        raise
    except ProviderError as e:
        logger.error("refund_error", extra={"charge_id": charge_id, "amount_cents": amount_cents, "error": str(e)})
        raise
