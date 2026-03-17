from .moving_average import MovingAverageStrategy
from .rsi_strategy import RSIStrategy

STRATEGY_REGISTRY ={
    "moving_average": MovingAverageStrategy,
    "rsi": RSIStrategy
}