from unittest.mock import Mock

import pytest

from payments.charge import charge
from payments.provider import Provider, ProviderError, ProviderTimeout


def test_charge_returns_provider_charge_id():
    provider = Mock(spec=Provider)
    provider.charge.return_value = "ch_123"

    result = charge(provider, "4242424242424242", 1500)

    assert result == "ch_123"
    provider.charge.assert_called_once_with("4242424242424242", 1500)


def test_charge_does_not_retry_on_timeout():
    provider = Mock(spec=Provider)
    provider.charge.side_effect = ProviderTimeout()

    with pytest.raises(ProviderTimeout):
        charge(provider, "4242424242424242", 1500)

    assert provider.charge.call_count == 1


def test_charge_surfaces_provider_error():
    provider = Mock(spec=Provider)
    provider.charge.side_effect = ProviderError("card declined")

    with pytest.raises(ProviderError):
        charge(provider, "4242424242424242", 1500)

    assert provider.charge.call_count == 1
