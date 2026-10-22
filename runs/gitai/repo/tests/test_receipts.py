from payments.receipts import format_receipt


def test_format_receipt_basic():
    assert (
        format_receipt("ch_123", "4242", 1234)
        == "Charged $12.34 to card ending 4242 (ch_123)"
    )


def test_format_receipt_rounds_to_cents():
    assert (
        format_receipt("ch_456", "0001", 100)
        == "Charged $1.00 to card ending 0001 (ch_456)"
    )


def test_format_receipt_thousands_separator():
    assert (
        format_receipt("ch_789", "9999", 123456)
        == "Charged $1,234.56 to card ending 9999 (ch_789)"
    )
