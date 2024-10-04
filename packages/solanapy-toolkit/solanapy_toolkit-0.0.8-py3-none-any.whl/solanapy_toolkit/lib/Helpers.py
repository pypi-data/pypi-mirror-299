import base58
import time
import json
import requests
import os
from dexscreener import DexscreenerClient
from solders.pubkey import Pubkey

from .Constants import Constants

def lamport_to_sol(lamports):
    return round(lamports / Constants.LAMPORT_PER_SOL, 9)

def sol_to_lamport(sol):
    return int(sol * Constants.LAMPORT_PER_SOL)

def array_to_base58(address_array):
    if isinstance(address_array, str):
        # Dangerous!
        address_array = eval(address_array)
    x_bytes = bytes(address_array)
    base58_encoded = base58.b58encode(x_bytes)
    return base58_encoded.decode('utf-8')

def base58_to_array(base58_string):
    base58_encoded = base58_string.encode('utf-8')
    decoded = base58.b58decode(base58_encoded)
    return str(list(decoded)).replace(' ', '')

def is_on_curve(address):
    if isinstance(address, str) and address != "":
        try:
            address = Pubkey.from_string(address)
        except Exception:
            raise TypeError("Malformed pubkey")
    elif isinstance(address, Pubkey):
        pass
    if address.is_on_curve():
        return True
    return False

def get_pairs_by_base_dexscreener(address):
    screener = DexscreenerClient()
    pair_addresses = []
    pairs = screener.search_pairs(address)
    if (pairs and pairs[0].base_token):
        base_token = pairs[0].base_token.address
    else:
        print(f"No base token for {address}!")
        return
    time.sleep(3)
    all_pairs = screener.search_pairs(base_token)
    for all_pair in all_pairs:
        pair_addresses.append(all_pair.pair_address)
    return pair_addresses

def get_pairs_by_base_solanatracker(address):
    headers = {'X-Billing-Token': os.getenv('SOLANATRACKER_TOKEN')}
    if not headers['X-Billing-Token']:
        raise Exception("Use SOLANATRACKER_TOKEN ENV")
    response = requests.get(f'https://solana.p.nadles.com/tokens/{address}', headers=headers)
    if response.status_code == 200:
        token = json.loads(response.content)
        pair_addresses = [pool['poolId'] for pool in token['pools']]
        pair_addresses.extend([pool['curve'] for pool in token['pools'] if pool.get('curve')])
        if address in pair_addresses:
            pair_addresses.remove(address)
        return pair_addresses
    else:
        return None

