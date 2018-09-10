# Maybe haskall study
from typing import Callable, Any, List, Type, Union, Optional, TypeVar, Generic, cast, NamedTuple
from Data_T import Data, _None_

T = TypeVar('T')


def _eq_(me, other):
    if (me._content == other._content):
        return True
    else:
        return False

class _Just_(Generic[T]):
    def __init__(self, just: T) -> None:
        self._content: T = just
    def isJust(self):
        return True
    def isNothing(self):
        return False
    def __repr__(self):
        return f'[Just:{self._content}]'
    def __eq__(self, other):
        return _eq_(self, other)


Just_ = Any
Just = _Just_[Any]
def just(x: Just_) -> Just:
    return _Just_(x)


class _Nothing_:
    def __init__(self) -> None:
        self._content = None
        self._nothing: bool = True
    def isNothing(self):
        return True
    def isJust(self):
        return False
    def __repr__(self):
        return f'[Nothing:]'
    def __eq__(self, other):
        return _eq_(self, other)


#Nothing_ = None
Nothing = _Nothing_
def nothing() -> Nothing:
    return _Nothing_()


class _Maybe_(Generic[T]):
    def __init__(self, just: Optional[_Just_[T]], nothing: bool) -> None:
        self._content: Optional[_Just_[T]]
        self._nothing: bool # todo: isNothing would be a better name
        if nothing:
            self._content = None
            self._nothing = nothing
        else: # Just
            self._content = just
            self._nothing = False

    def isJust(self):
        return not self._nothing

    def isNothing(self):
        return not self.isJust()

    def __repr__(self):
        if self.isJust():
            s = f'[self._just]'
        else:
            s = f'[Nothing:()]'
        return s
    def __eq__(self, other):
        return _eq_(self, other)


# Constructor Maybe
Maybe_ = Union[Just, Nothing]
Maybe = _Maybe_[Any]
def maybe(a: Maybe_)  -> Maybe:
    if isinstance(a,  type(just(a))):
        return _Maybe_(just=a, nothing=False)
    elif isinstance(a, type(nothing())):
        return _Maybe_(just=None, nothing=True)
    elif isinstance(a, type(just(lambda x:x))):
        print("oi")
        raise
    else:
        raise



def isJust(a: _Maybe_) -> bool:
    print(a)
    return a.isJust()





'''

def isNothing(a: Maybe) -> bool:
    return not isJust(a)

# extract just from maybe or error if nothing
def fromJust(a: Maybe) -> Just:
    if isinstance(a, type(just(a))):
        return a
    else:
        raise

# allow default a maybe result if the maybe contains nothing
def fromMaybe(a: Just, b: Maybe) -> Data[Just]:
    if isJust(b):
        return fromJust(b)
    elif isNothing(b):
        return just(a)
    else:
        raise

'''

if __name__ == "__main__":


    # just
    b: Just = just(1)
    assert(b._content == 1)
    assert(b == just(1))
    assert(b.isJust() == True)
    assert (b.isNothing() == False)
    # reveal_type(a)
    # reveal_type(b)

    #Nothing
    c: Nothing = nothing()
    assert(c._content == None)
    assert(c == nothing())
    assert (c.isJust() == False)
    assert (c.isNothing() == True)
    # reveal_type(a)
    # reveal_type(b)


    #Maybe
    j: Maybe = maybe(just(2))
    assert(j == maybe(just(2)))
    assert(j._content == just(2))
    assert(j.isJust() == True)
    assert (j.isNothing() == False)

    n: Maybe = maybe(nothing())
    assert (n == maybe(nothing()))
    assert (n._content == None)
    assert (n.isJust() == False)
    assert (n.isNothing() == True)

    x = isJust(maybe(just(2)))
    assert(x == True)
    assert (True == isJust(maybe(just(  ((2+2+2)/6)*10   )) ))
    f = lambda x:x+2
    assert (True == isJust(maybe(f              )))
    y = isJust(maybe(nothing()))
    print(y)
    assert (y == False)

    #n = maybe(nothing())

    #print(n)

'''
    #d = maybe(nothing())
    #print(d)
    #print(type(d))

    #Is just
    print("--")
    f = lambda  : just(1+2)
    true = isJust(f())
    assert(true == True)
    print(nothing())
    print(just(2+10))
    #reveal_type(nothing())
    n : Data[None]  = nothing()
    false : bool = isJust(maybe(nothing()))
    print(false)
    assert(false == False)


    # isNothing   
    assert(isNothing(d)==False)
    print(nothing())
    assert(isNothing(nothing()) == True)

    assert( isJust(just(1+2)) == True)
    assert(isJust(f()) == True)
    fromJust(f())
    #fromJust(None)

    #from maybe
    calc = nothing()
    print( fromMaybe("Erro", calc) )
'''