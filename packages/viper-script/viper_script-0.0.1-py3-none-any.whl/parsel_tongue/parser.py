# parser.py

from .exceptions import ParserError

import sys


class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        return f"ASTNode(type={self.node_type}, value={self.value}, children={self.children})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        ast = []
        while self.position < len(self.tokens):
            self.skip_newlines()
            if self.position < len(self.tokens):
                node = self.statement()
                ast.append(node)
        return ast

    def statement(self):
        token_type, _ = self.current_token()
        if token_type == 'RETURN':
            return self.return_statement()
        if token_type == 'FUNCTION':
            return self.function_definition()
        elif token_type == 'IF':
            return self.if_statement()
        elif token_type == 'WHILE':
            return self.while_loop()
        elif token_type == 'ID':
            if self.peek_next_token()[0] == 'LPAREN':
                return self.function_call()
            else:
                return self.assignment()
        elif token_type == 'PRINT':
            return self.print_statement()
        else:
            raise ParserError(f"Unexpected token {self.current_token()} at position {self.position}")

    def return_statement(self):
        self.consume('RETURN')
        expression = self.expression()
        return ASTNode('RETURN', expression)




    
    def if_statement(self):
        self.consume('IF')
        condition = self.expression()
        self.consume('COLON')
        self.consume('NEWLINE')
        self.consume('INDENT')
        then_branch = self.block()
        self.consume('DEDENT')

        else_branch = []
        if self.position < len(self.tokens) and self.current_token()[0] == 'ELSE':
            self.consume('ELSE')
            self.consume('COLON')
            self.consume('NEWLINE')
            self.consume('INDENT')
            else_branch = self.block()
            self.consume('DEDENT')

        return ASTNode('IF', (condition, then_branch, else_branch))


    def while_loop(self):
        self.consume('WHILE')
        condition = self.expression()
        self.consume('COLON')
        self.consume('NEWLINE')
        self.consume('INDENT')
        body = self.block()
        self.consume('DEDENT')
        return ASTNode('WHILE', (condition, body))



    def assignment(self):
        identifier = self.consume('ID')
        self.consume('ASSIGN')
        expression = self.expression()
        return ASTNode('ASSIGNMENT', (identifier, expression))

    def print_statement(self):
        self.consume('PRINT')
        expressions = [self.expression()]  # Start with the first expression
        while self.position < len(self.tokens) and self.current_token()[0] == 'COMMA':
            self.consume('COMMA')  # Consume the comma
            expressions.append(self.expression())  # Append the next expression
        return ASTNode('PRINT', expressions)


    def function_definition(self):
        self.consume('FUNCTION')
        func_name = self.consume('ID')
        self.consume('LPAREN')
        params = []
        while self.current_token()[0] != 'RPAREN':
            params.append(self.consume('ID'))
            if self.current_token()[0] == 'COMMA':
                self.consume('COMMA')
        self.consume('RPAREN')
        self.consume('COLON')
        self.consume('NEWLINE')
        self.consume('INDENT')
        body = self.block()
        self.consume('DEDENT')
        return ASTNode('FUNCTION_DEF', (func_name, params), body)

    def function_call(self):
        func_name = self.consume('ID')
        self.consume('LPAREN')
        args = []
        while self.current_token()[0] != 'RPAREN':
            args.append(self.expression())
            if self.current_token()[0] == 'COMMA':
                self.consume('COMMA')
        self.consume('RPAREN')
        return ASTNode('FUNCTION_CALL', (func_name, args))

    def function_call_with_identifier(self, func_name):
        self.consume('LPAREN')
        args = []
        while self.current_token()[0] != 'RPAREN':
            args.append(self.expression())
            if self.current_token()[0] == 'COMMA':
                self.consume('COMMA')
        self.consume('RPAREN')
        return ASTNode('FUNCTION_CALL', (func_name, args))


    def block(self):
        statements = []
        while self.position < len(self.tokens):
            self.skip_newlines()
            if self.current_token()[0] == 'DEDENT':
                break
            statements.append(self.statement())
        return statements



    def expression(self):
        return self.parse_expression()

    def parse_expression(self, precedence=0):
        left = self.parse_primary()

        while True:
            if self.position >= len(self.tokens):
                break
            current_token = self.current_token()
            token_type = current_token[0]

            if token_type not in PRECEDENCE or PRECEDENCE[token_type] < precedence:
                break

            operator_token_type = token_type
            self.consume(operator_token_type)
            operator = operator_token_type  # Use token type as the operator

            # For unary operators like NOT
            if operator in ['NOT']:
                operand = self.parse_expression(PRECEDENCE[operator_token_type])
                left = ASTNode('UNARY_EXPRESSION', (operator, operand))
            else:
                right = self.parse_expression(PRECEDENCE[operator_token_type] + 1)
                left = ASTNode('EXPRESSION', (left, operator, right))

        return left




    def parse_primary(self):
        token_type, token_value = self.current_token()

        if token_type == 'NOT':
            self.consume('NOT')
            operand = self.parse_expression(PRECEDENCE['NOT'])
            return ASTNode('UNARY_EXPRESSION', ('NOT', operand))
        elif token_type == 'NUMBER':
            self.consume('NUMBER')
            return int(token_value)
        elif token_type == 'STRING':
            self.consume('STRING')
            return token_value
        elif token_type == 'ID':
            identifier = self.consume('ID')
            if self.position < len(self.tokens) and self.current_token()[0] == 'LPAREN':
                # Function call within expression
                return self.function_call_with_identifier(identifier)
            else:
                return identifier
        elif token_type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        else:
            raise ParserError(f"Unexpected token {self.current_token()} in expression at position {self.position}")


    def current_token(self):
        return self.tokens[self.position]

    def consume(self, expected_type):
        token_type, token_value = self.current_token()
        if token_type == expected_type:
            self.position += 1
            return token_value
        raise ParserError(f"Expected token type {expected_type}, but got {token_type} at position {self.position}")

    def peek_next_token(self):
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return (None, None)

    def skip_newlines(self):
        while self.position < len(self.tokens) and self.current_token()[0] == 'NEWLINE':
            self.position += 1


# Define operator precedence
PRECEDENCE = {
    'OR': 1,
    'AND': 2,
    'NOT': 3,
    'EQ': 4,
    'NEQ': 4,
    'LT': 4,
    'LTE': 4,
    'GT': 4,
    'GTE': 4,
    'PLUS': 5,
    'MINUS': 5,
    'MULTIPLY': 6,
    'DIVIDE': 6,
}
