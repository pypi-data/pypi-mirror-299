# evaluator.py

from .parser import ASTNode
from .exceptions import EvaluatorError, ReturnValue



class Evaluator:
    def __init__(self, ast):
        self.ast = ast
        self.scopes = [{}]  # Stack of variable scopes
        self.functions = {}

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def get_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise EvaluatorError(f"Undefined variable: {name}")

    def set_variable(self, name, value):
        self.scopes[-1][name] = value


    def evaluate(self):
        for node in self.ast:
            self.execute(node)

    def execute(self, node):
        if node.node_type == 'RETURN':
            value = self.evaluate_expression(node.value)
            raise ReturnValue(value)
        elif node.node_type == 'ASSIGNMENT':
            self.assign(node)
        elif node.node_type == 'PRINT':
            self.print_value(node)
        elif node.node_type == 'FUNCTION_DEF':
            self.define_function(node)
        elif node.node_type == 'FUNCTION_CALL':
            self.call_function(node)  # We don't need the return value here
        elif node.node_type == 'IF':
            self.execute_if(node)
        elif node.node_type == 'WHILE':
            self.execute_while(node)
        else:
            raise EvaluatorError(f"Unknown node type: {node.node_type}")


    
    def execute_if(self, node):
        condition, then_branch, else_branch = node.value
        if self.evaluate_expression(condition):
            for stmt in then_branch:
                self.execute(stmt)
        elif else_branch:
            for stmt in else_branch:
                self.execute(stmt)

    def execute_while(self, node):
        condition, body = node.value
        while self.evaluate_expression(condition):
            for stmt in body:
                self.execute(stmt)




    def assign(self, node):
        var_name, expression = node.value
        value = self.evaluate_expression(expression)
        self.set_variable(var_name, value)


    def print_value(self, node):
        values = []
        for expr in node.value:
            value = self.evaluate_expression(expr)
            values.append(str(value))  # Convert all values to string
        print(' '.join(values))  # Print all concatenated values with spaces


    def define_function(self, node):
        func_name, params = node.value
        self.functions[func_name] = (params, node.children)

    def call_function(self, node):
        func_name, args = node.value

        if func_name not in self.functions:
            raise EvaluatorError(f"Undefined function: {func_name}")

        params, func_body = self.functions[func_name]

        if len(args) != len(params):
            raise EvaluatorError(f"Function '{func_name}' expects {len(params)} arguments, got {len(args)}")

        # Evaluate arguments
        evaluated_args = [self.evaluate_expression(arg) for arg in args]

        # Push a new scope
        self.push_scope()
        for param, arg in zip(params, evaluated_args):
            self.set_variable(param, arg)

        result = None
        try:
            for stmt in func_body:
                self.execute(stmt)
        except ReturnValue as rv:
            result = rv.value
        finally:
            # Pop the scope after function execution
            self.pop_scope()

        # Allow functions without a return value to return None
        return result  # This will return None if no explicit return value is provided




    def evaluate_expression(self, expression):
        if isinstance(expression, ASTNode):
            if expression.node_type == 'EXPRESSION':
                left = self.evaluate_expression(expression.value[0])
                operator = expression.value[1]
                right = self.evaluate_expression(expression.value[2])
                return self.apply_operator(left, operator, right)
            elif expression.node_type == 'UNARY_EXPRESSION':
                operator, operand = expression.value
                value = self.evaluate_expression(operand)
                return self.apply_operator(value, operator)
            elif expression.node_type == 'FUNCTION_CALL':
                return self.call_function(expression)
            else:
                raise EvaluatorError(f"Unknown expression node type: {expression.node_type}")
        else:
            return self.get_value(expression)



    def apply_operator(self, left, operator, right=None):
        if operator == 'AND':
            return left and right
        elif operator == 'OR':
            return left or right
        elif operator == 'NOT':
            return not left
        elif operator == 'PLUS':
            return left + right
        elif operator == 'MINUS':
            return left - right
        elif operator == 'MULTIPLY':
            return left * right
        elif operator == 'DIVIDE':
            return left / right
        elif operator == 'EQ':
            return left == right
        elif operator == 'NEQ':
            return left != right
        elif operator == 'LT':
            return left < right
        elif operator == 'LTE':
            return left <= right
        elif operator == 'GT':
            return left > right
        elif operator == 'GTE':
            return left >= right
        else:
            raise EvaluatorError(f"Unknown operator: {operator}")


    def get_value(self, token):
        if isinstance(token, int):
            return token
        elif isinstance(token, str):
            if token.startswith('"') and token.endswith('"'):
                return token[1:-1]  # Strip quotes for strings
            else:
                return self.get_variable(token)
        else:
            return token

