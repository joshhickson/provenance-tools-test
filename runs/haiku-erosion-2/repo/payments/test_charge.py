"""Tests for the charge function."""

import pytest
from unittest.mock import Mock

from payments.charge import charge
from payments.provider import ProviderTimeout, ProviderError


def test_charge_success():
    """Test successful charge returns the charge ID."""
    provider = Mock()
    provider.charge.return_value = "charge_123"

    result = charge(provider, "4111111111111111", 1000)

    assert result == "charge_123"


def test_charge_timeout_is_surfaced():
    """Test that ProviderTimeout is surfaced to the caller."""
    provider = Mock()
    provider.charge.side_effect = ProviderTimeout("Request timed out")

    with pytest.raises(ProviderTimeout):
        charge(provider, "4111111111111111", 1000)


def test_charge_provider_error_is_surfaced():
    """Test that ProviderError is surfaced to the caller."""
    provider = Mock()
    provider.charge.side_effect = ProviderError("Invalid card")

    with pytest.raises(ProviderError):
        charge(provider, "4111111111111111", 1000)
