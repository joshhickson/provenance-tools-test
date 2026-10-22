from unittest.mock import Mock

import pytest

from payments.charge import charge
from payments.provider import ProviderError, ProviderTimeout


def test_charge_returns_charge_id():
    provider = Mock()
    provider.charge.return_value = "ch_123"

    result = charge(provider, card="tok_visa", amount_cents=1000)

    assert result == "ch_123"
    provider.charge.assert_called_once_with("tok_visa", 1000)


def test_charge_propagates_timeout_without_retrying():
    provider = Mock()
    provider.charge.side_effect = ProviderTimeout("no response")

    with pytest.raises(ProviderTimeout):
        charge(provider, card="tok_visa", amount_cents=1000)

    provider.charge.assert_called_once_with("tok_visa", 1000)


def test_charge_propagates_provider_error():
    provider = Mock()
    provider.charge.side_effect = ProviderError("card declined")

    with pytest.raises(ProviderError):
        charge(provider, card="tok_visa", amount_cents=1000)

    provider.charge.assert_called_once_with("tok_visa", 1000)
