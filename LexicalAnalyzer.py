
import string

ID_VALID_CHARS = {string.ascii_letters + string.digits + '_'}
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
    "return": "T_Retrun",
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
    valid_start_charc = {string.ascii_letters + '_'}
    if text[start_index] not in valid_start_charc:
        return False, start_index, result
    

    while text[start_index] in ID_VALID_CHARS:
        result += text[start_index]
        start_index += 1

    if result and result not in KEYWORDS:
        return True, start_index, result
    else:
        return False, start_index, result
    



def main(text):
    pass



if __name__ == "__main__":
    #TODO: read code from file
    s = "int a = b + 4;"
    main(s)
    
