"""
Binance API Client Module
"""
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from conf.config import Config


class BinanceClient:
    """Binance Testnet API Client"""

    def __init__(self, api_key=None, secret_key=None):
        self.api_key = api_key or Config.API_KEY
        self.secret_key = secret_key or Config.SECRET_KEY
        self.base_url = Config.API_URL
        self.futures_url = Config.Futures_URL
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _generate_signature(self, params):
        """Generate HMAC SHA256 signature"""
        query_string = urlencode(params)
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _request(self, method, endpoint, signed=False, **kwargs):
        """Send API request"""
        url = f"{self.base_url}{endpoint}"
        params = kwargs.get("params", {})
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._generate_signature(params)

        kwargs["params"] = params

        try:
            response = self.session.request(method, url, timeout=Config.TIMEOUT, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(response, "status_code", None)}

    def _futures_request(self, method, endpoint, signed=False, **kwargs):
        """Send Futures API request"""
        url = f"{self.futures_url}{endpoint}"
        params = kwargs.get("params", {})

        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._generate_signature(params)

        kwargs["params"] = params

        try:
            response = self.session.request(method, url, timeout=Config.TIMEOUT, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(response, "status_code", None)}

    # ==================== Spot API ====================

    def ping(self):
        """Test connectivity"""
        return self._request("GET", "/v3/ping")


    def get_server_time(self):
        """Get server time"""
        return self._request("GET", "/v3/time")

    def get_exchange_info(self):
        """Get exchange info"""
        return self._request("GET", "/v3/exchangeInfo")

    def get_symbol_price(self, symbol):
        """Get symbol price ticker"""
        return self._request("GET", "/v3/ticker/price", params={"symbol": symbol})

    def get_order_book(self, symbol, limit=100):
        """Get order book"""
        return self._request("GET", "/v3/depth", params={"symbol": symbol, "limit": limit})

    def get_recent_trades(self, symbol, limit=100):
        """Get recent trades"""
        return self._request("GET", "/v3/trades", params={"symbol": symbol, "limit": limit})

    def get_klines(self, symbol, interval, limit=500):
        """Get candlestick/kline data"""
        return self._request("GET", "/v3/klines", params={
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        })

    def get_24hr_ticker(self, symbol=None):
        """Get 24hr ticker price change statistics"""
        params = {"symbol": symbol} if symbol else {}
        return self._request("GET", "/v3/ticker/24hr", params=params)

    def create_test_order(self, symbol, side, order_type, **kwargs):
        """Create a test order (no actual execution)"""
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            **kwargs
        }
        return self._request("POST", "/v3/order/test", signed=True, params=params)

    def get_account(self):
        """Get account info"""
        return self._request("GET", "/v3/account", signed=True)

    def get_open_orders(self, symbol=None):
        """Get current open orders"""
        params = {"symbol": symbol} if symbol else {}
        return self._request("GET", "/v3/openOrders", signed=True, params=params)

    # ==================== Futures API ====================

    def futures_ping(self):
        """Futures test connectivity"""
        return self._futures_request("GET", "/v1/ping")

    def futures_account(self):
        """Get futures account info"""
        return self._futures_request("GET", "/v2/account", signed=True)

    def futures_balance(self):
        """Get futures account balance"""
        return self._futures_request("GET", "/v2/balance", signed=True)

    def futures_place_order(self, symbol, side, order_type, quantity, **kwargs):
        """Place futures order"""
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            **kwargs
        }
        return self._futures_request("POST", "/v1/order", signed=True, params=params)

    def futures_get_positions(self):
        """Get futures positions"""
        return self._futures_request("GET", "/v2/positionRisk", signed=True)

    def futures_get_klines(self, symbol, interval, limit=500):
        """Get futures candlestick data"""
        return self._futures_request("GET", "/v1/klines", params={
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        })
