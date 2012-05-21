from abjad import *


def testNumberedObjectDiatonicPitch___init___01():

    numbered_diatonic_pitch = pitchtools.NumberedDiatonicPitch(7)
    assert isinstance(numbered_diatonic_pitch, pitchtools.NumberedDiatonicPitch)


def testNumberedObjectDiatonicPitch___init___02():

    numbered_diatonic_pitch_1 = pitchtools.NumberedDiatonicPitch(7)
    numbered_diatonic_pitch_2 = pitchtools.NumberedDiatonicPitch(numbered_diatonic_pitch_1)
    assert isinstance(numbered_diatonic_pitch_2, pitchtools.NumberedDiatonicPitch)
