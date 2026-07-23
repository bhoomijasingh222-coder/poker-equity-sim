import pytest

from poker.decisions import required_equity, call_ev

def test_required_equity():
    result = required_equity(pot_before_call=150, call=50 )

    assert result == pytest.approx(0.25)


def test_positive_call_ev():
    result = call_ev(equity=0.35, pot_before_call=150, call=50)

    assert result == pytest.approx(20.0)


def test_negative_call_ev():
    result = call_ev(equity=0.20, pot_before_call=150,call=50)

    assert result == pytest.approx(-10.0)