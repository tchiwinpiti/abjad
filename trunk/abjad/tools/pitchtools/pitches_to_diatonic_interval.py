from abjad.pitch import Pitch
from abjad.tools.pitchtools.MelodicDiatonicInterval import \
   MelodicDiatonicInterval
from abjad.tools.pitchtools.diatonic_and_chromatic_interval_numbers_to_diatonic_interval import diatonic_and_chromatic_interval_numbers_to_diatonic_interval


def pitches_to_diatonic_interval(pitch_1, pitch_2):
   '''.. versionadded:: 1.1.2

   Return diatonic interval from `pitch_1` to `pitch_2`. ::

   Unison. ::

      abjad> pitchtools.pitches_to_diatonic_interval(Pitch('c', 4), Pitch('c', 4))
      MelodicDiatonicInterval(perfect unison)

   Ascending diatonic intervals. ::

      abjad> pitchtools.pitches_to_diatonic_interval(Pitch('c', 4), Pitch('dff', 4))
      MelodicDiatonicInterval(ascending diminished second)

   ::

      abjad> pitchtools.pitches_to_diatonic_interval(Pitch('c', 4), Pitch('df', 4))
      DiatonicInterval(ascending minor second)

   ::

      abjad> pitchtools.pitches_to_diatonic_interval(Pitch('c', 4), Pitch('d', 4))
      MelodicDiatonicInterval(ascending major second)

   ::

      abjad> pitchtools.pitches_to_diatonic_interval(Pitch('c', 4), Pitch('ds', 4))
      MelodicDiatonicInterval(ascending augmented second)

   Descending diatonic intervals. ::

      abjad> pitchtools.pitches_to_diatonic_interval(Pitch('c', 4), Pitch('bs', 3))
      MelodicDiatonicInterval(ascending diminished second)

   ::

      abjad> pitchtools.pitches_to_diatonic_interval(Pitch('c', 4), Pitch('b', 3))
      MelodicDiatonicInterval(descending minor second)

   ::

      abjad> pitchtools.pitches_to_diatonic_interval(Pitch('c', 4), Pitch('bf', 3))
      MelodicDiatonicInterval(descending major second)

   ::

      abjad> pitchtools.pitches_to_diatonic_interval(Pitch('c', 4), Pitch('bff', 3))
      MelodicDiatonicInterval(descending augmented second)
   '''

   if not isinstance(pitch_1, Pitch):
      raise TypeError('must be pitch.')

   if not isinstance(pitch_2, Pitch):
      raise TypeError('must be pitch.')

   #print pitch_1, pitch_2

   diatonic_interval_number = abs(pitch_2.altitude - pitch_1.altitude) + 1
   chromatic_interval_number = pitch_2.number - pitch_1.number
   diatonic_interval = \
      diatonic_and_chromatic_interval_numbers_to_diatonic_interval(
      diatonic_interval_number, chromatic_interval_number)
   
   return diatonic_interval
