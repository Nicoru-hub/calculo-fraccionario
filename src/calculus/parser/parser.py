from __future__ import annotations

from calculus.parser.tokenizer import Tokenizer, TokenType, Token
from calculus.expressions.base import Expression, Number, Variable, Constant
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.expressions.functions import (
    Sin, Cos, Tan, Cot, Sec, Csc, Exp, Ln, Log, Sqrt, Abs, Gamma
)
from calculus.constants.constants import pi, e, phi
from fractions import Fraction


class Parser:
    """Parse mathematical expressions into AST."""
    
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
    
    @staticmethod
    def parse(text: str) -> Expression:
        """Parse a string into an Expression."""
        tokenizer = Tokenizer(text)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        return parser._parse_expression()
    
    def _current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def _peek_token(self, offset=1) -> Token:
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return self.tokens[-1]  # EOF
    
    def _advance(self):
        self.pos += 1
    
    def _expect(self, token_type: TokenType) -> Token:
        token = self._current_token()
        if token.type != token_type:
            raise ValueError(f"Expected {token_type}, got {token.type}")
        self._advance()
        return token
    
    def _parse_expression(self) -> Expression:
        """Parse addition/subtraction (lowest precedence)."""
        left = self._parse_term()
        
        while self._current_token().type in (TokenType.PLUS, TokenType.MINUS):
            if self._current_token().type == TokenType.PLUS:
                self._advance()
                right = self._parse_term()
                left = Add(left, right)
            else:  # MINUS
                self._advance()
                right = self._parse_term()
                left = Sub(left, right)
        
        return left
    
    def _parse_term(self) -> Expression:
        """Parse multiplication/division."""
        left = self._parse_unary()
        
        while self._current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            if self._current_token().type == TokenType.MULTIPLY:
                self._advance()
                right = self._parse_unary()
                left = Mul(left, right)
            else:  # DIVIDE
                self._advance()
                right = self._parse_unary()
                left = Div(left, right)
        
        return left
    
    def _parse_unary(self) -> Expression:
        """Parse unary operators and handle implicit multiplication."""
        if self._current_token().type == TokenType.MINUS:
            self._advance()
            expr = self._parse_unary()
            return Neg(expr)
        
        return self._parse_power()
    
    def _parse_power(self) -> Expression:
        """Parse exponentiation (right-associative)."""
        left = self._parse_atom()
        
        if self._current_token().type in (TokenType.POWER,):
            self._advance()
            right = self._parse_power()  # Right-associative
            return Pow(left, right)
        
        return left
    
    def _parse_atom(self) -> Expression:
        """Parse atoms: numbers, variables, constants, functions, parentheses."""
        token = self._current_token()
        
        if token.type == TokenType.NUMBER:
            self._advance()
            # Parse as fraction
            if "." in token.value:
                frac = Fraction(token.value).limit_denominator()
            else:
                frac = Fraction(int(token.value))
            return Number(frac)
        
        elif token.type == TokenType.VARIABLE:
            self._advance()
            return Variable(token.value)
        
        elif token.type == TokenType.CONSTANT:
            self._advance()
            if token.value == "pi":
                return pi
            elif token.value == "e":
                return e
            elif token.value == "phi":
                return phi
            else:
                return Constant(token.value)
        
        elif token.type == TokenType.FUNCTION:
            func_name = token.value
            self._advance()
            self._expect(TokenType.LPAREN)
            arg = self._parse_expression()
            self._expect(TokenType.RPAREN)
            
            # Map function name to class
            func_map = {
                "sin": Sin, "cos": Cos, "tan": Tan, "cot": Cot,
                "sec": Sec, "csc": Csc, "exp": Exp, "ln": Ln,
                "log": Log, "sqrt": Sqrt, "abs": Abs, "gamma": Gamma
            }
            
            if func_name in func_map:
                return func_map[func_name](arg)
            else:
                raise ValueError(f"Unknown function: {func_name}")
        
        elif token.type == TokenType.LPAREN:
            self._advance()
            expr = self._parse_expression()
            self._expect(TokenType.RPAREN)
            return expr
        
        else:
            raise ValueError(f"Unexpected token: {token.type}")
