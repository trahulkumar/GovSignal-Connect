"""
GovSignal Connectors Module
Mocks external government APIs (SAM.gov, Federal Register) for the research prototype.
"""
import logging

logger = logging.getLogger(__name__)

class SamGovConnector:
    """
    Mock connector for SAM.gov (System for Award Management).
    Simulates fetching government contract solicitations.
    """
    def __init__(self):
        logger.info("Initializing SamGovConnector (Mock Mode) - Prototype v1.0")

    def get_opportunities(self, keywords: list) -> list[dict]:
        """
        Simulates an API call to SAM.gov to find solicitations matching keywords.
        In this research prototype, we return a fixed mock response associated with Defense/Electronic Warfare.
        """
        logger.info(f"Querying SAM.gov with keywords: {keywords}")
        
        # Mock Data 2 (Defense) as per requirements
        # NOTE: This structure mimics the official SAM.gov API "opportunities" endpoint
        mock_response = [
            {
                "noticeId": "N00014-24-R-0001",
                "title": "DoD Solicitation: Electronic Warfare Readiness and Countermeasures",
                "department": "Department of Defense",
                "subTier": "Department of the Navy",
                "description": "The Office of Naval Research is soliciting proposals for advanced Electronic Warfare (EW) systems. Key areas of interest include next-generation jamming pods and high-power microwave integration for airborne platforms.",
                "type": "Solicitation",
                "postedDate": "2023-10-25",
                "archiveDate": "2024-01-25"
            }
        ]
        return mock_response

class FederalRegisterConnector:
    """
    Mock connector for the Federal Register API.
    Simulates fetching government notices and funding opportunities.
    """
    def __init__(self):
        logger.info("Initializing FederalRegisterConnector (Mock Mode) - Prototype v1.0")

    def get_documents(self, keywords: list) -> list[dict]:
        """
        Simulates an API call to Federal Register.
        In this research prototype, we return a fixed mock response associated with CHIPS Act/Semiconductors.
        """
        logger.info(f"Querying Federal Register with keywords: {keywords}")

        # Mock Data 1 (Semiconductor) as per requirements
        mock_response = [
            {
                "document_number": "2023-28912",
                "title": "CHIPS Act Funding Opportunity: Expansion of Domestic Nanofabrication Facilities",
                "agency": "Department of Commerce",
                "abstract": "The NIST is announcing a $5M grant program to support the construction and modernization of nanofabrication facilities. Priority will be given to proposals enhancing domestic capacity for high-vacuum processing and advanced lithography.",
                "publication_date": "2023-11-15",
                "type": "Notice of Funding Opportunity"
            }
        ]
        return mock_response
