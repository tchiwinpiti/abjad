# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_StatalServerCursor___eq___01():

    statal_server = datastructuretools.StatalServer([0, 1, 2, 3, 4])
    cursor_1 = statal_server.make_cursor()
    cursor_2 = statal_server.make_cursor()

    assert cursor_1 == cursor_1
    assert cursor_1 == cursor_2
    assert cursor_2 == cursor_1
    assert cursor_2 == cursor_2


def test_datastructuretools_StatalServerCursor___eq___02():

    statal_server = datastructuretools.StatalServer([0, 1, 2, 3, 4])
    cursor_1 = statal_server.make_cursor()
    cursor_2 = statal_server.make_cursor()
    cursor_1.next()

    assert cursor_1 == cursor_1
    assert cursor_1 != cursor_2
    assert cursor_2 != cursor_1
    assert cursor_2 == cursor_2