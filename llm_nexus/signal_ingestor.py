import random
import time

class SignalIngestor:
    """
    Ingests and parses geopolitical signals from External Feeds.
    Mocks a connection to Defense.gov RSS.
    """
    def __init__(self, source="defense.gov"):
        self.source = source
        self.synthetic_headlines = [
            ("DoD announces blockade in Strait of Hormuz", "HIGH"),
            ("New trade deal signed with key semiconductor partner", "LOW"),
            ("Minor delays expected at Port of LA due to labor", "MEDIUM"),
            ("Executive Order 14017 Implementation Update", "LOW"),
            ("Flash floods in Taiwan impact wafer output", "HIGH"),
            ("Cyberattack on Colonial Pipeline infrastructure", "HIGH"),
            ("Routine maintenance scheduled for naval base", "LOW"),
            ("Diplomatic talks yield positive results", "LOW")
        ]

    def fetch_latest_signals(self):
        """
        Simulates fetching live data.
        Returns a list of dictionaries with content and timestamp.
        """
        # Randomly select a few headlines to simulate a 'batch'
        num_signals = random.randint(1, 3)
        selection = random.sample(self.synthetic_headlines, num_signals)
        
        signals = []
        for text, risk_label in selection:
            signals.append({
                "source": self.source,
                "timestamp": time.time(),
                "content": text,
                "ground_truth_risk": risk_label # Specific to this mock for validation
            })
            
        return signals

if __name__ == "__main__":
    ingestor = SignalIngestor()
    print(ingestor.fetch_latest_signals())
