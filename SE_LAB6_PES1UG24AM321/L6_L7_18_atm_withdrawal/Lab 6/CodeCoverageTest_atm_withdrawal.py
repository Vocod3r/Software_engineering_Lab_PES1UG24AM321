"""
Lab 6 - Code (line) coverage tests for atm_withdrawal.py

Goal: make every LINE of atm_withdrawal.py execute at least once.
Run:
    coverage run --source=. -m pytest CodeCoverageTest_atm_withdrawal.py
    coverage report -m
"""
import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ---------------- withdraw() ----------------

def test_simple_withdrawal():
    # own bank, within limit, enough balance -> no fee
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_unknown_account_type():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "fixed", True)


def test_invalid_amount_zero():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 0, "savings", True)


def test_amount_above_daily_limit():
    assert withdraw(100000, 30000, "savings", True) == "limit exceeded"


def test_other_bank_large_amount_fee():
    # other bank ATM, amount > 10000 -> fee 20 + 10 = 30
    assert withdraw(50000, 20000, "current", False) == 50000 - 20000 - 30


def test_insufficient_funds():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


# ---------------- pin_check() ----------------

def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_card_blocked_after_three_attempts():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_wrong_pin_on_last_attempt_blocks_card():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_wrong_pin_retry():
    assert pin_check(1111, 1234, 0) == "retry"


# ---------------- note_breakup() ----------------

def test_note_breakup_invalid_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(150)


def test_note_breakup_with_200_notes():
    # 1800 = 3x500 + 1x200 + 1x100
    assert note_breakup(1800) == (3, 1, 1)


def test_note_breakup_without_200_notes():
    # 600 = 1x500 + 0x200 + 1x100
    assert note_breakup(600) == (1, 0, 1)
