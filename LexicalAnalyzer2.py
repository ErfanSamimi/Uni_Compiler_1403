import string

ID_VALID_CHARS = {x for x in string.ascii_letters + string.digits + '_'}
ID_VALID_START_CHARS = {x for x in string.ascii_letters + '_'}
SHOW_WHITESPACES = False

class Tokens:
    def __init__(self, lexeme, token, index):
        self.lexeme = lexeme
        self.token = token
        self.index = index

    def __lt__(self, other):
        return self.index < other.index

    def __str__(self):
        if self.token == 'T_Whitespace':
            representation_string = f"{self.index - len(self.lexeme)}: whitespace -> {self.token}"
        else:
            representation_string = f"{self.index - len(self.lexeme)}: {self.lexeme} -> {self.token}"

        return representation_string


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

SINGLE_CHAR_OPERATORS = {
    '+': "T_AOp_PL",
    '-': "T_AOp_MN",
    '*': "T_AOp_ML",
    '/': "T_AOp_DV",
    '%': "T_AOp_RM",
    '=': "T_Assign",
    '<': 'T_ROp_L',
    '>': 'T_ROp_G',
    '!': 'T_LOp_NOT',
}

DOUBLE_CHAR_OPERATORS = {
    '<=': 'T_ROp_LE',
    '>=': 'T_ROp_LE',
    '!=': 'T_ROp_NE',
    '==': 'T_ROp_E',
    '&&': 'T_LOp_AND',
    '||': 'T_LOp_OR',

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


def find_id(text: str, startindex: int):
    result = ''
    if text[startindex] not in ID_VALID_START_CHARS:
        return None

    while startindex < len(text) and text[startindex] in ID_VALID_CHARS:
        result += text[startindex]
        startindex += 1

    if result and result not in KEYWORDS:
        return Tokens(lexeme=result, token="T_Id", index=startindex)

    return None


def find_keywords(text: str, startindex: int):
    result = ''

    while startindex < len(text) and text[startindex] in ID_VALID_CHARS:
        result += text[startindex]
        startindex += 1

    if result and result in KEYWORDS:
        return Tokens(lexeme=result, token=KEYWORDS[result], index=startindex)

    return None


def find_comments(text: str, startindex: int):
    is_comment = text[startindex: startindex + 2] == '//'
    if not is_comment:
        return None

    result = ''

    while startindex < len(text) and text[startindex] != '\n':
        result += text[startindex]
        startindex += 1

    if result and text[startindex] == '\n':
        return Tokens(lexeme=result, token='T_Comment', index=startindex)

    return None


# ----------------------------------------------------------------------------------------------------


def find_decimal(text, startindex):
    valid_start_characters = {'+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    if text[startindex] not in valid_start_characters:
        return None

    sign = ''
    if text[startindex] in ['-', '+']:
        sign = text[startindex]
        startindex += 1

    result = ''
    valid_chars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

    while startindex < len(text):
        if text[startindex] in valid_chars:
            result += text[startindex]
            startindex += 1
        else:
            break

    if not result:
        return None

    else:
        return Tokens(lexeme=sign + result, token='T_Decimal', index=startindex)


def find_hex(text, startindex):
    hex_sign = text[startindex: startindex + 2]
    is_hex = hex_sign in ['0x', '0X']
    if not is_hex:
        return None
    else:
        startindex += 2

    valid_chars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'}
    result = ''

    while startindex < len(text):
        if text[startindex].lower() in valid_chars:
            result += text[startindex]
            startindex += 1
        else:
            break

    if not result:
        return None

    else:
        lexeme = hex_sign + result
        return Tokens(lexeme=lexeme, token='T_Hexadecimal', index=startindex)


def find_single_char(text, startindex):
    if text[startindex] != "'":
        return None

    startindex += 1
    result = ''
    while startindex < len(text) and text[startindex] != "'":
        char = text[startindex]
        result += char
        if char == '\\':
            startindex += 1
            result += text[startindex]

        startindex += 1

    if startindex < len(text) and text[startindex] == "'" \
            and (len(result) in [0, 1] or (len(result) == 2 and result[0] == '\\')):

        startindex += 1
        return Tokens(lexeme="'" + result + "'", token='T_Character', index=startindex)

    return None


def find_string(text, startindex):
    if startindex == 271:
        pass
    if text[startindex] != '"':
        return None

    startindex += 1
    result = ''
    while startindex < len(text) and text[startindex] != '"':
        char = text[startindex]
        result += char
        if char == '\\':
            startindex += 1
            result += text[startindex]

        startindex += 1

    if startindex < len(text) and text[startindex] == '"':
        startindex += 1
        return Tokens(lexeme='"' + result + '"', token='T_String', index=startindex)

    return None


def create_operator_finder_function(operator, token_type):
    def finder_function(text, startindex):
        result = ''
        for i in range(len(operator)):
            if startindex >= len(text):
                return None
            result += text[startindex]
            startindex += 1

        if result == operator:
            return Tokens(lexeme=operator, token=token_type, index=startindex)

        return None

    return finder_function


def find_whitespaces(text, startindex):
    result = ''
    while startindex < len(text) and text[startindex] in string.whitespace:
        result += text[startindex]
        startindex += 1

    if not len(result):
        return None

    return Tokens(lexeme=result, token='T_Whitespace', index=startindex)


def main(text, start_index):
    function_list = [
        find_keywords,
        find_id,
        find_comments,
        find_hex,
        find_decimal,
        find_single_char,
        find_string,
        find_whitespaces,
    ]

    for key, value in DOUBLE_CHAR_OPERATORS.items():
        function_list.append(create_operator_finder_function(key, value))

    for key, value in SINGLE_CHAR_OPERATORS.items():
        function_list.append(create_operator_finder_function(key, value))

    for key, value in SYMBOLS.items():
        function_list.append(create_operator_finder_function(key, value))

    while start_index < len(text):
        token_founded = False
        for func in function_list:
            token = func(text, start_index)
            if token is not None:
                if not(token.token == "T_Whitespace" and not SHOW_WHITESPACES):
                    print(token)

                start_index = token.index
                token_founded = True
                break

        if not token_founded:
            print(f"index={start_index}: Invalid code!")
            break


if __name__ == "__main__":
    # TODO: read code from file
    with open(r"test2.c", 'r') as file:
        text = file.read()

    main(text, 0)
