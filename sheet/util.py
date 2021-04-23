"""General utils"""
import tokenize
from itertools import groupby
from io import BytesIO

from typing import Callable


# NothingYet = type('NothingYet', (object,), {})
#
#
# def item_groups(item_gen, item_to_group, mk_item_container=list, clear_item_container: Callable = list.clear):
#     """A generator of (group, items) pairs obtained by traversing the item_gen generator """
#     last_group = NothingYet
#     group_items = mk_item_container()
#     group = NothingYet
#
#     for item in item_gen:
#         group = item_to_group(item)
#
#         if group != last_group and last_group is not NothingYet:
#             yield group, group_items
#             clear_item_container(group_items)  # empty container
#
#         group_items.append(item)
#         last_group = group
#
#     if len(group_items):
#         yield group, group_items  # yield what ever is remaining

def comment_or_other(token):
    if token.type == tokenize.COMMENT:
        return 'comment'
    else:
        return 'other'


def code_snippets(code_src, token_to_group=comment_or_other):
    src = BytesIO(code_src.encode())
    tokens = tokenize.tokenize(src.readline)
    for group, group_tokens in groupby(tokens, key=token_to_group):
        group_tokens = list(group_tokens)
        group_tokens = [x[:2] for x in group_tokens]
        if len(group_tokens):
            # print(len(group_tokens))
            yield group, ''.join(x[1] for x in group_tokens)
            # yield group, tokenize.untokenize(group_tokens)

