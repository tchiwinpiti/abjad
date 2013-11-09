# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondproxytools import LilyPondSettingManager


def test_lilypondproxytools_LilyPondSettingManager___repr___01():
    r'''LilyPond context contextualize component plug-in repr is evaluable.
    '''

    note = Note("c'4")
    contextualize(note).staff.tuplet_full_length = True

    context_setting_component_plug_in_1 = contextualize(note)
    context_setting_component_plug_in_2 = \
        eval(repr(context_setting_component_plug_in_1))

    assert isinstance(
        context_setting_component_plug_in_1, LilyPondSettingManager)
    assert isinstance(
        context_setting_component_plug_in_2, LilyPondSettingManager)


def test_lilypondproxytools_LilyPondSettingManager___repr___02():
    r'''LilyPond context contextualize component plug-in looks like this.
    '''

    note = Note("c'4")
    contextualize(note).staff.tuplet_full_length = True

    string = 'LilyPondSettingManager(staff__tuplet_full_length=True)'
    assert repr(contextualize(note)) == string
