import pytest
from payments.receipts import format_receipt


def test_format_receipt_basic():
    result = format_receipt("ch_123", "4242", 1234)
    assert result == "Charged $12.34 to card ending 4242 (ch_123)"


def test_format_receipt_whole_dollar():
    result = format_receipt("ch_456", "1111", 5000)
    assert result == "Charged $50.00 to card ending 1111 (ch_456)"


def test_format_receipt_cents_only():
    result = format_receipt("ch_789", "9999", 99)
    assert result == "Charged $0.99 to card ending 9999 (ch_789)"


def test_format_receipt_zero_amount():
    result = format_receipt("ch_000", "5555", 0)
    assert result == "Charged $0.00 to card ending 5555 (ch_000)"


def test_format_receipt_large_amount():
    result = format_receipt("ch_999", "3333", 999999)
    assert result == "Charged $9999.99 to card ending 3333 (ch_999)"
