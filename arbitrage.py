from pprint import pprint

def get_structured_trading_pairs(pairs_dict):
    pairs = pairs_dict["data"]["pairs"]
    pair_list = pairs[:100]
    remove_duplicate_list = []
    triangle_pairs = []

    # Loop trough each coin to find matches
    # Get first pair (A)
    for pair_a in pair_list:
        a_contract = pair_a["id"]
        a_base = pair_a["token0"]["symbol"]
        a_quote = pair_a["token1"]["symbol"]
        a_pair = f"{a_base}_{a_quote}"
        a_token_0_id = pair_a["token0"]["id"]
        a_token_1_id = pair_a["token1"]["id"]
        a_token_0_price = pair_a["token0Price"]
        a_token_1_price = pair_a["token1Price"]
        a_token_0_decimals = pair_a["token0"]["decimals"]
        a_token_1_decimals = pair_a["token1"]["decimals"]

        # Put (A) in box for checking (B)
        a_pair_box = [a_base, a_quote]

        # Get pair (B)
        for pair_b in pair_list:
            b_contract = pair_b["id"]
            b_base = pair_b["token0"]["symbol"]
            b_quote = pair_b["token1"]["symbol"]
            b_pair = f"{b_base}_{b_quote}"
            b_token_0_id = pair_b["token0"]["id"]
            b_token_1_id = pair_b["token1"]["id"]
            b_token_0_price = pair_b["token0Price"]
            b_token_1_price = pair_b["token1Price"]
            b_token_0_decimals = pair_b["token0"]["decimals"]
            b_token_1_decimals = pair_b["token1"]["decimals"]

            if b_pair != a_pair and b_base in a_pair_box or b_quote in a_pair_box:
                for pair_c in pair_list:
                    c_contract = pair_c["id"]
                    c_base = pair_c["token0"]["symbol"]
                    c_quote = pair_c["token1"]["symbol"]
                    c_pair = f"{c_base}_{c_quote}"
                    c_token_0_id = pair_c["token0"]["id"]
                    c_token_1_id = pair_c["token1"]["id"]
                    c_token_0_price = pair_c["token0Price"]
                    c_token_1_price = pair_c["token1Price"]
                    c_token_0_decimals = pair_c["token0"]["decimals"]
                    c_token_1_decimals = pair_c["token1"]["decimals"]

                    if c_pair != a_pair and c_pair != b_pair:
                        combine_ab = [a_base, a_quote, b_base, b_quote]
                        if c_base in combine_ab and c_quote in combine_ab:
                            pair_box = [a_pair, b_pair, c_pair]
                            pairs_combinaison = ",".join(pair_box)
                            if pairs_combinaison not in remove_duplicate_list:
                                remove_duplicate_list.append(pairs_combinaison)
                                match_dict = {
                                    "pairs": pair_box,
                                    "aPair": a_pair,
                                    "bPair": b_pair,
                                    "cPair": c_pair,
                                    "aBase": a_base,
                                    "aQuote": a_quote,
                                    "bBase": b_base,
                                    "bQuote": b_quote,
                                    "cBase": c_base,
                                    "cQuote": c_quote,
                                    "aToken0Id" : a_token_0_id,
                                    "aToken1Id" : a_token_1_id,
                                    "bToken0Id": b_token_0_id,
                                    "bToken1Id": b_token_1_id,
                                    "cToken0Id": c_token_0_id,
                                    "cToken1Id": c_token_1_id,
                                    "aToken0Decimals": a_token_0_decimals,
                                    "aToken1Decimals": a_token_1_decimals,
                                    "bToken0Decimals": b_token_0_decimals,
                                    "bToken1Decimals": b_token_1_decimals,
                                    "cToken0Decimals": c_token_0_decimals,
                                    "cToken1Decimals": c_token_1_decimals,
                                    "aToken0Price": a_token_0_price,
                                    "aToken1Price": a_token_1_price,
                                    "bToken0Price": b_token_0_price,
                                    "bToken1Price": b_token_1_price,
                                    "cToken0Price": c_token_0_price,
                                    "cToken1Price": c_token_1_price,
                                    "aContract": a_contract,
                                    "bContract": b_contract,
                                    "cContract": c_contract,
                                }
                                triangle_pairs.append(match_dict)
    return triangle_pairs

# Calculate surface rate to spot potential opportunities
def calc_triangular_arb_surface_rate(pairs):
    print(pairs["pairs"])
    surface_dict = {}
    