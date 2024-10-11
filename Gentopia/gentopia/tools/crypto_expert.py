from typing import AnyStr, Optional, Type, Any
from gentopia.tools.basetool import BaseTool, BaseModel, Field
import requests
import json
import datetime

class CryptoExpertArgs(BaseModel):
    action: str = Field(..., description="The action to perform: data, history, list, map, exchange, list_exchanges.")
    symbol: Optional[str] = Field(None, description="The cryptocurrency symbol (e.g., BTC).")
    start: Optional[str] = Field(None, description="Start date for historical data in timestamp.")
    end: Optional[str] = Field(str(int(datetime.datetime.now().timestamp() * 1000)), description="End date for historical data in timestamp.")
    symbols: Optional[str] = Field(None, description="Comma-separated list of cryptocurrency symbols.")
    exchange_id: Optional[str] = Field(None, description="The exchange ID for fetching exchange data.")
    sort: Optional[str] = Field("rank", description="Sort parameter for listing coins.")
    order: Optional[str] = Field("ascending", description="Order for sorting (ascending or descending).")
    offset: Optional[int] = Field(0, description="Offset for listing coins.")
    limit: Optional[int] = Field(50, description="Limit for listing coins.")
    meta: Optional[bool] = Field(True, description="Include metadata in the results.")
    currency: Optional[str] = Field("USD", description="Currency for listing coins or conversions. Default is USD.")


class CryptoExpert(BaseTool):
    """Tool that interacts with the Livecoinwatch API for cryptocurrency data."""

    name = "crypto_expert"
    #description = ("Welcome!! I am a crypto agent."
    #                "I can guide you in your crypto investments!"
    #                "I get my data from livecoinwatch public API."
    #                "I can make about 10,000 free requests per day, which may sound alot, but sometimes it isnt."
    #                "Bear with me as I might run out of my free api requests.")

    description = ("Tool to fetch real-time crypto-currency related data."
                   "Tool provides focus information related to crypto currency")

    args_schema: Optional[Type[BaseModel]] = CryptoExpertArgs

    api_key: str = "bc51fc9a-0a0a-45b2-8fd1-655edf8fdbd9"   # I am not aware of anyother way to pass API key
                                                            # It shouldn't matter as it is a free account, I will eventually get rid of it. 
    base_url: str = "https://api.livecoinwatch.com"

    print("Inside crypto expert class")

    def _make_request(self, endpoint: str, payload: dict) -> dict:
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get('error', 'Failed to fetch data')}

    def _run(self, action: str, symbol: Optional[str] = None, start: Optional[str] = None,
         end: Optional[str] = None, symbols: Optional[str] = None, exchange_id: Optional[str] = None,
         currency: str = "USD", sort: str = "rank", order: str = "ascending", 
         offset: int = 0, limit: int = 50, meta: bool = True):


        if action == "data" and symbol:
            payload = {"currency": currency, "code": symbol, "meta": True}
            response = self._make_request("coins/single", payload)
            #return f"Crypto {symbol}: \nPrice: {response.get('rate')}\nMarket Cap: {response.get('cap')}\n" if "error" not in response else response["error"]

        elif action == "history" and symbol and start and end:
            payload = {"currency": currency, "code": symbol, "start": start, "end": end}
            response = self._make_request("coins/single/history", payload)
            #return response

        elif action == "list":
            payload = {"currency": currency, "sort": sort, "order": order, "offset": offset, "limit": limit, "meta": meta}
            response = self._make_request("coins/list", payload)
            #return response

        elif action == "map" and symbols:
            symbols_list = symbols.split(",")
            payload = {"currency": currency, "codes": symbols_list, "sort": sort, "order": order, "offset": offset, "limit": limit, "meta": meta}
            response = self._make_request("coins/map", payload)
            #return response

        elif action == "exchange" and exchange_id:
            payload = {"currency":currency,"id": exchange_id, "meta": meta}
            response = self._make_request("exchanges/single", payload)
            #return response

        elif action == "list_exchanges":
            payload = {"currency":currency, "sort": "volume", "order": order, "offset": offset, "limit": limit, "meta": meta}
            response = self._make_request("exchanges/list", payload)
            #return response

        else:
            return "Invalid action or missing parameters."

        return json.dumps(response, indent=4)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    crypto_expert = CryptoExpert()

    action = "data"
    symbol = "BTC"
    result = crypto_expert._run(action, symbol=symbol)
    print(result)
