import tokenize
from io import StringIO
import itertools

# GRAMMAR:
# S       ::= CLAUSES END
# CLAUSES ::= CLAUSE CLAUSES | e
# CLAUSE  ::= accept COND | reject COND
# COND    ::= SCOND and COND | SCOND
# SCOND   ::= quoted_regex

def tokenize_line(line):
    return tokenize.generate_tokens(StringIO(line).readline)


class Tokens:
    def __init__(self, line):
        self.token_generator = tokenize_line(line)


    def peek(self):
        val = self.token_generator.__next__()
        self.token_generator = itertools.chain([val], self.token_generator)
        return val


    def next(self):
        return self.token_generator.__next__()


    def __next__(self):
        return self.next()


def expect(tokens, type):
    assert(tokens.peek().type == type)
    return tokens.next()


def parse_scond(tokens, d):
    #print(d + "parse_scond")
    val = expect(tokens, tokenize.STRING)
    print(val.string)

def parse_cond(tokens, d):
    #print(d + "parse_cond")
    parse_scond(tokens, d + "  ")
    if tokens.peek().string == "AND":
        print(d + "AND")
        tokens.next() # throw it away!
        parse_cond(tokens, d + "  ")

def parse_clause(tokens, d):
    #print(d + "parse_clause")
    a_or_r = expect(tokens, tokenize.NAME)
    if a_or_r.string == "accept":
        print("Accepting:")
        parse_cond(tokens, d + "  ")
    elif a_or_r.string == "reject":
        print("Rejecting:")
        parse_cond(tokens, d + "  ")
    else:
        assert(False)

def parse_clauses(tokens, d):
    #print(d + "parse_clauses")
    next = tokens.peek()
    if next.type != tokenize.NAME:
        return None
    parse_clause(tokens, d + "  ")
    parse_clauses(tokens, d + "  ")


def parse(line):
    tokens = Tokens(line)
    clauses = parse_clauses(tokens, "")
    expect(tokens, tokenize.ENDMARKER)
