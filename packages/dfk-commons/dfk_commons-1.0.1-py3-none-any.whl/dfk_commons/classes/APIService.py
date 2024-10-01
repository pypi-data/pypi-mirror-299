import requests
from dfk_commons.classes.Token import Token


class APIService:
    def __init__(self, url, api_key, chain):
        self.url = url
        self.tokens = self.getTokens(chain)
        self.contracts = self.getContracts(chain)
        self.pairs = self.getPairs("Jewel", chain)

        self.headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        }

    def getTokens(self, chain):
        response = requests.get(f"{self.url}/dfk/tokens", headers=self.headers,  params={"chain": chain})
        response_json = response.json()
        tokens = {}
        for token in response_json:
            tokens[token] = Token(token, chain, response_json[token]["address"], response_json[token]["decimals"], None)
        return tokens

    def getPairs(self, base_token, chain):
        response = requests.get(f"{self.url}/dfk/pairs", headers=self.headers, params={"token": base_token, "chain": chain})
        return response.json()
    
    def getContracts(self, chain):
        response = requests.get(f"{self.url}/dfk/contracts", headers=self.headers, params={"chain": chain})
        return response.json()
    