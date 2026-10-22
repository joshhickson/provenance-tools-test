from unittest.mock import ANY, Mock

import pytest

from payments.charge import MAX_ATTEMPTS, charge
from payments.provider import Provider, ProviderError, ProviderTimeout


def test_charge_returns_provider_charge_id():
    provider = Mock(spec=Provider)
    provider.charge.return_value = "ch_123"

    result = charge(provider, "4242424242424242", 1000)

    assert result == "ch_123"
    provider.charge.assert_called_once_with(
        "4242424242424242", 1000, idempotency_key=ANY
    )


def test_charge_retries_timeout_then_succeeds_with_same_idempotency_key(monkeypatch):
    monkeypatch.setattr("payments.charge.time.sleep", lambda _: None)
    provider = Mock(spec=Provider)
    provider.charge.side_effect = [ProviderTimeout(), "ch_123"]

    result = charge(provider, "4242424242424242", 1000)

    assert result == "ch_123"
    assert provider.charge.call_count == 2
    first_key = provider.charge.call_args_list[0].kwargs["idempotency_key"]
    second_key = provider.charge.call_args_list[1].kwargs["idempotency_key"]
    assert first_key == second_key


def test_charge_raises_after_exhausting_retries(monkeypatch):
    monkeypatch.setattr("payments.charge.time.sleep", lambda _: None)
    provider = Mock(spec=Provider)
    provider.charge.side_effect = ProviderTimeout()

    with pytest.raises(ProviderTimeout):
        charge(provider, "4242424242424242", 1000)

    assert provider.charge.call_count == MAX_ATTEMPTS
    keys = {call.kwargs["idempotency_key"] for call in provider.charge.call_args_list}
    assert len(keys) == 1


def test_charge_propagates_provider_error_without_retrying():
    provider = Mock(spec=Provider)
    provider.charge.side_effect = ProviderError("card declined")

    with pytest.raises(ProviderError):
        charge(provider, "4242424242424242", 1000)

    provider.charge.assert_called_once_with(
        "4242424242424242", 1000, idempotency_key=ANY
    )
