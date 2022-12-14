import json

import requests
from pprint import pprint
import arbitrage

# Url for api calls to uniswap graph ql
urlUniswap = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"

def get_uniswap_informations(url):
    # Define query
    query_string = """
    query 
    {
        pairs(
        first: 500,
        orderBy: trackedReserveETH,
        orderDirection: desc
        ) {
            id
            txCount
            token0Price
            token1Price
            token0 {
              id
              symbol
              name
              decimals
            }
            token1 {
              id
              symbol
              name
              decimals
            }
        
        }
    }
    """

    # Graph QL request
    dict_json = requests.post(urlUniswap, json={"query": query_string}).json()
    return dict_json

if __name__ == "__main__":
    # Get data
    pairs = get_uniswap_informations(urlUniswap)
    trading_pairs_list = arbitrage.get_structured_trading_pairs(pairs)

    # Detect opportunities with surface rate calculation
    surface_rates_list = []
    for trading_pairs in trading_pairs_list:
        surface_rate = arbitrage.calc_triangular_arb_surface_rate(trading_pairs, min_rate=0.002)
        if len(surface_rate) > 0:
            surface_rates_list.append(surface_rate)

    # Save opportunities to JSON file
    with open("uniswap_surface_rates.json", "w") as f:
        json.dump(surface_rates_list, f)



