"""Tests for the format_receipt function."""

from payments.receipts import format_receipt


def test_format_receipt_basic():
    """Test basic receipt formatting."""
    receipt = format_receipt("ch_123", "4242", 1234)
    assert receipt == "Charged $12.34 to card ending 4242 (ch_123)"


def test_format_receipt_whole_dollar():
    """Test receipt with whole dollar amount."""
    receipt = format_receipt("ch_456", "5555", 5000)
    assert receipt == "Charged $50.00 to card ending 5555 (ch_456)"


def test_format_receipt_single_cent():
    """Test receipt with single cent."""
    receipt = format_receipt("ch_789", "1111", 1)
    assert receipt == "Charged $0.01 to card ending 1111 (ch_789)"
