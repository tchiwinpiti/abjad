# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_display_every_asset_status_01():
    r'''Works with library.
    '''

    input_ = 'G rst* q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_SegmentPackageWrangler_display_every_asset_status_02():
    r'''Works with Git-managed segment package.
    '''

    input_ = 'red~example~score g rst* q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_SegmentPackageWrangler_display_every_asset_status_03():
    r'''Works with Subversion-managed segment package.
    '''

    wrangler = score_manager._segment_package_wrangler
    manager = wrangler._find_svn_manager(inside_score=False)
    if not manager:
        return

    manager.display_status()
    titles = manager._transcript.titles

    assert 'Repository status for' in contents
    assert '... OK' in contents