import re
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


def exec_re(r, i):
    print("Searching '" + i + "' for regex :" + r.pattern)
    worked = r.search(i) is not None
    print("Got: ", worked)
    return worked

def parse_scond(tokens, d):
    print(d + "parse_scond " + tokens.peek().string)
    val = expect(tokens, tokenize.STRING)
    terminal_regex = re.compile(val.string[1:-1]) # need to trim the quotes!
    return lambda input: exec_re(terminal_regex, input)


def parse_cond(tokens, d):
    print(d + "parse_cond " + tokens.peek().string)
    l = parse_scond(tokens, d + "  ")
    if tokens.peek().string == "AND":
        print(d + "AND")
        tokens.next() # throw it away!
        r = parse_cond(tokens, d + "  ")
        return lambda line: l(line) and r(line)
    else:
        return l

def parse_clause(tokens, d):
    print(d + "parse_clause " + tokens.peek().string)
    a_or_r = expect(tokens, tokenize.NAME)
    l = parse_cond(tokens, d + "  ")
    if a_or_r.string == "accept":
        return l
    elif a_or_r.string == "reject":
        return lambda line: not l(line)
    else:
        assert(False)

def parse_clauses(tokens, d):
    print(d + "parse_clauses " + tokens.peek().string)
    clauses = []
    while tokens.peek().type == tokenize.NAME:
        clauses.append(parse_clause(tokens, d + "  "))

    return clauses
    next = tokens.peek()
    if next.type != tokenize.NAME:
        return []
    clause = parse_clause(tokens, d + "  ")
    clauses = parse_clauses(tokens, d + "  ")
    print(d + "clauses: ", clauses)
    return clauses.append(clause)


def parse(line):
    [name, rules] = line.split(": ", 1)
    tokens = Tokens(rules)
    clauses = parse_clauses(tokens, "")
    expect(tokens, tokenize.ENDMARKER)
    return (name, clauses)

def execute(clauses, input):
    return all([clause(input) for clause in clauses])
