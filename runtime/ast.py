from abc import ABC, abstractmethod

from attr import dataclass

from runtime.runtime import Runtime

class Node(ABC):
    pass

@dataclass
class Statement(Node, ABC):
    
    def exec(self, env: Runtime):
        pass

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

    def exec(self, env: Runtime):
        for statement in self.body:
            statement.exec(env)

    def dict(self):
        return {
            "type": "Program",
            "body": [statement.dict() for statement in self.body]
        }
@dataclass
class Identifier(Expression):
    name: str
    def eval(self):
        return self.name
    
    def dict(self):
        return {
            "type": "Identifier",
            "name": self.name
        }
    
@dataclass
class Block(Statement):
    body: list[Statement]

    def exec(self, env: Runtime):
        context = Runtime(env)
        for statement in self.body:
            statement.exec(context)

    def dict(self):
        return {
            "type": "Block",
            "body": [statement.dict() for statement in self.body]
        }
    
@dataclass
class VariableDeclaration(Statement):
    id: Identifier
    value: Expression

    def exec(self, env: Runtime):
        env.context.set_value(self.id.name, self.value.eval())

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

    def exec(self, env: Runtime):
        if not env.context.has_value(self.id.name):
            raise Exception(f"Variable {self.id.name} not defined")
        env.context.set_value(self.id.name, self.value.eval())

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
    
