from abjad import *
from abjad.wf import check_measures_durations


def test_measure_empty_01( ):
   t = Measure(None, [ ])
   assert repr(t) == 'Measure( )'
   assert str(t) == '| |'
   assert t.format == ''
   assert t.meter == None
   assert len(t) == 0
   assert t.duration == Rational(0)
   assert t.duration.prolated == Rational(0)
   assert check_measures_durations(t, ret = True)


def test_measure_empty_02( ):
   t = Measure((4, 4), [ ])
   assert repr(t) == 'Measure(4/4)'
   assert str(t) == '|4/4|'
   assert t.format == '\t\\time 4/4'
   assert len(t) == 0
   assert t.duration == Rational(0)
   assert t.duration.prolated == Rational(0)
   assert not check_measures_durations(t, ret = True)


def test_measure_empty_03( ):
   t = Measure((4, 5), [ ])
   assert repr(t) == 'Measure(4/5)'
   assert str(t) == '|4/5|'
   assert t.format == '\t\\time 4/5'
   assert len(t) == 0
   assert t.duration == Rational(0)
   assert t.duration.prolated == Rational(0)
   assert not check_measures_durations(t, ret = True)
