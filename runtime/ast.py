from abc import ABC, abstractmethod

from attr import dataclass


class Node(ABC):
    def type(self):
        return self.__class__.__name__

@dataclass
class Statement(Node, ABC):
    
    @abstractmethod
    def dict(self):
        pass

@dataclass
class Expression(Node):

    @abstractmethod
    def eval(self):
        return self

    @abstractmethod
    def dict(self):
        pass

@dataclass
class Literal(Expression):
    value: str | int | float | bool
    def eval(self):
        return self.value
    
    def dict(self) -> dict:
        return {
            "type": "Literal",
            "value": self.value
        }
    
@dataclass
class StringLiteral(Literal):
    value: str
    def eval(self):
        return self.value
    def dict(self) -> dict:
        return {
            "type": "StringLiteral",
            "value": self.value
        }
    
@dataclass
class IntLiteral(Literal):
    value: int
    def eval(self):
        return self.value
    def dict(self):
        return {
            "type": "IntLiteral",
            "value": self.value
        }
    
@dataclass
class FloatLiteral(Literal):
    value: float
    def eval(self):
        return self.value
    def dict(self):
        return {
            "type": "FloatLiteral",
            "value": self.value
        }
    
@dataclass
class BoolLiteral(Literal):
    value: bool
    def eval(self):
        return self.value
    def dict(self):
        return {
            "type": "FloatLiteral",
            "value": self.value
        }
    
@dataclass
class UnaryExpression(Expression):
    operator: str
    expression: Expression
    def eval(self):
        if self.operator == "-":
            return -self.expression.eval()
        if self.operator == "!":
            return not self.expression.eval()
        return self.expression.eval()
    
    def dict(self):
        return {
            "type": "UnaryExpression",
            "operator": self.operator,
            "argument": self.expression.dict()
        }

@dataclass
class Program(Statement):
    body: list[Statement]

    def dict(self):
        return {
            "type": self.type(),
            "body": [statement.dict() for statement in self.body]
        }
@dataclass
class Identifier(Expression):
    name: str
    def eval(self):
        return self.name
    
    def dict(self):
        return {
            "type": self.type(),
            "name": self.name
        }
    
@dataclass
class Block(Statement):
    body: list[Statement]

    def dict(self):
        return {
            "type": "Block",
            "body": [statement.dict() for statement in self.body]
        }
@dataclass
class WhileStatement(Statement):
    test: Expression
    body: Block

    def dict(self):
        return {
            "type": "WhileStatement",
            "test": self.test.dict(),
            "body": self.body.dict()
        }
    
@dataclass
class BreakStatement(Statement):

    def dict(self):
        return {
            "type": "BreakStatement"
        }

@dataclass
class ReturnStatement(Statement):
    value: Expression

    def dict(self):
        return {
            "type": "ReturnStatement",
            "value": self.value.dict()
        }

@dataclass
class IfStatement(Statement):
    test: Expression
    consequent: Block
    alternate: Block

    def dict(self):
        return {
            "type": "IfStatement",
            "test": self.test.dict(),
            "consequent": self.consequent.dict(),
            "alternate": self.alternate.dict()
        }

@dataclass
class VariableDeclaration(Statement):
    id: Identifier
    value: Expression

    def dict(self):
        return {
            "type": "VariableDeclaration",
            "id": self.id.dict(),
            "value": self.value.dict()
        }

@dataclass
class Assignment(Statement):
    id: Identifier
    value: Expression

    def dict(self):
        return {
            "type": "Assignment",
            "id": self.id.dict(),
            "value": self.value.dict()
        }
    
@dataclass
class Argument(Expression):
    id: Identifier
    value: Expression

    def dict(self):
        return {
            "type": "Argument",
            "id": self.id.dict(),
            "value": self.value.dict()
        }

@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression

    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if self.operator == "+":
            return left + right
        if self.operator == "-":
            return left - right
        if self.operator == "*":
            return left * right
        if self.operator == "/":
            return left / right
        if self.operator == "%":
            return left % right
        if self.operator == "<":
            return left < right
        if self.operator == ">":
            return left > right
        if self.operator == "<=":
            return left <= right
        if self.operator == ">=":
            return left >= right
        if self.operator == "==":
            return left == right
        if self.operator == "!=":
            return left != right
        if self.operator == "&&":
            return left and right
        if self.operator == "||":
            return left or right
        return None
    
    def dict(self):
        return {
            "type": "BinaryExpression",
            "left": self.left.dict(),
            "operator": self.operator,
            "right": self.right.dict()
        }
    
@dataclass
class CallExpression(Expression):
    callee: Identifier
    arguments: list[Expression]
    def eval(self):
        return self.callee.eval()(*[argument.eval() for argument in self.arguments])
    def dict(self):
        return {
            "type": "CallExpression",
            "callee": self.callee.dict(),
            "arguments": [argument.dict() for argument in self.arguments]
        }

@dataclass
class Fun(Statement):
    params: list[Identifier]
    body: Block

    def dict(self):
        return {
            "type": "Fun",
            "params": [param.dict() for param in self.params],
            "body": self.body.dict()
        }
    
class EmptyStatement(Statement):
    def dict(self):
        return {
            "type": "EmptyStatement"
        }
    