"""Tests for the charge function."""

import pytest
from unittest.mock import Mock, call

from payments.charge import charge
from payments.provider import ProviderTimeout, ProviderError


def test_charge_success():
    """Test successful charge."""
    provider = Mock()
    provider.charge.return_value = "charge_123"

    result = charge(provider, card="4111111111111111", amount_cents=1000)

    assert result == "charge_123"


def test_charge_timeout_fails_after_retries():
    """Test that timeout is retried and then surfaced to the caller."""
    provider = Mock()
    provider.charge.side_effect = ProviderTimeout("Request timed out")

    with pytest.raises(ProviderTimeout):
        charge(provider, card="4111111111111111", amount_cents=1000, max_retries=3)

    assert provider.charge.call_count == 4


def test_charge_timeout_succeeds_on_retry():
    """Test that transient timeout is recovered by retry."""
    provider = Mock()
    provider.charge.side_effect = [
        ProviderTimeout("Request timed out"),
        ProviderTimeout("Request timed out"),
        "charge_123",
    ]

    result = charge(provider, card="4111111111111111", amount_cents=1000, max_retries=3)

    assert result == "charge_123"
    assert provider.charge.call_count == 3


def test_charge_provider_error():
    """Test that provider error is surfaced to the caller without retries."""
    provider = Mock()
    provider.charge.side_effect = ProviderError("Card declined")

    with pytest.raises(ProviderError):
        charge(provider, card="4111111111111111", amount_cents=1000, max_retries=3)

    assert provider.charge.call_count == 1
