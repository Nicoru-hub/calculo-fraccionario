from __future__ import annotations

from enum import Enum, auto
from dataclasses import dataclass
import re


class TokenType(Enum):
    # Literals
    NUMBER = auto()
    VARIABLE = auto()
    CONSTANT = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    
    # Functions
    FUNCTION = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    
    # Special
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    position: int


class Tokenizer:
    """Tokenize mathematical expressions."""
    
    CONSTANTS = {"pi", "e", "phi"}
    FUNCTIONS = {
        "sin", "cos", "tan", "cot", "sec", "csc",
        "exp", "ln", "log", "sqrt", "abs", "gamma"
    }
    OPERATORS = {"+", "-", "*", "/", "^", "**"}
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.tokens = []
    
    def tokenize(self) -> list[Token]:
        """Convert text into tokens."""
        while self.pos < len(self.text):
            self._skip_whitespace()
            if self.pos >= len(self.text):
                break
            
            char = self.text[self.pos]
            
            if char == "(":
                self.tokens.append(Token(TokenType.LPAREN, "(", self.pos))
                self.pos += 1
            elif char == ")":
                self.tokens.append(Token(TokenType.RPAREN, ")", self.pos))
                self.pos += 1
            elif char == ",":
                self.tokens.append(Token(TokenType.COMMA, ",", self.pos))
                self.pos += 1
            elif char == "+":
                self.tokens.append(Token(TokenType.PLUS, "+", self.pos))
                self.pos += 1
            elif char == "-":
                self.tokens.append(Token(TokenType.MINUS, "-", self.pos))
                self.pos += 1
            elif char == "*":
                if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == "*":
                    self.tokens.append(Token(TokenType.POWER, "**", self.pos))
                    self.pos += 2
                else:
                    self.tokens.append(Token(TokenType.MULTIPLY, "*", self.pos))
                    self.pos += 1
            elif char == "/":
                self.tokens.append(Token(TokenType.DIVIDE, "/", self.pos))
                self.pos += 1
            elif char == "^":
                self.tokens.append(Token(TokenType.POWER, "^", self.pos))
                self.pos += 1
            elif char.isdigit() or (char == "." and self._peek().isdigit()):
                self._tokenize_number()
            elif char.isalpha() or char == "_" or char == "π" or char == "φ":
                self._tokenize_identifier()
            else:
                raise ValueError(f"Unexpected character: {char!r} at position {self.pos}")
        
        self.tokens.append(Token(TokenType.EOF, "", self.pos))
        return self.tokens
    
    def _skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1
    
    def _peek(self, offset=1):
        if self.pos + offset < len(self.text):
            return self.text[self.pos + offset]
        return ""
    
    def _tokenize_number(self):
        """Parse a number (integer or float)."""
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == "."):
            self.pos += 1
        value = self.text[start:self.pos]
        self.tokens.append(Token(TokenType.NUMBER, value, start))
    
    def _tokenize_identifier(self):
        """Parse a variable, constant, or function name."""
        start = self.pos
        
        # Handle special constants
        if self.text[self.pos] == "π":
            self.tokens.append(Token(TokenType.CONSTANT, "pi", start))
            self.pos += 1
            return
        if self.text[self.pos] == "φ":
            self.tokens.append(Token(TokenType.CONSTANT, "phi", start))
            self.pos += 1
            return
        
        # Parse identifier
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == "_"):
            self.pos += 1
        
        value = self.text[start:self.pos]
        
        if value in self.CONSTANTS:
            self.tokens.append(Token(TokenType.CONSTANT, value, start))
        elif value in self.FUNCTIONS:
            self.tokens.append(Token(TokenType.FUNCTION, value, start))
        else:
            # Single letter variables like x, y, t, z
            if len(value) == 1 and value.isalpha():
                self.tokens.append(Token(TokenType.VARIABLE, value, start))
            else:
                # Try to match multi-letter variables
                self.tokens.append(Token(TokenType.VARIABLE, value, start))
