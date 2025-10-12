"""
Calculation Service

This module provides calculation utilities like win rate calculator.
"""

import math
from typing import Dict, Any

from app.core.logging import get_logger

logger = get_logger(__name__)


class CalculationService:
    """Service for various game-related calculations."""
    
    @staticmethod
    def calculate_required_wins(
        current_matches: int,
        current_win_rate: float,
        target_win_rate: float
    ) -> Dict[str, Any]:
        """
        Calculate required consecutive wins to reach target win rate.
        
        Args:
            current_matches: Current number of matches played
            current_win_rate: Current win rate percentage (0-100)
            target_win_rate: Target win rate percentage (0-100)
            
        Returns:
            Dict[str, Any]: Calculation result with required wins
            
        Raises:
            ValueError: If input values are invalid
        """
        # Validate inputs
        if current_matches < 0:
            raise ValueError("Current matches must be non-negative")
        
        if not (0 <= current_win_rate <= 100):
            raise ValueError("Current win rate must be between 0 and 100")
        
        if not (0 < target_win_rate <= 100):
            raise ValueError("Target win rate must be between 0 and 100")
        
        if target_win_rate <= current_win_rate:
            raise ValueError(
                "Target win rate must be greater than current win rate"
            )
        
        # Calculate current wins
        current_wins = current_matches * (current_win_rate / 100.0)
        
        # Calculate required wins
        # Formula: (current_wins + x) / (current_matches + x) = target_win_rate / 100
        # Solving for x: x = (current_wins - current_matches * target_wr) / (target_wr - 1)
        target_ratio = target_win_rate / 100.0
        denominator = target_ratio - 1.0
        
        if denominator == 0:
            raise ValueError(
                f"Cannot reach {target_win_rate}% win rate with finite matches"
            )
        
        numerator = current_wins - current_matches * target_ratio
        required_matches = numerator / denominator
        
        # Round up to get integer number of matches
        required_matches_int = math.ceil(required_matches)
        
        if required_matches_int < 0:
            raise ValueError(
                "Target win rate cannot be achieved with only consecutive wins"
            )
        
        logger.info(
            f"Calculated required wins: {required_matches_int} "
            f"(from {current_matches} matches at {current_win_rate}% "
            f"to {target_win_rate}%)"
        )
        
        return {
            "status": "success",
            "match_now": current_matches,
            "wr_now": current_win_rate,
            "wr_future": target_win_rate,
            "required_no_lose_matches": required_matches_int,
            "message": (
                f"To achieve a win rate of {target_win_rate}%, "
                f"you need {required_matches_int} consecutive wins "
                f"without any losses."
            )
        }


# Singleton instance
_calculation_service: CalculationService | None = None


def get_calculation_service() -> CalculationService:
    """
    Get calculation service singleton instance.
    
    Returns:
        CalculationService: Calculation service instance
    """
    global _calculation_service
    if _calculation_service is None:
        _calculation_service = CalculationService()
    return _calculation_service
