import pytest

from payments.receipts import format_receipt


def test_format_receipt_basic():
    result = format_receipt("ch_123", "4242", 1234)
    assert result == "Charged $12.34 to card ending 4242 (ch_123)"


def test_format_receipt_zero_cents():
    result = format_receipt("ch_456", "5678", 5000)
    assert result == "Charged $50.00 to card ending 5678 (ch_456)"


def test_format_receipt_one_cent():
    result = format_receipt("ch_789", "9012", 1)
    assert result == "Charged $0.01 to card ending 9012 (ch_789)"
