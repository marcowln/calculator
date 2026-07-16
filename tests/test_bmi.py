import pytest

from bmi import calculate_bmi, classify_bmi


def test_calculate_bmi() -> None:
    result = calculate_bmi(80, 1.80)

    assert result == pytest.approx(24.691358, rel=1e-5)


def test_classify_normal_weight() -> None:
    assert classify_bmi(22.0) == "Normalgewicht"


def test_classify_overweight() -> None:
    assert classify_bmi(27.0) == "Übergewicht"


def test_rejects_negative_weight() -> None:
    with pytest.raises(ValueError):
        calculate_bmi(-80, 1.80)


def test_rejects_zero_height() -> None:
    with pytest.raises(ValueError):
        calculate_bmi(80, 0)