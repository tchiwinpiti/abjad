# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_go_to_all_materials_01():
    r'''From score materials to all materials.
    '''

    input_ = 'red~example~score m M q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Abjad IDE - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_MaterialPackageWrangler_go_to_all_materials_02():
    r'''From all materials to all materials.
    '''

    input_ = 'M M q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials',
        'Abjad IDE - materials',
        ]
    assert score_manager._transcript.titles == titles