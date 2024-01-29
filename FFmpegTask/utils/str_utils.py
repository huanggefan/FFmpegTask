def str_has_token(string: str, tokens: list[str]) -> bool:
    for token in tokens:
        if token not in string:
            return False
    return True
