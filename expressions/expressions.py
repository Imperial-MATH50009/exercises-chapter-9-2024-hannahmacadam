import numbers

class Expression:

    def __init__(self, *operands):
        operands = list(operands)
        for i in range(len(operands)):
            if isinstance(operands[i], numbers.Number):
                operands[i] = Number(operands[i])
        
        operands = tuple(operands)
        self.operands = (operands)
"""
    def __add__(self, other):
        if isinstance(other, numbers.Number):
            return Add(self, Number(other))
        else:
            return Add(self, other)

    def __sub__(self, other):
        if isinstance(other, numbers.Number):
            return Sub(self, Number(other))
        else:
            return Sub(self, other)

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Mul(self, Number(other))
        else:
            return Mul(self, other)

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            return Div(self, Number(other))
        else:
            return Div(self, other)

    def __pow__(self, other):
        if isinstance(other, numbers.Number):
            return Pow(self, Number(other))
        else:
            return Pow(self, other)
"""

def __add__(self, other):
    if not isinstance(other, Expression):
        if isinstance(other, numbers.Number):
            other = Number(other)
        else:
            raise TypeError(f"Unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")
    return Add(self, other)

def __sub__(self, other):
    if not isinstance(other, Expression):
        if isinstance(other, numbers.Number):
            other = Number(other)
        else:
            raise TypeError(f"Unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")
    return Sub(self, other)

def __mul__(self, other):
    if not isinstance(other, Expression):
        if isinstance(other, numbers.Number):
            other = Number(other)
        else:
            raise TypeError(f"Unsupported operand type(s) for *: '{type(self).__name__}' and '{type(other).__name__}'")
    return Mul(self, other)

def __truediv__(self, other):
    if not isinstance(other, Expression):
        if isinstance(other, numbers.Number):
            other = Number(other)
        else:
            raise TypeError(f"Unsupported operand type(s) for /: '{type(self).__name__}' and '{type(other).__name__}'")
    return Div(self, other)

def __pow__(self, other):
    if not isinstance(other, Expression):
        if isinstance(other, numbers.Number):
            other = Number(other)
        else:
            raise TypeError(f"Unsupported operand type(s) for ** or ^: '{type(self).__name__}' and '{type(other).__name__}'")
    return Pow(self, other)

class Operator(Expression):

    def __repr__(self):
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        str_operands = []
        for o in self.operands:
            if o.precedence < self.precedence:
                str_operands += [f"({str(o)})"]
            else:
                str_operands += [str(o)]
        return self.symbol.join(str_operands)


class Add(Operator):

    precedence = 0
    symbol = ' + '


class Sub(Operator):

    precedence = 0
    symbol = ' - '


class Mul(Operator):

    precedence = 1
    symbol = ' * '


class Div(Operator):

    precedence = 1
    symbol = ' / '


class Pow(Operator):

    precedence = 2
    symbol = ' ^ '


class Terminal(Expression):

    precedence = 3

    def __init__(self, value):
        self.value = value
        super().__init__(())

    def __repr__(self):
        return repr(self.value)
    
    def __str__(self):
        return str(self.value)

class Symbol(Terminal):

    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError('Symbol must take a string')
        else:
            super().__init__(value)


class Number(Terminal):
    
    def __init__(self, value):
        if not isinstance(value, numbers.Number):
            raise TypeError('Number must take a number')
        else:
            super().__init__(value)
