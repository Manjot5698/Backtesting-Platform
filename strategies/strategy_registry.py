from .moving_average import MovingAverageStrategy
from .rsi_strategy import RSIStrategy
from .Bollinger_strategy import BollingerStrategy

STRATEGY_REGISTRY = {
    "moving_average": MovingAverageStrategy,
    "rsi": RSIStrategy,
    "bollinger": BollingerStrategy
}

def get_strategy(name: str):
    if name not in STRATEGY_REGISTRY:
        raise ValueError(f"Strategy '{name}' not found")

    return STRATEGY_REGISTRY[name]