"""A brain-dead implementation of Mako"""
import re
import typing as tp


FOR_MATCH = re.compile(r'% for (.*?) in (.*?)\:')

HFILE_MAKO = """#include "Python.h"

PyObject* PyInit_{initpy_name}();
"""


INITPY_MAKO = """from {module_name}.__bootstrap__ import bootstrap_cython_submodules
bootstrap_cython_submodules()
"""

class Output:
    def __init__(self):
        self.elements_containing = {}   #: type dict[str, list[str]]
        self.data = []      #: type: str | tuple[str, str, str]

    def __str__(self):
        return '\n'.join(self.data)
    def append(self, ostr: str, **kwargs):
        if kwargs:
            ostr = ostr.format(**kwargs)
        self.data.append(ostr)
    def append_many(self, lines: str, **kwargs):
        for line in lines.split('\n'):
            if kwargs:
                line = line.format(**kwargs)
            self.data.append(line)
