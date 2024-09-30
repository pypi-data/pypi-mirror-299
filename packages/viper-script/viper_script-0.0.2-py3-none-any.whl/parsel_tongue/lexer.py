# lexer.py

import re
from .exceptions import LexerError


# Order matters: longer patterns should come first
TOKEN_TYPES = [
    ('PRINT', r'\bprint\b'),        # 'print' keyword
    ('IF', r'\bif\b'),              # 'if' keyword
    ('ELSE', r'\belse\b'),          # 'else' keyword
    ('WHILE', r'\bwhile\b'),        # 'while' keyword
    ('FUNCTION', r'\bfunction\b'),  # 'function' keyword
    ('RETURN', r'\breturn\b'),      # 'return' keyword
    ('AND', r'\band\b'),            # 'and' operator
    ('OR', r'\bor\b'),              # 'or' operator
    ('NOT', r'\bnot\b'),            # 'not' operator
    ('EQ', r'=='),                  # '==' operator
    ('NEQ', r'!='),                 # '!=' operator
    ('LTE', r'<='),                 # '<=' operator
    ('GTE', r'>='),                 # '>=' operator
    ('LT', r'<'),                   # '<' operator
    ('GT', r'>'),                   # '>' operator
    ('NUMBER', r'\d+'),             # Integer numbers
    ('STRING', r'"[^"\n]*"'),       # String literals
    ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers (variables and function names)
    ('ASSIGN', r'='),               # Assignment operator
    ('PLUS', r'\+'),                # '+' operator
    ('MINUS', r'-'),                # '-' operator
    ('MULTIPLY', r'\*'),            # '*' operator
    ('DIVIDE', r'/'),               # '/' operator
    ('LPAREN', r'\('),              # '('
    ('RPAREN', r'\)'),              # ')'
    ('COLON', r':'),                # ':'
    ('COMMA', r','),                # ','
    ('NEWLINE', r'\n'),             # Newline
    ('SKIP', r'[ \t]+'),            # Skip spaces and tabs
    ('COMMENT', r'\#.*'),           # Single-line comment
    ('MISMATCH', r'.'),             # Any other character (for catching errors)
]

def tokenize(code):
    tokens = []
    position = 0
    lineno = 1
    indent_stack = [0]
    # Precompile the regex patterns
    TOKEN_REGEXES = [(token_type, re.compile(pattern)) for token_type, pattern in TOKEN_TYPES]

    while position < len(code):
        match = None
        for token_type, regex in TOKEN_REGEXES:
            match = regex.match(code, position)
            if match:
                token_value = match.group(0)
                if token_type == 'NEWLINE':
                    tokens.append(('NEWLINE', token_value))
                    position = match.end(0)
                    lineno += 1
                    # Handle indentation after newline
                    if position < len(code):
                        whitespace_match = re.match(r'[ \t]*', code[position:])
                        if whitespace_match:
                            ws = whitespace_match.group(0)
                            position += len(ws)
                            current_indent = len(ws.replace('\t', ' ' * 4))
                            last_indent = indent_stack[-1]
                            if current_indent > last_indent:
                                indent_stack.append(current_indent)
                                tokens.append(('INDENT', ws))
                            elif current_indent < last_indent:
                                while current_indent < indent_stack[-1]:
                                    indent_stack.pop()
                                    tokens.append(('DEDENT', ''))
                    break
                elif token_type == 'COMMENT':
                    # Skip comments
                    position = match.end(0)
                    break
                elif token_type == 'SKIP':
                    # Skip whitespace
                    position = match.end(0)
                    break
                else:
                    tokens.append((token_type, token_value))
                    position = match.end(0)
                    break
        if not match:
            raise LexerError(f"Unexpected character: '{code[position]}' at line {lineno}")
    # Add DEDENT tokens at the end of the file
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(('DEDENT', ''))
    return tokens
