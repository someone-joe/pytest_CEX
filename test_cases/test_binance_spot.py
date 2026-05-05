"""
Test Cases for Binance Spot API
"""
import pytest
from binance_api import BinanceClient


class TestBinanceSpotAPI:
    """Test cases for Binance Spot API"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = BinanceClient()
        self.test_symbol = "BTCUSDT"

    def test_ping(self):
        """Test connectivity"""
        response = self.client.ping()
        assert "error" not in response or response.get("error") is None

    def test_get_server_time(self):
        """Test server time"""
        response = self.client.get_server_time()
        assert "serverTime" in response
        assert isinstance(response["serverTime"], int)

    def test_get_exchange_info(self):
        """Test exchange info"""
        response = self.client.get_exchange_info()
        assert "symbols" in response
        assert len(response["symbols"]) > 0

    def test_get_symbol_price(self):
        """Test symbol price"""
        response = self.client.get_symbol_price(self.test_symbol)
        assert "symbol" in response
        assert response["symbol"] == self.test_symbol
        assert "price" in response

    def test_get_order_book(self):
        """Test order book"""
        response = self.client.get_order_book(self.test_symbol, limit=10)
        assert "bids" in response
        assert "asks" in response
        assert len(response["bids"]) <= 10
        assert len(response["asks"]) <= 10

    def test_get_recent_trades(self):
        """Test recent trades"""
        response = self.client.get_recent_trades(self.test_symbol, limit=5)
        assert isinstance(response, list)
        assert len(response) <= 5

    def test_get_klines(self):
        """Test candlestick data"""
        response = self.client.get_klines(self.test_symbol, "1h", limit=10)
        assert isinstance(response, list)
        assert len(response) <= 10

    def test_get_24hr_ticker(self):
        """Test 24hr ticker"""
        response = self.client.get_24hr_ticker(self.test_symbol)
        assert "symbol" in response
        assert "priceChange" in response
        assert "volume" in response

    def test_get_all_24hr_tickers(self):
        """Test all 24hr tickers"""
        response = self.client.get_24hr_ticker()
        assert isinstance(response, list)
        assert len(response) > 0

    def test_get_account(self):
        """Test account info"""
        response = self.client.get_account()
        if "error" in response:
            pytest.skip(f"API Key not configured: {response.get('error')}")
        assert "balances" in response

    def test_get_open_orders(self):
        """Test open orders"""
        response = self.client.get_open_orders(symbol=self.test_symbol)
        if "error" in response:
            pytest.skip(f"API Key not configured: {response.get('error')}")
        assert isinstance(response, list)

    def test_create_test_order(self):
        """Test order creation (test mode)"""
        response = self.client.create_test_order(
            symbol=self.test_symbol,
            side="BUY",
            order_type="LIMIT",
            quantity="0.001",
            price="50000",
            timeInForce="GTC"
        )
        if "error" in response:
            pytest.skip(f"API Key not configured: {response.get('error')}")
        assert response == {}


class TestBinanceFuturesAPI():
    """Test cases for Binance Futures API"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = BinanceClient()
        self.test_symbol = "BTCUSDT"

    def test_futures_ping(self):
        """Test futures connectivity"""
        response = self.client.futures_ping()
        assert "error" not in response or response.get("error") is None

    def test_futures_balance(self):
        """Test futures balance"""
        response = self.client.futures_balance()
        if "error" in response:
            pytest.skip(f"API Key not configured: {response.get('error')}")
        assert isinstance(response, list)

    def test_futures_account(self):
        """Test futures account"""
        response = self.client.futures_account()
        if "error" in response:
            pytest.skip(f"API Key not configured: {response.get('error')}")
        assert "totalMarginBalance" in response or "assets" in response

    def test_futures_positions(self):
        """Test futures positions"""
        response = self.client.futures_get_positions()
        if "error" in response:
            pytest.skip(f"API Key not configured: {response.get('error')}")
        assert isinstance(response, list)

    def test_futures_klines(self):
        """Test futures candlestick data"""
        response = self.client.futures_get_klines(self.test_symbol, "1h", limit=5)
        if "error" in response:
            pytest.skip(f"API Key not configured: {response.get('error')}")
        assert isinstance(response, list)
