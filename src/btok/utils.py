from .constants import CH_MASK, PT_ATOZ_WS, PT_CH_CJK


def mask_ws_between_atoz(sentence: str) -> str:
    return PT_ATOZ_WS.sub(CH_MASK, sentence)


def replace_mask_to_ws(tokens: list[str]):
    return [token.replace(CH_MASK, " ") for token in tokens]


def calc_cjk_char_len(token: str) -> int:
    return sum(1 for char in token if PT_CH_CJK.match(char))
