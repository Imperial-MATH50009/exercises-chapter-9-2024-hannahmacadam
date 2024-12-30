"""Implement operation hierarchy and differentiation for expressions."""

import numbers
from functools import singledispatch


class Expression:
    """Define super class expression."""

    def __init__(self, *operands):
        """Initialise."""
        operands = list(operands)
        for i in range(len(operands)):
            if isinstance(operands[i], numbers.Number):
                operands[i] = Number(operands[i])

        operands = tuple(operands)
        self.operands = operands

    def __add__(self, other):
        """Define addition of expressions."""
        if isinstance(other, numbers.Number):
            return Add(self, Number(other))
        else:
            return Add(self, other)

    def __radd__(self, other):
        """Define reverse addition of expressions."""
        if isinstance(other, numbers.Number):
            return Add(Number(other), self)
        else:
            raise TypeError(
                f"Unsupported operand type(s) for +: '{type(other).__name__}' \
                and '{type(self).__name__}'"
                           )

    def __sub__(self, other):
        """Define subtraction of expressions."""
        if isinstance(other, numbers.Number):
            return Sub(self, Number(other))
        else:
            return Sub(self, other)

    def __rsub__(self, other):
        """Define reverse subtraction of expressions."""
        if isinstance(other, numbers.Number):
            return Sub(Number(other), self)
        else:
            raise TypeError(
                f"Unsupported operand type(s) for -: '{type(other).__name__}' \
                and '{type(self).__name__}'")

    def __mul__(self, other):
        """Define multiplication of expressions."""
        if isinstance(other, numbers.Number):
            return Mul(self, Number(other))
        else:
            return Mul(self, other)

    def __rmul__(self, other):
        """Define reverse multiplication of expressions."""
        if isinstance(other, numbers.Number):
            return Mul(Number(other), self)
        else:
            raise TypeError(
                f"Unsupported operand type(s) for *: '{type(other).__name__}' \
                and '{type(self).__name__}'")

    def __truediv__(self, other):
        """Define division of expressions."""
        if isinstance(other, numbers.Number):
            return Div(self, Number(other))
        else:
            return Div(self, other)

    def __rtruediv__(self, other):
        """Define reverse division of expressions."""
        if isinstance(other, numbers.Number):
            return Div(Number(other), self)
        else:
            raise TypeError(
                f"Unsupported operand type(s) for /: '{type(other).__name__}' \
                and '{type(self).__name__}'")

    def __pow__(self, other):
        """Define exponentiation of expressions."""
        if isinstance(other, numbers.Number):
            return Pow(self, Number(other))
        else:
            return Pow(self, other)

    def __rpow__(self, other):
        """Define reverse exponentiation of expressions."""
        if isinstance(other, numbers.Number):
            return Pow(Number(other), self)
        else:
            raise TypeError(
                f"Unsupported operand type(s) for **: '{type(other).__name__}'\
                and '{type(self).__name__}'")


class Operator(Expression):
    """Define the Operator subclass of Expression."""

    def __repr__(self):
        """Implement representation of expressions."""
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        """Implement string representation of expressions."""
        str_operands = []
        for o in self.operands:
            if o.precedence < self.precedence:
                str_operands += [f"({str(o)})"]
            else:
                str_operands += [str(o)]
        return self.symbol.join(str_operands)


class Add(Operator):
    """Define the Add subclass of Operator."""

    precedence = 0
    symbol = ' + '


class Sub(Operator):
    """Define the Subtract subclass of Operator."""

    precedence = 0
    symbol = ' - '


class Mul(Operator):
    """Define the Multiply subclass of Operator."""

    precedence = 1
    symbol = ' * '


class Div(Operator):
    """Define the Division subclass of Operator."""

    precedence = 1
    symbol = ' / '


class Pow(Operator):
    """Define the Power subcalss of Operator."""

    precedence = 2
    symbol = ' ^ '


class Terminal(Expression):
    """Define the Terminal sublass of Operator."""

    precedence = 3

    def __init__(self, value):
        """Initialise."""
        self.value = value
        super().__init__()

    def __repr__(self):
        """Implement representation of Terminals."""
        return repr(self.value)

    def __str__(self):
        """Implement string representation of Terminals."""
        return str(self.value)


class Symbol(Terminal):
    """Define Symbol subclass of Terminal."""

    def __init__(self, value):
        """Initialize."""
        if not isinstance(value, str):
            raise TypeError('Symbol must take a string')
        else:
            super().__init__(value)


class Number(Terminal):
    """Define Number subclass of Terminal."""

    def __init__(self, value):
        """Initialize."""
        if not isinstance(value, numbers.Number):
            raise TypeError('Number must take a number')
        else:
            super().__init__(value)


def postvisitor(expr, fn, **kwargs):
    """Visit nodes of a tree in post order.

    Execute a function, visiting each node only once.
    """
    stack = []
    visited = {}
    stack += [expr]
    while stack:
        e = stack.pop()
        unvisited_children = []
        for o in e.operands:
            if o not in visited:
                unvisited_children += [o]

        if unvisited_children:
            stack += [e]
            stack += unvisited_children
        else:
            visited[e] = fn(e,
                            *(visited[o] for o in e.operands),
                            **kwargs)
    return visited[expr]


@singledispatch
def differentiate(expr, *o, **kwargs):
    """Differentiate an expression node.

    Parameters
    ----------
    expr: Expression
        The expression node to be differentiated.
    *o: Expression
        The results of differentiating the operands of expr.
    **kwargs:
        Any keyword arguments required to differentiate specific types of
        expression.
    var: string
        A string representing the symbol to differentiate with respect to.
    """
    raise NotImplementedError(
        f"Cannot differentiate a {type(expr).__name__}")


@differentiate.register(numbers.Number)
def _(expr, *o, **kwargs):
    return 0


@differentiate.register(Number)
def _(expr, *o, **kwargs):
    return 0


@differentiate.register(Symbol)
def _(expr, *o, var, **kwargs):
    if str(expr) == var:
        return 1
    else:
        return 0


@differentiate.register(Add)
def _(expr, *o, **kwargs):
    return o[0] + o[1]


@differentiate.register(Sub)
def _(expr, *o, **kwargs):
    return o[0] - o[1]


@differentiate.register(Mul)
def _(expr, *o, **kwargs):
    return expr.operands[0] * o[1] + expr.operands[1] * o[0]


@differentiate.register(Div)
def _(expr, *o, **kwargs):
    num = expr.operands[1] * o[0] - expr.operands[0] * o[1]
    denom = expr.operands[1] ** 2
    return num / denom


@differentiate.register(Pow)
def _(expr, *o, **kwargs):
    e0 = o[0]
    e1 = expr.operands[1] * expr.operands[0] ** (expr.operands[1] - 1)
    return e0 * e1
