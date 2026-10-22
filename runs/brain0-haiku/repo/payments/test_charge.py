import pytest
from unittest.mock import Mock

from payments.charge import charge
from payments.provider import ProviderTimeout, ProviderError


def test_charge_success():
    provider = Mock()
    provider.charge.return_value = "charge_123"

    result = charge(provider, "card_456", 1000)

    assert result == "charge_123"


def test_charge_retries_on_timeout():
    provider = Mock()
    provider.charge.side_effect = [
        ProviderTimeout("Request timed out"),
        ProviderTimeout("Request timed out"),
        "charge_123"
    ]

    result = charge(provider, "card_456", 1000)

    assert result == "charge_123"
    assert provider.charge.call_count == 3


def test_charge_surfaces_timeout_after_retries():
    provider = Mock()
    provider.charge.side_effect = ProviderTimeout("Request timed out")

    with pytest.raises(ProviderTimeout):
        charge(provider, "card_456", 1000)

    assert provider.charge.call_count == 4  # initial + 3 retries


def test_charge_surfaces_provider_error():
    provider = Mock()
    provider.charge.side_effect = ProviderError("Card declined")

    with pytest.raises(ProviderError):
        charge(provider, "card_456", 1000)

    assert provider.charge.call_count == 1  # no retries on permanent errors
