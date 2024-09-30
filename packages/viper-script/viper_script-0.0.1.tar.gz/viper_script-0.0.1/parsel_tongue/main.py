import sys
import traceback

# parsel_tongue/main.py

from .lexer import tokenize
from .parser import Parser
from .evaluator import Evaluator
from .exceptions import LexerError, ParserError, EvaluatorError



def run_code(code):
    try:
        tokens = tokenize(code)
        # Uncomment for debugging
        # print(f"Tokens: {tokens}")
        parser = Parser(tokens)
        ast = parser.parse()
        # Uncomment for debugging
        # print(f"AST: {ast}")
        evaluator = Evaluator(ast)
        evaluator.evaluate()
    except (LexerError, ParserError, EvaluatorError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print("Unknown Error:")
        traceback.print_exc()

def repl():
    print("Welcome to ParselTongue REPL. Type 'exit' to quit.")
    code_lines = []
    prompt = '>> '
    while True:
        try:
            line = input(prompt)
            if line.strip().lower() == 'exit':
                break
            if not line.strip():
                continue  # Skip empty lines
            code_lines.append(line)
            # Check if the line ends with ':' indicating a code block
            if line.rstrip().endswith(':'):
                # Continue collecting indented lines
                prompt = '.. '  # Indentation prompt
                while True:
                    next_line = input(prompt)
                    if next_line.strip() == '':
                        break  # Empty line signifies end of code block
                    code_lines.append(next_line)
                # Reset prompt after code block
                prompt = '>> '
            # If not in a code block, execute the code
            if prompt == '>> ':
                code = '\n'.join(code_lines)
                # Print the code for debugging
                print("Executing code:")
                print(code)
                run_code(code)
                # Reset for the next input
                code_lines = []
        except KeyboardInterrupt:
            print("\nExiting REPL.")
            break
        except Exception as e:
            print(f"Error: {e}")
            # Reset in case of an error
            code_lines = []
            prompt = '>> '


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--repl':
            repl()
        else:
            filename = sys.argv[1]
            with open(filename, 'r') as file:
                code = file.read()
            run_code(code)
    else:
        print("Usage: python main.py <filename>")
        print("Or, start the REPL by running: python main.py --repl")

if __name__ == "__main__":
    main()
