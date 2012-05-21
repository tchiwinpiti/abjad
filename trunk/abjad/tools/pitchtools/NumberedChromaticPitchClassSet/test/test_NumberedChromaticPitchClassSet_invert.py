from abjad import *


def testNumberedObjectChromaticPitchClassSet_invert_01():

    assert pitchtools.NumberedChromaticPitchClassSet([0, 1, 5]).invert() == \
        pitchtools.NumberedChromaticPitchClassSet([0, 7, 11])
    assert pitchtools.NumberedChromaticPitchClassSet([1, 2, 6]).invert() == \
        pitchtools.NumberedChromaticPitchClassSet([6, 10, 11])
