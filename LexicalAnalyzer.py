import string

ID_VALID_CHARS = {string.ascii_letters + string.digits + '_'}
TOKENS = []


class Tokens:
    def __init__(self, lexeme, token, index):
        self.lexeme = lexeme
        self.token = token
        self.index = index
        self.payload = None

    def __lt__(self, other):
        return self.index < other.index


KEYWORDS = {
    "bool": "T_Bool",
    "break": "T_Break",
    "char": "T_Char",
    "continue": "T_Continue",
    "else": "T_Else",
    "false": "T_False",
    "for": "T_For",
    "if": "T_If",
    "int": "T_Int",
    "print": "T_Print",
    "return": "T_Return",
    "true": "T_True",
}

OPERATORS = {
    '+': "T_AOp_PL",
    '-': "T_AOp_MN",
    '*': "T_AOp_ML",
    '/': "T_AOp_DV",
    '%': "T_AOp_RM",
    '=': "T_Assign",
}

RELATIONAL_OPERATORS = {
    '<': 'T_ROp_L',
    '>': 'T_ROp_G',
    '<=': 'T_ROp_LE',
    '>=': 'T_ROp_LE',
    '!=': 'T_ROp_NE',
    '==': 'T_ROp_E',
}

LOGICAL_OPERATORS = {
    '&&': 'T_LOp_AND',
    '||': 'T_LOp_OR',
    '!': 'T_LOp_NOT',
}

SYMBOLS = {
    '(': 'T_LP',
    ')': 'T_RP',
    '{': 'T_LC',
    '}': 'T_RC',
    '[': 'T_LB',
    ']': 'T_RB',
    ';': 'T_Semicolon',
    ',': 'T_Comma',
}


def detect_id(text: str, start_index: int):
    result = ''
    valid_start_chars = {string.ascii_letters + '_'}
    if text[start_index] not in valid_start_chars:
        return False, start_index, result

    while text[start_index] in ID_VALID_CHARS:
        result += text[start_index]
        start_index += 1

    if result and result not in KEYWORDS:
        TOKENS.append(Tokens(lexeme=result, token="T_Id", index=start_index))


def find_keywords(text: str, start_index: int):
    text_length = len(text)
    for keyword in KEYWORDS.keys():
        keyword_length = len(keyword)
        end_index = start_index + keyword_length
        if end_index <= text_length:
            if (
                    (start_index == 0 or not text[start_index - 1].isalpha())
                    and (end_index == text_length or not text[end_index].isalpha())
                    and text[start_index:end_index] == keyword
            ):
                result = keyword
                TOKENS.append(Tokens(lexeme=result, token=KEYWORDS[keyword], index=start_index))
                start_index = end_index


def find_symbols(text: str, start_index: int):
    for symbol in SYMBOLS.keys():
        end_index = start_index + len(symbol)
        if text[start_index:end_index] == symbol:
            symbol_result = symbol
            TOKENS.append(Tokens(lexeme=symbol_result, token=SYMBOLS[symbol], index=end_index))


def find_comments(text: str, start_index: int):
    in_comment = False
    current_comment = ""
    for i in range(start_index, len(text)):
        char = text[i]

        if not in_comment:
            if char == '/':
                if i + 1 < len(text) and text[i + 1] == '/':
                    in_comment = True
                    current_comment = "/"
                continue

        if in_comment:
            current_comment += char

        if in_comment and char == '\n':
            in_comment = False
            token = Tokens(lexeme="//", token="T_Comment", index=i)
            token.payload = current_comment
            TOKENS.append(token)


def main(text, startIndex):
    while startIndex < len(text):
        find_symbols(text=text, start_index=startIndex)
        find_keywords(text=text, start_index=startIndex)
        detect_id(text=text, start_index=startIndex)

        startIndex += 1

    find_comments(text=text, start_index=0)

    TOKENS.sort()
    for e in TOKENS:
        print(e.lexeme, e.token, e.index)


if __name__ == "__main__":
    # TODO: read code from file
    with open(r"test.txt", 'r') as file:
        text = file.read()

    main(text=text, startIndex=0)
