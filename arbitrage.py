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
def calc_triangular_arb_surface_rate(t_group, min_rate=0):
    surface_dict = {}
    starting_amount = 1
    arbitrageGroup = t_group["pairs"]
    min_surface_rate = min_rate
    pool_contract_1 = ""
    pool_contract_2 = ""
    pool_contract_3 = ""
    pool_direction_contract_1 = ""
    pool_direction_contract_2 = ""
    pool_direction_contract_3 = ""

    trade_directions = ["forward", "reverse"]

    # Get pairs info
    a_base = t_group["aBase"]
    a_quote = t_group["aQuote"]
    b_base = t_group["bBase"]
    b_quote = t_group["bQuote"]
    c_base = t_group["cBase"]
    c_quote = t_group["cQuote"]

    # Get price info
    a_token_0_price = float(t_group["aToken0Price"])
    a_token_1_price = float(t_group["aToken1Price"])
    b_token_0_price = float(t_group["bToken0Price"])
    b_token_1_price = float(t_group["bToken1Price"])
    c_token_0_price = float(t_group["cToken0Price"])
    c_token_1_price = float(t_group["cToken1Price"])

    # Get contract info
    a_contract = t_group["aContract"]
    b_contract = t_group["bContract"]
    c_contract = t_group["cContract"]

    acquired_coin_t1 = 0
    acquired_coin_t2 = 0
    acquired_coin_t3 = 0
    swap_1_rate = 0
    swap_2_rate = 0
    swap_3_rate = 0
    swap_1 = 0
    swap_2 = 0
    swap_3 = 0

    calculated = False

    # Computes surface rate for both direction of trade
    # Trade Forward
    for direction in trade_directions:
        # Forward: start with aBase

        if direction == "forward":
            swap_1 = a_base
            swap_2 = a_quote
            swap_1_rate = a_token_1_price
            pool_direction_contract_1 = "baseToQuote"
            pool_contract_1 = a_contract
            acquired_coin_t1 = starting_amount * swap_1_rate
            
            # Forward: Check if aQuote (acquired coin) matches bBase
            if a_quote == b_base:
                pool_contract_2 = b_contract
                pool_direction_contract_2 = "baseToQuote"
                swap_2_rate = b_token_1_price
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate

                pool_contract_3 = c_contract
                # Forward: Check if bQuote (acquired coin) matches cBase
                if b_quote == c_base:
                    swap_3 = c_base
                    pool_direction_contract_3 = "baseToQuote"
                    swap_3_rate = c_token_1_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

                # Forward: Check if bQuote (acquired coin) matches cQuote
                elif b_quote == c_quote:
                    swap_3 = c_quote
                    pool_direction_contract_3 = "quoteToBase"
                    swap_3_rate = c_token_0_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

            # Forward: Check if aQuote (acquired coin) matches bQuote
            if a_quote == b_quote:
                pool_contract_2 = b_contract
                pool_direction_contract_2 = "quoteToBase"
                swap_2_rate = b_token_0_price
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate

                pool_contract_3 = c_contract
                # Forward: Check if bBase (acquired coin) matches cBase
                if b_base == c_base:
                    swap_3 = c_base
                    pool_direction_contract_3 = "baseToQuote"
                    swap_3_rate = c_token_1_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

                # Forward: Check if bBase (acquired coin) matches cQuote
                elif b_base == c_quote:
                    swap_3 = c_quote
                    pool_direction_contract_3 = "quoteToBase"
                    swap_3_rate = c_token_0_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

            # Forward: Check if aQuote (acquired coin) matches cBase
            if a_quote == c_base:
                pool_contract_2 = c_contract
                pool_direction_contract_2 = "baseToQuote"
                swap_2_rate = c_token_1_price
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate

                pool_contract_3 = b_contract
                # Forward: Check if cQuote (acquired coin) matches bBase
                if c_quote == b_base:
                    swap_3 = b_base
                    pool_direction_contract_3 = "baseToQuote"
                    swap_3_rate = b_token_1_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

                # Forward: Check if cQuote (acquired coin) matches bQuote
                if c_quote == b_quote:
                    swap_3 = b_quote
                    pool_direction_contract_3 = "quoteToBase"
                    swap_3_rate = b_token_0_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

            # Forward: Check if aQuote (acquired coin) matches cQuote
            if a_quote == c_quote:
                pool_contract_2 = c_contract
                pool_direction_contract_2 = "quoteToBase"
                swap_2_rate = c_token_0_price
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate

                pool_contract_3 = b_contract

                # Forward: Check if cBase (acquired coin) matches bBase
                if c_base == b_base:
                    swap_3 = b_base
                    pool_direction_contract_3 = "baseToQuote"
                    swap_3_rate = b_token_1_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

                # Forward: Check if cBase (acquired coin) matches bQuote
                elif c_base == b_quote:
                    swap_3 = b_quote
                    pool_direction_contract_3 = "quoteToBase"
                    swap_3_rate = b_token_0_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

        # TODO simplify and shorten code
        # Reverse: start with aQuote
        elif direction == "reverse":
            swap_1 = a_quote
            swap_2 = a_base
            swap_1_rate = a_token_0_price
            pool_direction_contract_1 = "quoteToBase"
            pool_contract_1 = a_contract
            acquired_coin_t1 = starting_amount * swap_1_rate

            # Reverse: Check if aBase (acquired coin) matches bBase
            if a_base == b_base:
                pool_contract_2 = b_contract
                pool_direction_contract_2 = "baseToQuote"
                swap_2_rate = b_token_1_price
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate

                pool_contract_3 = c_contract
                # Reverse: Check if bQuote (acquired coin) matches cBase
                if b_quote == c_base:
                    swap_3 = c_base
                    pool_direction_contract_3 = "baseToQuote"
                    swap_3_rate = c_token_1_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

                # Reverse: Check if bQuote (acquired coin) matches cQuote
                elif b_quote == c_quote:
                    swap_3 = c_quote
                    pool_direction_contract_3 = "quoteToBase"
                    swap_3_rate = c_token_0_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

            # Reverse: Check if aBase (acquired coin) matches bQuote
            if a_base == b_quote:
                pool_contract_2 = b_contract
                pool_direction_contract_2 = "quoteToBase"
                swap_2_rate = b_token_0_price
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate

                pool_contract_3 = c_contract
                # Reverse: Check if bBase (acquired coin) matches cBase
                if b_base == c_base:
                    swap_3 = c_base
                    pool_direction_contract_3 = "baseToQuote"
                    swap_3_rate = c_token_1_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

                # Reverse: Check if bBase (acquired coin) matches cQuote
                elif b_base == c_quote:
                    swap_3 = c_quote
                    pool_direction_contract_3 = "quoteToBase"
                    swap_3_rate = c_token_0_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

            # Reverse: Check if aBase (acquired coin) matches cBase
            if a_base == c_base:
                pool_contract_2 = c_contract
                pool_direction_contract_2 = "baseToQuote"
                swap_2_rate = c_token_1_price
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate

                pool_contract_3 = b_contract
                # Reverse: Check if cQuote (acquired coin) matches bBase
                if c_quote == b_base:
                    swap_3 = b_base
                    pool_direction_contract_3 = "baseToQuote"
                    swap_3_rate = b_token_1_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

                # Reverse: Check if cQuote (acquired coin) matches bQuote
                if c_quote == b_quote:
                    swap_3 = b_quote
                    pool_direction_contract_3 = "quoteToBase"
                    swap_3_rate = b_token_0_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

            # Reverse: Check if aBase (acquired coin) matches cQuote
            if a_base == c_quote:
                pool_contract_2 = c_contract
                pool_direction_contract_2 = "quoteToBase"
                swap_2_rate = c_token_0_price
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate

                pool_contract_3 = b_contract

                # Reverse: Check if cBase (acquired coin) matches bBase
                if c_base == b_base:
                    swap_3 = b_base
                    pool_direction_contract_3 = "baseToQuote"
                    swap_3_rate = b_token_1_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

                # Reverse: Check if cBase (acquired coin) matches bQuote
                elif c_base == b_quote:
                    swap_3 = b_quote
                    pool_direction_contract_3 = "quoteToBase"
                    swap_3_rate = b_token_0_price
                    acquired_coin_t3 = acquired_coin_t2 * swap_3_rate

        # Calculate surface rate arbitrage
        profit_loss = acquired_coin_t3-starting_amount
        surface_rate_perc = profit_loss/starting_amount if starting_amount != 0 else 0

        if surface_rate_perc > min_surface_rate:
            surface_dict = {
                "direction": direction,
                "swap1": swap_1,
                "swap2": swap_2,
                "swap3": swap_3,
                "arbitrageGroup": arbitrageGroup,
                "poolContract1": pool_contract_1,
                "poolContract2": pool_contract_2,
                "poolContract3": pool_contract_3,
                "poolDirectionContract1": pool_direction_contract_1,
                "poolDirectionContract2": pool_direction_contract_2,
                "poolDirectionContract3": pool_direction_contract_3,
                "swap1Rate": swap_1_rate,
                "swap2Rate": swap_2_rate,
                "swap3Rate": swap_3_rate,
                "acquiredCoinT1": acquired_coin_t1,
                "acquiredCoinT2": acquired_coin_t2,
                "acquiredCoinT3": acquired_coin_t3,
                "profitLoss": profit_loss,
                "surface_rate": surface_rate_perc
            }
            return surface_dict

    return surface_dict