# exceptions.py

class LexerError(Exception):
    pass

class ParserError(Exception):
    pass

class EvaluatorError(Exception):
    pass

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value
