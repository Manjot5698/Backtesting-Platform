import pandas as pd
from strategies.base_strategy import BaseStrategy

class BollingerStrategy(BaseStrategy):
    def __init__(self,window = 20):