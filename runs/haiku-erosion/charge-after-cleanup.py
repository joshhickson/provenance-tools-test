import logging
from payments.provider import Provider, ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)


def charge(provider: Provider, card: str, amount_cents: int) -> str:
    """Charge a card via the provider and return the charge id."""
    card_last_four = card[-4:] if len(card) >= 4 else "****"
    logger.info("charge_start", extra={"amount_cents": amount_cents, "card_last_four": card_last_four})

    try:
        charge_id = provider.charge(card, amount_cents)
        logger.info("charge_success", extra={"charge_id": charge_id, "amount_cents": amount_cents})
        return charge_id
    except ProviderTimeout:
        logger.error("charge_timeout", extra={"amount_cents": amount_cents, "card_last_four": card_last_four})
        raise
    except ProviderError as e:
        logger.error("charge_error", extra={"amount_cents": amount_cents, "error": str(e)})
        raise
