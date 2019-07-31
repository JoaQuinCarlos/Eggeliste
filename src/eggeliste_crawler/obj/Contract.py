class Contract:

    def __init__(self, contract_level, suit, doubled=False, redoubled=False):
        self.contract_level = contract_level
        self.suit = suit
        self.doubled = doubled
        self.redoubled = redoubled
