import pytest
from unittest.mock import Mock
from payments.refund import refund
from payments.provider import ProviderTimeout, ProviderError


def test_refund_success():
    provider = Mock()
    provider.refund.return_value = "refund_12345"

    refund_id = refund(provider, "charge_12345", 1000)

    assert refund_id == "refund_12345"


def test_refund_provider_error():
    provider = Mock()
    provider.refund.side_effect = ProviderError("Charge not found")

    with pytest.raises(ProviderError, match="Charge not found"):
        refund(provider, "charge_12345", 1000)


def test_refund_timeout_no_retry():
    provider = Mock()
    provider.refund.side_effect = ProviderTimeout("Request timed out")

    with pytest.raises(ProviderTimeout, match="Request timed out"):
        refund(provider, "charge_12345", 1000)
