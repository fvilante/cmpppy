# Data primitives
# (Here command concept is looked in relation to Data: See Command/Data relationship in documentation)
from stack.JuliaProtocol.Symbol_ import Symbol


# =================================
# DATA MODEL
# ===============================


# --- First-Order primitive abstract data ---


class Data(Symbol):
    pass


# ------------------
# Test
# ------------------

if __name__ == "__main__":

    s = Data()
    print(type(s))




