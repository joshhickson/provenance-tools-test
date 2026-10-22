from payments.receipts import format_receipt


def test_format_receipt_basic():
    assert (
        format_receipt("ch_123", "4242", 1234)
        == "Charged $12.34 to card ending 4242 (ch_123)"
    )


def test_format_receipt_pads_single_digit_cents():
    assert (
        format_receipt("ch_456", "1111", 1005)
        == "Charged $10.05 to card ending 1111 (ch_456)"
    )


def test_format_receipt_whole_dollar_amount():
    assert (
        format_receipt("ch_789", "9999", 500)
        == "Charged $5.00 to card ending 9999 (ch_789)"
    )
