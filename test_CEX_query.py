import time
import hmac
import hashlib
import requests

API_KEY = "Qet0Xqc4b2WnGThHvubqPb7UMqqWGWwsPoyLIvkOEUpORRROV1U5ELyj2wfD6nDX"
SECRET_KEY = "oaKqj4WR4iQVnKPGRVdZEok5haieI9jSOAZ7U9xQ2fNX8GqBOvCPRPTmBVnlMMcB"
BASE_URL = "https://testnet.binance.vision"


def sign(query):
    return hmac.new(
        SECRET_KEY.encode('utf-8'),
        query.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def get_signed(path, params=None):
    params = params or {}
    params["timestamp"] = int(time.time() * 1000)
    params["recvWindow"] = 5000

    query = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = sign(query)

    url = f"{BASE_URL}{path}?{query}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}
    return requests.get(url, headers=headers).json()


# 1. 查单个订单
print("=== 单个订单 ===")
print(get_signed("/api/v3/order", {
    "symbol": "BTCUSDT",
    "orderId": 446288  # 替换成你的 orderId
}))

# 2. 查当前挂单
print("\n=== 当前挂单 ===")
print(get_signed("/api/v3/openOrders", {"symbol": "BTCUSDT"}))

# 3. 查所有历史订单
print("\n=== 历史订单 ===")
print(get_signed("/api/v3/allOrders", {"symbol": "BTCUSDT", "limit": 10}))
