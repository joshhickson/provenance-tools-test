"""Charge implementation."""

import logging
import time

from payments.provider import Provider, ProviderTimeout, ProviderError

logger = logging.getLogger(__name__)


def charge(provider: Provider, card: str, amount_cents: int, max_retries: int = 2) -> str:
    """Charge a card with retries on transient timeout errors."""
    logger.info("Attempting charge", extra={"amount_cents": amount_cents, "card_last4": card[-4:]})

    for attempt in range(max_retries + 1):
        try:
            charge_id = provider.charge(card, amount_cents)
            logger.info("Charge successful", extra={"charge_id": charge_id, "amount_cents": amount_cents})
            return charge_id
        except ProviderTimeout:
            if attempt < max_retries:
                wait_time = 2 ** attempt
                logger.warning(
                    "Charge timed out, retrying",
                    extra={"amount_cents": amount_cents, "card_last4": card[-4:], "retry_attempt": attempt + 1, "wait_seconds": wait_time},
                )
                time.sleep(wait_time)
            else:
                logger.warning(
                    "Charge timed out",
                    extra={"amount_cents": amount_cents, "card_last4": card[-4:]},
                )
                raise
        except ProviderError as e:
            logger.error(
                "Charge failed",
                extra={"error": str(e), "amount_cents": amount_cents, "card_last4": card[-4:]},
            )
            raise
