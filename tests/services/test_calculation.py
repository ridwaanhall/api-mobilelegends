"""
Test Calculation Service

Tests for win rate calculation service.
"""

import pytest
from app.services import get_calculation_service


def test_calculate_required_wins_success():
    """Test successful win rate calculation."""
    service = get_calculation_service()
    
    result = service.calculate_required_wins(
        current_matches=100,
        current_win_rate=50.0,
        target_win_rate=75.0
    )
    
    assert result["status"] == "success"
    assert result["match_now"] == 100
    assert result["wr_now"] == 50.0
    assert result["wr_future"] == 75.0
    assert result["required_no_lose_matches"] > 0
    assert "message" in result


def test_calculate_required_wins_invalid_current_matches():
    """Test calculation with negative current matches."""
    service = get_calculation_service()
    
    with pytest.raises(ValueError, match="non-negative"):
        service.calculate_required_wins(
            current_matches=-10,
            current_win_rate=50.0,
            target_win_rate=75.0
        )


def test_calculate_required_wins_invalid_win_rates():
    """Test calculation with invalid win rates."""
    service = get_calculation_service()
    
    with pytest.raises(ValueError, match="between 0 and 100"):
        service.calculate_required_wins(
            current_matches=100,
            current_win_rate=150.0,  # Invalid
            target_win_rate=75.0
        )


def test_calculate_required_wins_target_lower_than_current():
    """Test calculation with target lower than current."""
    service = get_calculation_service()
    
    with pytest.raises(ValueError, match="greater than"):
        service.calculate_required_wins(
            current_matches=100,
            current_win_rate=75.0,
            target_win_rate=50.0  # Lower than current
        )


def test_calculate_required_wins_edge_case():
    """Test calculation edge case with 0 matches."""
    service = get_calculation_service()
    
    result = service.calculate_required_wins(
        current_matches=0,
        current_win_rate=0.0,
        target_win_rate=50.0
    )
    
    assert result["status"] == "success"
    assert result["required_no_lose_matches"] == 0
