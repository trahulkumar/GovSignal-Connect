"""
GovSignal Local Connectors Module
Mocks data from State, Local, and Non-Profit sources for deeper supply chain signals.
"""
import logging
from .connectors import ConnectorResponse

logger = logging.getLogger(__name__)

# Base class or common util could go here, but for prototype we'll keep classes independent.

class CaliforniaGoBizConnector:
    """
    Mock connector for California Governor's Office of Business and Economic Development.
    Target: Semiconductor grants.
    """
    def get_opportunities(self, keywords: list) -> ConnectorResponse:
        logger.info("Querying CA GO-Biz")
        return [{
            "source": "CA GO-Biz",
            "title": "California Competes Tax Credit - Semiconductor Focus",
            "description": "Tax credits available for semiconductor manufacturing equipment upgrades in Silicon Valley.",
            "url": "https://business.ca.gov/"
        }]

class TexasEnterpriseFundConnector:
    """
    Mock connector for Texas Enterprise Fund.
    Target: Defense manufacturing.
    """
    def get_opportunities(self, keywords: list) -> ConnectorResponse:
        logger.info("Querying Texas TEF")
        return [{
            "source": "Texas TEF",
            "title": "Defense Supply Chain Resilience Grant",
            "description": "Funding for manufacturers of critical defense components in the Dallas-Fort Worth metroplex.",
            "url": "https://gov.texas.gov/business/page/texas-enterprise-fund"
        }]

class NewYorkEmpireStateConnector:
    """
    Mock connector for New York Empire State Development.
    Target: GlobalFoundries/Semiconductors.
    """
    def get_opportunities(self, keywords: list) -> ConnectorResponse:
        logger.info("Querying NY ESD")
        return [{
            "source": "NY ESD",
            "title": "Green CHIPS Community Investment Fund",
            "description": "Grant opportunities for sustainable semiconductor manufacturing in Upstate New York.",
            "url": "https://esd.ny.gov/green-chips"
        }]
