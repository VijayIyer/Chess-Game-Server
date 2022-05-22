import re
from collections import defaultdict
import sys

'''
work on this regex
(?'piece'[K|N|B|R|Q]?)(?'amb'[a-h1-8]?)(?'capture'[x]?)(?'newcol'[a-h]{1})(?'newrow'[1-8]{1})(?'checkormate'[+|#]*)$

:param move: the notation used
:return: a dictionary which can then be used to infer the piece, the type of move, disambiguate
'''
move = sys.argv[1]
pattern = re.compile('(?P<piece>[K|N|B|R|Q]?)(?P<amb>[a-h1-8]?)(?P<capture>[x]?)(?P<newcol>[a-h]{1})('
                     '?P<newrow>[1-8]{1})(?P<promotion>=([N|B|R|Q]){1})?(?P<checkormate>[+|#]?)$|('
                     '?P<LongCastle>^(O-O-O){1})$|(?P<Castle>^(O-O){1})$')
m = re.match(pattern=pattern, string=move)
m_dict = m.groupdict()
for k, v in m_dict.items():
    print(f'{k}:{v}')
