import requests
from pprint import pprint

# Url for api calls to uniswap graph ql
urlUniswap = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"

# Define query
query_string = """
query {
    pairs {
        id
    }
}
"""

req = requests.post(urlUniswap, json={"query": query_string}).json()
pprint(req)