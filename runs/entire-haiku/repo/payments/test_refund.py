"""Tests for the refund function."""

import pytest
from unittest.mock import Mock

from payments.refund import refund
from payments.provider import ProviderTimeout, ProviderError


def test_refund_success():
    """Test successful refund."""
    provider = Mock()
    provider.refund.return_value = "refund_123"

    result = refund(provider, "charge_456", 5000)

    assert result == "refund_123"
    provider.refund.assert_called_once_with("charge_456", 5000)


def test_refund_timeout_is_not_retried():
    """Test that ProviderTimeout is surfaced to caller without retry."""
    provider = Mock()
    provider.refund.side_effect = ProviderTimeout("connection timeout")

    with pytest.raises(ProviderTimeout):
        refund(provider, "charge_456", 5000)

    provider.refund.assert_called_once()


def test_refund_provider_error():
    """Test that ProviderError is surfaced to caller."""
    provider = Mock()
    provider.refund.side_effect = ProviderError("refund failed")

    with pytest.raises(ProviderError):
        refund(provider, "charge_456", 5000)

    provider.refund.assert_called_once_with("charge_456", 5000)
