import networkx as nx
import numpy as np
import os
import re
import sys
from collections import ChainMap, defaultdict, deque, Counter
from dataclasses import dataclass
from enum import Enum
from functools import partial, reduce
from itertools import chain, combinations, count, cycle, permutations, product, repeat
from math import ceil, cos, cosh, dist, floor, gcd, hypot, sin, sinh, tan, tanh
from operator import and_, mul, attrgetter, itemgetter, methodcaller

from lib.input import (
    fetch,
    fetch_commasep,
    fetch_int_commasep,
    fetch_lines,
    fetch_int_lines,
)

