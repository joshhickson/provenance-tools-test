"""Tests for the refund function."""

import pytest
from unittest.mock import Mock

from payments.refund import refund
from payments.provider import ProviderTimeout, ProviderError


def test_refund_success():
    """Test successful refund returns the refund ID."""
    provider = Mock()
    provider.refund.return_value = "refund_123"

    result = refund(provider, "charge_123", 1000)

    assert result == "refund_123"


def test_refund_timeout_is_surfaced():
    """Test that ProviderTimeout is surfaced to the caller."""
    provider = Mock()
    provider.refund.side_effect = ProviderTimeout("Request timed out")

    with pytest.raises(ProviderTimeout):
        refund(provider, "charge_123", 1000)


def test_refund_provider_error_is_surfaced():
    """Test that ProviderError is surfaced to the caller."""
    provider = Mock()
    provider.refund.side_effect = ProviderError("Charge not found")

    with pytest.raises(ProviderError):
        refund(provider, "charge_123", 1000)
