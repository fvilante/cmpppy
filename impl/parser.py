# Author: Flavio Vilante
# Date: 07/08/2018

from typing import Tuple, Optional, Union, List, Callable, cast
from functools import partial

FlowChannel = Union['Remaining', 'Fail']
Unit = int  # base unit of analysis
InputQueue = Optional[List[Unit]]
ErrorMessage = str
Parser = Callable[[InputQueue], FlowChannel]

class PassThrough:
    def __init__(self, remaining: InputQueue, matchedValue: Optional[Unit]) -> None:
        self._remaining: InputQueue = remaining
        self._matchedValue = matchedValue

    def __repr__(self):
        return f"Match: {self._matchedValue}, Remaining:{self._remaining}\n"

    @property
    def remaining(self):
        return self._remaining

    @property
    def matched(self):
        return self._matchedValue

class Fail:
    def __init__(self, error_msg: ErrorMessage) -> None:
        self.error_msg = error_msg

    def __repr__(self):
        str_ = self.error_msg + "\n"
        return str_


def coreParser(input_: InputQueue, toMatch: Optional[Unit], blockIfNoMatch:bool) -> FlowChannel:

    if input_ is None:
        return Fail(f"No more input")
    else:
        if input_[0] == toMatch:
            return PassThrough(input_[1:], toMatch)
        elif blockIfNoMatch:
            return Fail(f"Fail: Expecting chr={toMatch}. Got chr={input_[0]}.")
        else:
            return PassThrough(input_[0:], None)


def run(parser: Parser, inputQueue_: InputQueue) -> FlowChannel:
    return parser(inputQueue_)


ESC = 27
STX = 2
ACK = 6
NACK = 21
ETX = 3

coreParser_blocked = partial(coreParser, blockIfNoMatch=True)
coreParser_opened = partial(coreParser, blockIfNoMatch=False)

#blocked
escParser_blocked = partial(coreParser_blocked, toMatch=ESC)
# opended
escParser = partial(coreParser_opened, toMatch=ESC)
stxParser = partial(coreParser_opened, toMatch=STX)
ackParser = partial(coreParser_opened, toMatch=ACK)
nackParser = partial(coreParser_opened, toMatch=NACK)
etxParser = partial(coreParser_opened, toMatch=ETX)


'''
def mapP(func, parser, input_):
    result = run(parser, input_)
    if is_success(result):
        result2 = list(map(func,result.matched))
        return result2
    else:
        return result # fail
'''


def andThen(p1: Parser, p2: Parser, input_: InputQueue) -> FlowChannel:

    res1 = run(p1, input_)
    if type(res1) is Fail:
        return res1
    else:
        res1 = cast(PassThrough, res1)
        res2 = run(p2, res1.remaining)
        return res2

esc_stx = lambda x: andThen(escParser, stxParser, x)
esc_etx = lambda x: andThen(escParser, etxParser, x)

def terminalBlockParser(input_: InputQueue, termparser: Parser) -> FlowChannel:
    if input_ is None:
        return Fail(f"No more input")


        return PassThrough(input_[0:], None)





test = lambda x: andThen(esc_stx, esc_etx, x)

if __name__ == "__main__":

    packet = [27,2,0,0,1,10,27,3,130]

    print(f"Parssing: {packet}\n")
    a = run(test, packet)


    print(a)



