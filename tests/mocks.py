from govsignal.scout import ProcurementScout

class MockScout(ProcurementScout):
    """
    Shared mock for testing Scout logic without loading external config files unless needed.
    """
    def __init__(self):
        self.MAX_PROBABILITY = 0.95
        self.BASE_SCORE = 0.4
        self.config = {}
        self.targets = {}
    
    def _calculate_probability(self, text, keywords):
        # Expose protected method for testing
        return super()._calculate_probability(text, keywords)

    def _generate_signal(self, data, category, probability):
        return super()._generate_signal(data, category, probability)
