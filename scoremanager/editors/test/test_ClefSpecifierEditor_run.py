# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ClefSpecifierEditor_run_01():

    editor = scoremanager.editors.ClefSpecifierEditor()
    editor._run(pending_user_input='clef tre done') == 'treble'
