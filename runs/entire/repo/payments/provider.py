"""Client for the payment provider's API (stubbed for this demo)."""


class ProviderTimeout(Exception):
    """The provider did not answer within the timeout."""


class ProviderError(Exception):
    """The provider rejected the request."""


class Provider:
    def charge(
        self, card: str, amount_cents: int, idempotency_key: str, timeout: float = 10.0
    ) -> str:
        """Charge a card and return a charge id.

        ``idempotency_key`` must be reused across retries of the same logical
        charge so the provider can recognize a retried request and return the
        original result instead of charging the card twice.
        """
        raise NotImplementedError("the real HTTP client is not part of this demo")

    def refund(self, charge_id: str, amount_cents: int, timeout: float = 10.0) -> str:
        """Refund part or all of a charge and return a refund id."""
        raise NotImplementedError("the real HTTP client is not part of this demo")
