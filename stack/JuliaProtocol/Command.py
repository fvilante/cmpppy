# Command primitives
# (Here command concept is looked in relation to Data: See Command/Data relationship in documentation)
import abc
from stack.JuliaProtocol.Symbol_ import Symbol
from typing import Sized, NamedTuple, List
#from typing import NamedTuple, Iterable, List
#from stack.JuliaProtocol.Frame import


# =================================
# DATA MODEL
# ===============================

# --- First-Order primitive abstract commands ---

# ---------------------
# COMMAND
# ---------------------

Command: Sized
class Command(Symbol):
    pass

# ---------------------
# PARAMETER
# -------------------

Parameter = Sized
class Parameter(Symbol):
    pass

FixedSizeParameter = Sized
class FixedSizeParameter(Parameter):
    pass

VariableSizeParameter = Sized
class VariableSizeParameter(Parameter):
    pass



# ---------------------
# COMPOSITION
# -------------------

Parameters = List[Parameter]

class CommandWithParameters(NamedTuple):
    Command: Command
    Parameters: Parameters


# ------------------
# Test
# ------------------

if __name__ == "__main__":


    ps = [Parameter(), FixedSizeParameter(), VariableSizeParameter]
    print(type(ps))
    # EXPECTED ERROR HERE
    # SUBCLASS MUST IMPLEMENT __len__
    for each in ps:
        try:
            len(each)
            raise TypeError
        except:
            print("Ok")
