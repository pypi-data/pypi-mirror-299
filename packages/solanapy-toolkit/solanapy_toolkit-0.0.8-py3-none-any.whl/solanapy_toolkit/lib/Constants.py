from spl.token.constants import TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID
from solana.rpc.types import TokenAccountOpts
from solders.pubkey import Pubkey

class Constants:
    CONVERSION_FACTOR = 9
    LAMPORT_PER_SOL = 10**CONVERSION_FACTOR
    SOL_PER_LAMPORT = 1 / LAMPORT_PER_SOL
    VALID_COMMITMENTS = ["processed", "confirmed", "finalized", "recent", "single", "root", "max"]
    TOKEN_PROGRAM_ID = str(TOKEN_PROGRAM_ID)
    TOKEN_2022_PROGRAM_ID = str(TOKEN_2022_PROGRAM_ID)
    SOL_TOKEN = "So11111111111111111111111111111111111111111"
    WSOL_TOKEN = "So11111111111111111111111111111111111111112"
    SYSTEM_PROGRAM = "11111111111111111111111111111111"
    TOKEN_ACCOUNT_OPTS = TokenAccountOpts(program_id=Pubkey.from_string(str(TOKEN_PROGRAM_ID)))
    TOKEN_2022_ACCOUNT_OPTS = TokenAccountOpts(program_id=Pubkey.from_string(str(TOKEN_2022_PROGRAM_ID)))

