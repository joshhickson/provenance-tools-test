"""Tests for receipt formatting."""

import pytest

from payments.receipts import format_receipt


def test_format_receipt_basic():
    """Test basic receipt formatting."""
    result = format_receipt("ch_123", "4242", 1234)
    assert result == "Charged $12.34 to card ending 4242 (ch_123)"


def test_format_receipt_with_single_cent():
    """Test receipt with single cent."""
    result = format_receipt("ch_456", "5555", 101)
    assert result == "Charged $1.01 to card ending 5555 (ch_456)"


def test_format_receipt_with_round_dollar():
    """Test receipt with round dollar amount."""
    result = format_receipt("ch_789", "1111", 5000)
    assert result == "Charged $50.00 to card ending 1111 (ch_789)"


def test_format_receipt_with_zero_dollars():
    """Test receipt with amount less than a dollar."""
    result = format_receipt("ch_000", "9999", 99)
    assert result == "Charged $0.99 to card ending 9999 (ch_000)"


def test_format_receipt_with_zero_amount():
    """Test receipt with zero amount."""
    result = format_receipt("ch_zero", "0000", 0)
    assert result == "Charged $0.00 to card ending 0000 (ch_zero)"


def test_format_receipt_with_large_amount():
    """Test receipt with large amount."""
    result = format_receipt("ch_big", "8888", 999999)
    assert result == "Charged $9999.99 to card ending 8888 (ch_big)"


def test_format_receipt_with_different_card_formats():
    """Test receipt with various card last4 formats."""
    result = format_receipt("ch_test", "0001", 5000)
    assert result == "Charged $50.00 to card ending 0001 (ch_test)"
