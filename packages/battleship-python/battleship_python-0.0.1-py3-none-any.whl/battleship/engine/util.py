#
# This file is part of the battleship-python project
#
# Copyright (c) 2024 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

import functools


def iter_points_from_lines(lines, translation=(0, 0)):
    tx, ty = translation
    return ((x + tx, y + ty) for y, row in enumerate(lines) for x, cell in enumerate(row) if cell != " ")


@functools.cache
def points_from_lines(lines, translation=(0, 0)):
    return frozenset(iter_points_from_lines(lines, translation))
