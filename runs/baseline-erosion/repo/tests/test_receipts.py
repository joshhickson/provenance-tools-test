from payments.receipts import format_receipt


def test_format_receipt():
    assert format_receipt("ch_123", "4242", 1234) == "Charged $12.34 to card ending 4242 (ch_123)"


def test_format_receipt_pads_single_digit_cents():
    assert format_receipt("ch_456", "0001", 100) == "Charged $1.00 to card ending 0001 (ch_456)"
