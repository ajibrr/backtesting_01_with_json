from conditions.previous_candles import greater_than_all_previous, absolute_greater_than_all_previous

def test_gamma():
    assert greater_than_all_previous(10, [1, 2, 3])

def test_delta():
    assert absolute_greater_than_all_previous(-10, [-2, 3, -5])
