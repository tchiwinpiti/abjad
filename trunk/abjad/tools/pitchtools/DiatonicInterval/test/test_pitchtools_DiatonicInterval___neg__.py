from abjad import *
import py.test
py.test.skip( )


def test_pitchtools_DiatonicInterval___neg___01( ):

   interval = pitchtools.DiatonicInterval('minor', 3)
   assert -interval == pitchtools.DiatonicInterval('minor', -3)


def test_pitchtools_DiatonicInterval___neg___02( ):

   interval = pitchtools.DiatonicInterval('minor', -3)
   assert -interval == pitchtools.DiatonicInterval('minor', 3)
