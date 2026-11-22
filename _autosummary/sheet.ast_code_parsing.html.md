# sheet.ast_code_parsing

Tools to parse code

### Functions

| [`annotate_lines`](#sheet.ast_code_parsing.annotate_lines)(code_str)                      | Generate (annotation, line) pairs where annotation indicates if the line is a (Annot).CODE, .COMMENT or .SPACE   |
|------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| [`code_blocks`](#sheet.ast_code_parsing.code_blocks)(code_str[, include_line_numbers]) | Extract code blocks from code_str                                                                                |

### Classes

| [`Annot`](#sheet.ast_code_parsing.Annot)(\*values)   |    |
|--------------------------------------------------------------------|----|

### *class* sheet.ast_code_parsing.Annot(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

### sheet.ast_code_parsing.annotate_lines(code_str)

Generate (annotation, line) pairs where annotation indicates if the line is a (Annot).CODE, .COMMENT or .SPACE

```pycon
>>> from inspect import getsource
>>>
>>> lines_to_skip = len(annotate_lines.__doc__.split('\n')) + 1  # need this to avoid docs
>>> annotated_lines = annotate_lines(getsource(annotate_lines))
>>> for annot, line in list(annotated_lines)[lines_to_skip:]:
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
```

### sheet.ast_code_parsing.code_blocks(code_str, include_line_numbers=True)

Extract code blocks from code_str

* **Parameters:**
  **code_str** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – String containing valid python code
* **Returns:**
  A generator of valid python code blocks, extracted sequentially from code_str

```pycon
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
    return a + b
>>> lineno, block = blocks[1]
>>> lineno
5
>>> print(block)
foo(a=1, b=2)
```
