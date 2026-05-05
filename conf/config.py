"""
Binance Testnet API Configuration
"""
import os


class Config:
    # Binance Testnet API Base URLs
    BASE_URL = "https://testnet.binance.vision"
    API_URL = "https://testnet.binance.vision/api"
    Futures_URL = "https://testnet.binance.vision/fapi"
    WEBSOCKET_URL = "wss://testnet.binance.vision/ws"

    # API Keys (Get from: https://testnet.binance.vision/)
    API_KEY = os.getenv("BINANCE_API_KEY", "Qet0Xqc4b2WnGThHvubqPb7UMqqWGWwsPoyLIvkOEUpORRROV1U5ELyj2wfD6nDX")
    SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "oaKqj4WR4iQVnKPGRVdZEok5haieI9jSOAZ7U9xQ2fNX8GqBOvCPRPTmBVnlMMcB")

    # Request timeout
    TIMEOUT = 30

    # Enable testnet mode (no actual trades)
    TESTNET = True

    # Logging level
    LOG_LEVEL = "INFO"

    # Test report settings
    REPORT_DIR = "../reports"
    REPORT_FORMAT = "html"
