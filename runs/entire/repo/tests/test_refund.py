from unittest.mock import Mock

import pytest

from payments.provider import Provider, ProviderError, ProviderTimeout
from payments.refund import refund


def test_refund_returns_provider_refund_id():
    provider = Mock(spec=Provider)
    provider.refund.return_value = "re_123"

    result = refund(provider, "ch_123", 1000)

    assert result == "re_123"
    provider.refund.assert_called_once_with("ch_123", 1000)


def test_refund_propagates_timeout():
    provider = Mock(spec=Provider)
    provider.refund.side_effect = ProviderTimeout()

    with pytest.raises(ProviderTimeout):
        refund(provider, "ch_123", 1000)

    provider.refund.assert_called_once_with("ch_123", 1000)


def test_refund_propagates_provider_error():
    provider = Mock(spec=Provider)
    provider.refund.side_effect = ProviderError("charge already refunded")

    with pytest.raises(ProviderError):
        refund(provider, "ch_123", 1000)

    provider.refund.assert_called_once_with("ch_123", 1000)
