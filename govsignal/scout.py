import json
import logging
import yaml
from datetime import datetime
from .connectors import SamGovConnector, FederalRegisterConnector

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GovSignal.Scout")

class ProcurementScout:
    """
    Strategic Procurement Agent (The Scout).
    Reads unstructured government data and converts it into structured JSON signals
    for legacy ERP ingestion.
    """

    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.sam_connector = SamGovConnector()
        self.fr_connector = FederalRegisterConnector()
        
        # Load surveillance targets from config
        self.targets = self.config.get('surveillance_targets', {})
        logger.info(f"Scout initialized with targets: {list(self.targets.keys())}")

    def _load_config(self, path: str) -> dict:
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    def _calculate_probability(self, text: str, target_keywords: list) -> float:
        """
        Simulates NLP demand probability scoring based on keyword density and presence.
        Returns a float between 0.0 and 1.0.
        """
        text_lower = text.lower()
        match_count = 0
        for kw in target_keywords:
            if kw.lower() in text_lower:
                match_count += 1
        
        # Simple heuristic: more matches = higher probability
        # Base score 0.4, +0.2 per keyword match, capped at 0.95
        if match_count == 0:
            return 0.1
        
        score = 0.4 + (match_count * 0.2)
        return min(score, 0.95)

    def _generate_signal(self, source_data: dict, target_category: str, probability: float) -> dict:
        """
        Generates the standardized JSON signal for ERP ingestion.
        """
        # Determine specific asset and action based on the target category
        # In a real system, this would be a more complex mapping or AI inference
        target_info = self.targets.get(target_category, {})
        asset_name = target_info.get('related_asset', 'Unknown Asset')
        
        # Logic to determine action based on probability
        if probability >= 0.8:
            action = "release_capital_hold"
        elif probability > 0.5:
            action = "flag_for_review"
        else:
            action = "monitor"

        signal = {
            "signal_id": f"SIG-{int(datetime.now().timestamp())}-{target_category[:3].upper()}",
            "timestamp": datetime.now().isoformat(),
            "source": source_data.get('source_name', 'Government Feed'),
            "detected_event": source_data.get('title', 'Unknown Event'),
            "demand_probability": round(probability, 2),
            "asset_implication": asset_name,
            "erp_action_recommendation": action,
            "raw_snippet": source_data.get('description', source_data.get('abstract', ''))[:200] + "..."
        }
        return signal

    def run(self):
        """
        Main execution loop.
        1. Fetch data from connectors.
        2. Analyze against targets.
        3. Emit signals.
        """
        logger.info("Starting Scout surveillance cycle...")
        all_signals = []

        # 1. Process SAM.gov Data (Defense Use Case)
        # We look for "Defense" related keywords defined in config logic, 
        # but for this prototype we iterate our known targets.
        
        for category, criteria in self.targets.items():
            keywords = criteria.get('keywords', [])
            
            # Query Connectors (In a real app, we'd optimize these calls)
            sam_opportunities = self.sam_connector.get_opportunities(keywords)
            fr_documents = self.fr_connector.get_documents(keywords)

            # Analyze SAM data
            for item in sam_opportunities:
                # Mocking a match check - normally we'd check if the item ACTUALLY matches the category
                # For the prototype, we assume the connector returned relevant data for the "Defense" case
                description_lower = item.get('description', '').lower()
                if category == "Defense_Systems" and "jamming" in description_lower:
                    item['source_name'] = "SAM.gov"
                    prob = self._calculate_probability(item['description'], keywords)
                    signal = self._generate_signal(item, category, prob)
                    all_signals.append(signal)

            # Analyze Federal Register data
            for item in fr_documents:
                # Similarly, check for semiconductor match
                abstract_lower = item.get('abstract', '').lower()
                if category == "Semiconductors" and "nanofabrication" in abstract_lower:
                    item['source_name'] = "Federal Register"
                    prob = self._calculate_probability(item['abstract'], keywords)
                    signal = self._generate_signal(item, category, prob)
                    all_signals.append(signal)

        # Output results
        print(json.dumps(all_signals, indent=2))
        logger.info(f"Surveillance cycle complete. Generated {len(all_signals)} signals.")

if __name__ == "__main__":
    # If run directly
    import sys
    config_file = sys.argv[1] if len(sys.argv) > 1 else "examples/config.yaml"
    scout = ProcurementScout(config_file)
    scout.run()
