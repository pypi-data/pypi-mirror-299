"""Unicode Characters"""
import string
def letters():
    """All Alhabet letters"""
    string.ascii_letters
def upperletters():
    """Letters Upper"""
    string.ascii_uppercase
def lowerletters():
    """letters lower"""
    string.ascii_lowercase
class Unicodeupper:
    for code in range(65,91):
        print(chr(code),end="")
    print("")
class Unicodelower:
    for codel in range(65,91):
        print(chr(codel).lower(),end="")
    print("")
class UnicodeSymbols:
    """keyboard and charaters symbols"""
    for symb in range(170,3000):
        print(chr(symb),end="")
    print("")
