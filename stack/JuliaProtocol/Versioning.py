# Julia Versioning Policy System
from stack.JuliaProtocol.Common import DateTime
#
from typing import NamedTuple, Tuple, Optional


# --------------------
#   DATA MODEL
# --------------------

# semver format
# USES:
# mayor => if you change the interface or compromise backwards compatibility someway
# minor => Improvements fully backward compatible
# revision => hotfixes
SemVer_Version = Tuple[int, int, int]
Hash = Optional[str] # some hash checksum


class Version(NamedTuple):
    product: str
    version: SemVer_Version
    date: DateTime
    hash: Hash

    @property
    def mayor(self):
        (v, _, _) = self.version
        return v

    @property
    def minor(self):
        (_, v, _) = self.version
        return v

    @property
    def revision(self):
        (_, _, v) = self.version
        return v


# ----------------------
#  Instantiation
# ----------------------
__version__ = Version( "Julia SemVer Version Controller", (0,0,1),(6,9,18), None)


# Todo : Create a preprocessor compiler, to parse production code. (or any other solution)
# if versioning not implemented yet
FakeVersion = Version( "Fake versioner", (0,0,1),(6,9,18), None)


# --------------------
# Test
# --------------------

if __name__ == "__main__":

    print(__version__)