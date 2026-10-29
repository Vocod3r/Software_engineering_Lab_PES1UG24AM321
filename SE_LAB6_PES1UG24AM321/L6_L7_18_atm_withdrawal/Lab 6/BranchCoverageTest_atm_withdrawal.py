"""
Lab 6 - Branch coverage tests for atm_withdrawal.py

Goal: make every decision (if / or) in atm_withdrawal.py evaluate to BOTH
True and False, plus boundary / edge cases.
Run:
    coverage run --branch --source=. -m pytest BranchCoverageTest_atm_withdrawal.py
    coverage report -m
"""
import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ======================= withdraw() =======================

# --- if account_type not in DAILY_LIMIT ---
@pytest.mark.parametrize("account_type", ["fixed", "SAVINGS", "", None])
def test_unknown_account_type_raises(account_type):
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, account_type, True)


@pytest.mark.parametrize("account_type", ["savings", "current"])
def test_known_account_types_accepted(account_type):
    assert withdraw(5000, 1000, account_type, True) == 4000


# --- if amount <= 0 or amount % 100 != 0 ---
@pytest.mark.parametrize("amount", [0, -100, 150, 1050, 99])
def test_invalid_amounts_raise(amount):
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, amount, "savings", True)


def test_smallest_valid_amount():
    assert withdraw(5000, 100, "savings", True) == 4900


# --- if amount > DAILY_LIMIT[account_type] ---
def test_savings_limit_exceeded():
    assert withdraw(100000, 25100, "savings", True) == "limit exceeded"


def test_current_limit_exceeded():
    assert withdraw(100000, 50100, "current", True) == "limit exceeded"


def test_savings_exactly_at_limit_allowed():
    assert withdraw(100000, 25000, "savings", True) == 75000


def test_current_exactly_at_limit_allowed():
    assert withdraw(100000, 50000, "current", True) == 50000


# --- if not own_bank  /  if amount > 10000 ---
def test_own_bank_no_fee():
    assert withdraw(20000, 15000, "savings", True) == 5000


def test_other_bank_small_amount_fee_20():
    assert withdraw(5000, 1000, "savings", False) == 5000 - 1000 - 20


def test_other_bank_exactly_10000_fee_20():
    # boundary: 10000 is NOT > 10000, so only the base fee applies
    assert withdraw(20000, 10000, "savings", False) == 20000 - 10000 - 20


def test_other_bank_large_amount_fee_30():
    assert withdraw(20000, 10100, "savings", False) == 20000 - 10100 - 30


# --- if amount + fee > balance ---
def test_insufficient_funds_own_bank():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


def test_insufficient_funds_because_of_fee():
    # amount alone fits, but amount + fee does not
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"


def test_balance_exactly_covers_amount_and_fee():
    assert withdraw(1020, 1000, "savings", False) == 0


def test_balance_exactly_covers_amount_own_bank():
    assert withdraw(1000, 1000, "current", True) == 0


# ======================= pin_check() =======================

# --- if attempts >= 3 ---
@pytest.mark.parametrize("attempts", [3, 4, 10])
def test_blocked_when_attempts_reached(attempts):
    # blocked even if the PIN is correct
    assert pin_check(1234, 1234, attempts) == "card blocked"


# --- if entered == actual ---
@pytest.mark.parametrize("attempts", [0, 1, 2])
def test_correct_pin_before_block(attempts):
    assert pin_check(1234, 1234, attempts) == "ok"


# --- if attempts == 2 ---
def test_wrong_pin_third_try_blocks_card():
    assert pin_check(1111, 1234, 2) == "card blocked"


@pytest.mark.parametrize("attempts", [0, 1])
def test_wrong_pin_can_retry(attempts):
    assert pin_check(1111, 1234, attempts) == "retry"


# ======================= note_breakup() =======================

# --- if amount % 100 != 0 ---
@pytest.mark.parametrize("amount", [50, 150, 1999])
def test_note_breakup_invalid(amount):
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(amount)


# --- if remaining >= 200 ---
@pytest.mark.parametrize("amount, expected", [
    (200, (0, 1, 0)),     # exactly 200 remaining -> boundary
    (300, (0, 1, 1)),
    (400, (0, 2, 0)),
    (1800, (3, 1, 1)),
    (2900, (5, 2, 0)),
])
def test_note_breakup_uses_200_notes(amount, expected):
    assert note_breakup(amount) == expected


@pytest.mark.parametrize("amount, expected", [
    (0, (0, 0, 0)),
    (100, (0, 0, 1)),
    (500, (1, 0, 0)),
    (600, (1, 0, 1)),
    (2500, (5, 0, 0)),
])
def test_note_breakup_no_200_notes(amount, expected):
    assert note_breakup(amount) == expected


def test_note_breakup_total_matches_amount():
    for amount in range(0, 10001, 100):
        n500, n200, n100 = note_breakup(amount)
        assert n500 * 500 + n200 * 200 + n100 * 100 == amount
