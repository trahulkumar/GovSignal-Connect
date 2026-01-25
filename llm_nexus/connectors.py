import json
import random

class SamGovConnector:
    """
    Connector for US Government System for Award Management (SAM).
    Retrieves contract opportunities.
    """
    def __init__(self, api_key="DEMO_KEY"):
        self.api_key = api_key
        self.base_url = "https://api.sam.gov/opportunities/v2/search"

    def fetch_opportunities(self, naics_code: str, mock=True):
        """
        Fetches active opportunities for a given NAICS code (e.g., 334413 for Semi/Solar).
        """
        if mock:
            return self._mock_response(naics_code)
        else:
            # Implementation for real API call would go here
            # response = requests.get(...)
            raise NotImplementedError("Real API connection requires valid credentials.")

    def _mock_response(self, naics_code):
        """
        Generates realistic JSON response mimicking SAM.gov API.
        """
        # Synthetic opportunities
        titles = [
            "Advanced Semiconductor Packaging Research",
            "Supply of Ruggedized Field Laptops",
            "Next-Gen Battery Storage Prototype",
            "Cloud Infrastructure Support Services"
        ]
        
        opportunities = []
        for _ in range(random.randint(2, 5)):
            title = random.choice(titles)
            opp_id = f"NOTICE-{random.randint(10000, 99999)}"
            
            opp = {
                "noticeId": opp_id,
                "title": title,
                "solicitationNumber": f"SOL-{random.randint(100, 999)}",
                "organizationHierarchy": {
                    "level": "DEPARTMENT",
                    "name": "Department of Defense"
                },
                "naicsCode": naics_code,
                "type": "Presolicitation",
                "postedDate": "2025-10-15",
                "responseDeadLine": "2025-12-01",
                "uiLink": f"https://sam.gov/opp/{opp_id}/view"
            }
            opportunities.append(opp)
            
        return {
            "totalRecords": len(opportunities),
            "opportunitiesData": opportunities
        }

if __name__ == "__main__":
    connector = SamGovConnector()
    data = connector.fetch_opportunities("334413")
    print(json.dumps(data, indent=2))
