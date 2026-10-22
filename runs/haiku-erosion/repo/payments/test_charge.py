import pytest
from unittest.mock import Mock, patch
from payments.charge import charge, MAX_RETRIES
from payments.provider import ProviderTimeout, ProviderError


def test_charge_success():
    provider = Mock()
    provider.charge.return_value = "charge_12345"

    charge_id = charge(provider, "4111111111111111", 1000)

    assert charge_id == "charge_12345"


def test_charge_provider_error():
    provider = Mock()
    provider.charge.side_effect = ProviderError("Card declined")

    with pytest.raises(ProviderError, match="Card declined"):
        charge(provider, "4111111111111111", 1000)


def test_charge_timeout_with_retry_succeeds():
    provider = Mock()
    provider.charge.side_effect = [
        ProviderTimeout("Request timed out"),
        ProviderTimeout("Request timed out"),
        "charge_12345"
    ]

    with patch('payments.charge.time.sleep'):
        charge_id = charge(provider, "4111111111111111", 1000)

    assert charge_id == "charge_12345"
    assert provider.charge.call_count == 3


def test_charge_timeout_exhausts_retries():
    provider = Mock()
    provider.charge.side_effect = ProviderTimeout("Request timed out")

    with patch('payments.charge.time.sleep'):
        with pytest.raises(ProviderTimeout, match="Request timed out"):
            charge(provider, "4111111111111111", 1000)

    assert provider.charge.call_count == MAX_RETRIES
