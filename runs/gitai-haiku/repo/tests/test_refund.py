"""Tests for the refund function."""

import pytest
from unittest.mock import Mock

from payments.refund import refund
from payments.provider import ProviderTimeout, ProviderError


def test_refund_success():
    """Test successful refund."""
    provider = Mock()
    provider.refund.return_value = "refund_456"

    result = refund(provider, charge_id="charge_123", amount_cents=1000)

    assert result == "refund_456"


def test_refund_timeout():
    """Test that timeout is surfaced to the caller."""
    provider = Mock()
    provider.refund.side_effect = ProviderTimeout("Request timed out")

    with pytest.raises(ProviderTimeout):
        refund(provider, charge_id="charge_123", amount_cents=1000)


def test_refund_provider_error():
    """Test that provider error is surfaced to the caller."""
    provider = Mock()
    provider.refund.side_effect = ProviderError("Charge not found")

    with pytest.raises(ProviderError):
        refund(provider, charge_id="charge_123", amount_cents=1000)
