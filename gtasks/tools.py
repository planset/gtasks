# -*- coding: utf-8 -*-
"""
    gtasks.tools
    ~~~~~~~~~~~~


    :copyright: (c) 2012 by Daisuke Igarashi.
    :license: BSD, see LICENSE for more details.
"""

import os

def clear_screen():
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        os.system('CLS')
    else:
        print "\n"*40
