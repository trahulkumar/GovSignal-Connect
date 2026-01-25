import random

class SentimentEngine:
    """
    Analyzes unstructured text to produce a Risk Score (0.0 - 1.0).
    In production, this would use a Transformer (BERT/RoBERTa).
    """
    def __init__(self, model_name="mock-transformer"):
        self.model_name = model_name

    def analyze_risk(self, text):
        """
        Returns a float between 0.0 (Safe) and 1.0 (Critical Risk).
        """
        # Mock Logic based on keywords
        text_lower = text.lower()
        
        if any(w in text_lower for w in ["blockade", "war", "cyberattack", "sanction", "embargo", "floods", "strike"]):
            # High Risk
            base_score = 0.8
        elif any(w in text_lower for w in ["delay", "inflation", "tariff", "review"]):
            # Medium Risk
            base_score = 0.5
        else:
            # Low Risk
            base_score = 0.1
            
        # Add noise to simulate model uncertainty
        noise = random.uniform(-0.05, 0.05)
        final_score = max(0.0, min(1.0, base_score + noise))
        
        return final_score

    def update_volatility_index(self, signals, current_volatility):
        """
        Aggregates risk scores from multiple signals to update the global volatility index.
        """
        if not signals:
            return current_volatility
            
        risk_scores = [self.analyze_risk(s['content']) for s in signals]
        avg_risk = sum(risk_scores) / len(risk_scores)
        
        # Logic: If avg_risk is high (>0.7), trigger a volatility spike
        if avg_risk > 0.7:
            # Significant spike
            new_volatility = min(1.0, current_volatility + 0.4)
        elif avg_risk > 0.4:
            # Moderate increase
            new_volatility = min(1.0, current_volatility + 0.1)
        else:
            # Calm period, decay volatility
            new_volatility = max(0.0, current_volatility * 0.9)
            
        return new_volatility
