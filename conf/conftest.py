"""
Test Report Configuration
"""
import os
from config import Config


def pytest_configure(config):
    """Configure pytest"""
    os.makedirs(Config.REPORT_DIR, exist_ok=True)


def pytest_html_report_title(report):
    """Custom HTML report title"""
    report.title = "Binance Testnet API Automation Report"
