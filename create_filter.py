import tokenize
from io import StringIO

# GRAMMAR:
# S       ::= CLAUSES
# CLAUSES ::= CLAUSE CLAUSES | e
# CLAUSE  ::= accept COND | reject COND
# COND    ::= SCOND and COND | SCOND
# SCOND   ::= quoted_regex

def tokenize_line(line):
    return tokenize.generate_tokens(StringIO(line).readline)
    
