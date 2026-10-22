"""Tests for the charge function."""

import pytest
from unittest.mock import Mock

from payments.charge import charge
from payments.provider import ProviderTimeout, ProviderError


def test_charge_success():
    """Test successful charge."""
    provider = Mock()
    provider.charge.return_value = "charge_123"

    result = charge(provider, "card_456", 5000)

    assert result == "charge_123"
    provider.charge.assert_called_once_with("card_456", 5000)


def test_charge_timeout_is_retried():
    """Test that ProviderTimeout is retried."""
    provider = Mock()
    provider.charge.side_effect = [
        ProviderTimeout("connection timeout"),
        ProviderTimeout("connection timeout"),
        "charge_123",
    ]

    result = charge(provider, "card_456", 5000)

    assert result == "charge_123"
    assert provider.charge.call_count == 3


def test_charge_timeout_exhausted():
    """Test that ProviderTimeout is raised after max retries."""
    provider = Mock()
    provider.charge.side_effect = ProviderTimeout("connection timeout")

    with pytest.raises(ProviderTimeout):
        charge(provider, "card_456", 5000)

    assert provider.charge.call_count == 3


def test_charge_provider_error():
    """Test that ProviderError is surfaced to caller."""
    provider = Mock()
    provider.charge.side_effect = ProviderError("card declined")

    with pytest.raises(ProviderError):
        charge(provider, "card_456", 5000)

    provider.charge.assert_called_once_with("card_456", 5000)


