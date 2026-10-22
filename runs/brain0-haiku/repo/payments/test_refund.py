import pytest
from unittest.mock import Mock

from payments.refund import refund
from payments.provider import ProviderTimeout, ProviderError


def test_refund_success():
    provider = Mock()
    provider.refund.return_value = "refund_123"

    result = refund(provider, "charge_456", 1000)

    assert result == "refund_123"


def test_refund_surfaces_timeout():
    provider = Mock()
    provider.refund.side_effect = ProviderTimeout("Request timed out")

    with pytest.raises(ProviderTimeout):
        refund(provider, "charge_456", 1000)


def test_refund_surfaces_provider_error():
    provider = Mock()
    provider.refund.side_effect = ProviderError("Refund denied")

    with pytest.raises(ProviderError):
        refund(provider, "charge_456", 1000)
