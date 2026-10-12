from __future__ import annotations

from typing import Optional
from calculus.expressions.base import Expression, Number, Variable, Constant
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.expressions.functions import (
    Sin, Cos, Tan, Exp, Ln, Log, Sqrt, Abs
)
from calculus.constants.constants import pi, e
from fractions import Fraction


class Token:
    """Represents a single token in the mathematical expression."""
    
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Tokenizer:
    """Converts mathematical expression string into tokens."""
    
    OPERATORS = {'+', '-', '*', '/', '^', '('}
    FUNCTIONS = {'sin', 'cos', 'tan', 'exp', 'ln', 'log', 'sqrt', 'abs', 'gamma'}
    CONSTANTS = {'pi', 'e', 'phi'}
    
    def __init__(self, text: str):
        self.text = text.strip()
        self.pos = 0
        self.tokens = []
    
    def tokenize(self) -> list[Token]:
        """Tokenize the expression."""
        while self.pos < len(self.text):
            if self.text[self.pos].isspace():
                self.pos += 1
                continue
            
            if self.text[self.pos] in self.OPERATORS or self.text[self.pos] == ')':
                self.tokens.append(Token('OP', self.text[self.pos]))
                self.pos += 1
            elif self.text[self.pos].isdigit() or self.text[self.pos] == '.':
                self._read_number()
            elif self.text[self.pos].isalpha() or self.text[self.pos] == '_':
                self._read_identifier()
            else:
                raise ValueError(f"Unexpected character: {self.text[self.pos]}")
        
        return self.tokens
    
    def _read_number(self) -> None:
        """Read a number (integer or fraction)."""
        start = self.pos
        
        # Read integer part
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self.pos += 1
        
        # Read decimal part
        if self.pos < len(self.text) and self.text[self.pos] == '.':
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
        
        # Read fraction part (e.g., 1/2)
        if self.pos < len(self.text) and self.text[self.pos] == '/':
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
        
        number_str = self.text[start:self.pos]
        self.tokens.append(Token('NUMBER', number_str))
    
    def _read_identifier(self) -> None:
        """Read a function, constant, or variable name."""
        start = self.pos
        
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            self.pos += 1
        
        name = self.text[start:self.pos]
        
        if name in self.FUNCTIONS:
            self.tokens.append(Token('FUNCTION', name))
        elif name in self.CONSTANTS:
            self.tokens.append(Token('CONSTANT', name))
        else:
            self.tokens.append(Token('VARIABLE', name))


class Parser:
    """Parses tokens into an Abstract Syntax Tree (AST)."""
    
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
    
    @staticmethod
    def parse(text: str) -> Expression:
        """Parse a mathematical expression string."""
        tokenizer = Tokenizer(text)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        return parser._parse_expression()
    
    def _current_token(self) -> Optional[Token]:
        """Get the current token without advancing."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def _advance(self) -> None:
        """Move to the next token."""
        self.pos += 1
    
    def _expect(self, value: str) -> Token:
        """Expect a specific token value."""
        token = self._current_token()
        if not token or token.value != value:
            raise ValueError(f"Expected {value}, got {token}")
        self._advance()
        return token
    
    def _parse_expression(self) -> Expression:
        """Parse addition/subtraction (lowest precedence)."""
        left = self._parse_term()
        
        while self._current_token() and self._current_token().value in ['+', '-']:
            op = self._current_token().value
            self._advance()
            right = self._parse_term()
            
            if op == '+':
                left = Add(left, right)
            else:
                left = Sub(left, right)
        
        return left
    
    def _parse_term(self) -> Expression:
        """Parse multiplication/division (medium precedence)."""
        left = self._parse_factor()
        
        while self._current_token() and self._current_token().value in ['*', '/']:
            op = self._current_token().value
            self._advance()
            right = self._parse_factor()
            
            if op == '*':
                left = Mul(left, right)
            else:
                left = Div(left, right)
        
        return left
    
    def _parse_factor(self) -> Expression:
        """Parse exponentiation (high precedence)."""
        left = self._parse_unary()
        
        if self._current_token() and self._current_token().value == '^':
            self._advance()
            right = self._parse_factor()  # Right-associative
            return Pow(left, right)
        
        return left
    
    def _parse_unary(self) -> Expression:
        """Parse unary operators (negation)."""
        token = self._current_token()
        
        if token and token.value == '-':
            self._advance()
            expr = self._parse_unary()
            return Neg(expr)
        
        return self._parse_primary()
    
    def _parse_primary(self) -> Expression:
        """Parse primary expressions (numbers, variables, functions, parentheses)."""
        token = self._current_token()
        
        if not token:
            raise ValueError("Unexpected end of expression")
        
        # Number
        if token.type == 'NUMBER':
            self._advance()
            return Number(Fraction(token.value))
        
        # Constant
        if token.type == 'CONSTANT':
            self._advance()
            if token.value == 'pi':
                return pi
            elif token.value == 'e':
                return e
            else:
                return Constant(token.value)
        
        # Variable
        if token.type == 'VARIABLE':
            self._advance()
            return Variable(token.value)
        
        # Function
        if token.type == 'FUNCTION':
            func_name = token.value
            self._advance()
            self._expect('(')
            arg = self._parse_expression()
            self._expect(')')
            
            if func_name == 'sin':
                return Sin(arg)
            elif func_name == 'cos':
                return Cos(arg)
            elif func_name == 'tan':
                return Tan(arg)
            elif func_name == 'exp':
                return Exp(arg)
            elif func_name == 'ln':
                return Ln(arg)
            elif func_name == 'log':
                return Log(arg)
            elif func_name == 'sqrt':
                return Sqrt(arg)
            elif func_name == 'abs':
                return Abs(arg)
            else:
                raise ValueError(f"Unknown function: {func_name}")
        
        # Parenthesized expression
        if token.value == '(':
            self._advance()
            expr = self._parse_expression()
            self._expect(')')
            return expr
        
        raise ValueError(f"Unexpected token: {token}")
