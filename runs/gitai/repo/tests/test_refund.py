from unittest.mock import Mock

import pytest

from payments.refund import refund
from payments.provider import ProviderError, ProviderTimeout


def test_refund_returns_refund_id():
    provider = Mock()
    provider.refund.return_value = "re_123"

    result = refund(provider, charge_id="ch_123", amount_cents=500)

    assert result == "re_123"
    provider.refund.assert_called_once_with("ch_123", 500)


def test_refund_propagates_timeout_without_retrying():
    provider = Mock()
    provider.refund.side_effect = ProviderTimeout("no response")

    with pytest.raises(ProviderTimeout):
        refund(provider, charge_id="ch_123", amount_cents=500)

    provider.refund.assert_called_once_with("ch_123", 500)


def test_refund_propagates_provider_error():
    provider = Mock()
    provider.refund.side_effect = ProviderError("refund rejected")

    with pytest.raises(ProviderError):
        refund(provider, charge_id="ch_123", amount_cents=500)

    provider.refund.assert_called_once_with("ch_123", 500)
