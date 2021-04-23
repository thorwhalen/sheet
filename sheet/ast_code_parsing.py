"""Tools to parse code"""
import re
from ast import parse as ast_parse
from enum import Enum

try:
    # Try ast.parse (3.9+)
    from ast import unparse as ast_unparse
except ImportError:
    try:
        from astunparse import unparse as ast_unparse
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "Can't find a ast unparse function -- you'll need python 3.9+ or (pip/conda) install astunparse")


def code_blocks(code_str: str, include_line_numbers=True):
    """Extract code blocks from code_str

    :param code_str: String containing valid python code
    :return: A generator of valid python code blocks, extracted sequentially from code_str

    >>> code_str = '''
    ... def foo(a, b):
    ...     return a + b
    ...
    ... foo(
    ...     a=1,
    ...     b=2
    ... )
    ... '''
    >>> blocks = list(code_blocks(code_str))
    >>> len(blocks)
    2
    >>> lineno, block = blocks[0]
    >>> lineno  # note that line numbers start at 1 (not like lists that start at 0)
    2
    >>> print(block)
    def foo(a, b):
        return (a + b)
    >>> lineno, block = blocks[1]
    >>> lineno
    5
    >>> print(block)
    foo(a=1, b=2)

    """
    if include_line_numbers:
        for ast_obj in ast_parse(code_str).body:
            yield ast_obj.lineno, ast_unparse(ast_obj).strip()
    else:
        for ast_obj in ast_parse(code_str).body:
            yield ast_unparse(ast_obj).strip()


single_leading_space = re.compile(r'^\s')
assert list(map(lambda x: single_leading_space.sub('', x),
                ['no space', ' one space', '  two spaces'])) == ['no space', 'one space', ' two spaces']

all_space = re.compile(r'^\s*$')
assert list(map(lambda x: bool(all_space.match(x)),
                [' \t\n\r', ' some non space'])) == [True, False]

line_starts_with_comment_re = re.compile(r'^\s*#')

_test_examples = [
    '# comment',
    '  \t  # comment',
    '# comment # another',
    '  this is # comment'
]

assert list(map(lambda x: bool(line_starts_with_comment_re.match(x)),
                _test_examples)) == [True, True, True, False]

Annot = Enum('Annot', 'CODE COMMENT SPACE')


def annotate_lines(code_str):
    r"""Generate (annotation, line) pairs where annotation indicates if the line is a (Annot).CODE, .COMMENT or .SPACE

    >>> from inspect import getsource
    >>>
    >>> lines_to_skip = len(annotate_lines.__doc__.split('\n')) + 1  # need this to avoid docs
    >>> annotated_lines = annotate_lines(getsource(annotate_lines))
    >>> for annot, line in list(annotated_lines)[lines_to_skip:]:  # doctest: +NORMALIZE_WHITESPACE
    ...     print(annot, line)
    Annot.CODE     for line in code_str.splitlines():
    Annot.CODE         m = line_starts_with_comment_re.match(line)
    Annot.SPACE
    Annot.COMMENT         # TODO: Consider using Pattern Matching when python 3.10 comes along
    Annot.CODE         if m:
    Annot.CODE             yield Annot.COMMENT, line
    Annot.CODE         elif all_space.match(line):
    Annot.CODE             yield Annot.SPACE, line
    Annot.CODE         else:  # assume it's code and return (annotated) line as is
    Annot.CODE             yield Annot.CODE, line

    """
    for line in code_str.splitlines():
        m = line_starts_with_comment_re.match(line)

        # TODO: Consider using Pattern Matching when python 3.10 comes along
        if m:
            yield Annot.COMMENT, line
        elif all_space.match(line):
            yield Annot.SPACE, line
        else:  # assume it's code and return (annotated) line as is
            yield Annot.CODE, line


#single_leading_space.sub('', line[m.end(0):])

class MyMixin:
    def foo(self):
        return self.x + self.y


class A(MyMixin):
    def __init__(self, x=0):
        self.x = x


a = A(10)  # no problem
a.foo()  # problem!