"""Tests for the receipt formatting."""

from payments.receipts import format_receipt


def test_format_receipt_basic():
    """Test basic receipt formatting."""
    result = format_receipt(charge_id="ch_123", card_last4="4242", amount_cents=1234)
    assert result == "Charged $12.34 to card ending 4242 (ch_123)"


def test_format_receipt_whole_dollars():
    """Test receipt formatting with whole dollars."""
    result = format_receipt(charge_id="ch_456", card_last4="5555", amount_cents=5000)
    assert result == "Charged $50.00 to card ending 5555 (ch_456)"


def test_format_receipt_single_cent():
    """Test receipt formatting with single cent amount."""
    result = format_receipt(charge_id="ch_789", card_last4="9999", amount_cents=1)
    assert result == "Charged $0.01 to card ending 9999 (ch_789)"


def test_format_receipt_zero_amount():
    """Test receipt formatting with zero amount."""
    result = format_receipt(charge_id="ch_000", card_last4="0000", amount_cents=0)
    assert result == "Charged $0.00 to card ending 0000 (ch_000)"
