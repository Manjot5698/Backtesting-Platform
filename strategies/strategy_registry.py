from .moving_average import MovingAverageStrategy
from .rsi_strategy import RSIStrategy
from .Bollinger_strategy import BollingerStrategy

STRATEGY_REGISTRY ={
    "moving_average": MovingAverageStrategy,
    "rsi": RSIStrategy,
    "bollinger": BollingerStrategy
}