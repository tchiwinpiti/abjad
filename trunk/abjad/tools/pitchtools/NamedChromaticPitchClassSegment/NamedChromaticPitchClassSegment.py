from abjad.tools.pitchtools._PitchClassSegment import _PitchClassSegment
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.MelodicDiatonicInterval import MelodicDiatonicInterval
from abjad.tools.pitchtools.NamedChromaticPitchClass import NamedChromaticPitchClass
from abjad.tools.pitchtools.NamedChromaticPitchClassSet import NamedChromaticPitchClassSet
from abjad.tools.pitchtools.NumberedChromaticPitchClassSegment import NumberedChromaticPitchClassSegment
from abjad.tools.pitchtools.NumberedChromaticPitchClassSet import NumberedChromaticPitchClassSet
import copy


class NamedChromaticPitchClassSegment(_PitchClassSegment):
   '''.. versionadded:: 1.1.2

   Ordered collection of named pitch-class instances.
   '''

   #def __init__(self, named_chromatic_pitch_class_tokens):
   def __new__(self, named_chromatic_pitch_class_tokens):
      npcs = [NamedChromaticPitchClass(x) for x in named_chromatic_pitch_class_tokens]
      #self.extend(npcs)
      return tuple.__new__(self, npcs)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '<%s>' % self._format_string
      
   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])

   ## PUBLIC ATTRIBUTES ##

   @property
   def diatonic_interval_class_segment(self):
      from abjad.tools import listtools
      from abjad.tools.pitchtools.InversionEquivalentDiatonicIntervalClassSegment import InversionEquivalentDiatonicIntervalClassSegment
      dics = listtools.difference_series(self)
      return InversionEquivalentDiatonicIntervalClassSegment(dics)

   @property
   def named_chromatic_pitch_class_set(self):
      return NamedChromaticPitchClassSet(self)

   @property
   def named_chromatic_pitch_classes(self):
      return tuple(self[:])

   @property
   def pitch_class_segment(self):
      return NumberedChromaticPitchClassSegment(self)

   @property
   def pitch_class_set(self):
      return NumberedChromaticPitchClassSet(self)

   @property
   def pitch_classes(self):
      return self.pitch_class_segment.pitch_classes

   ## PUBLIC METHODS ##

   def is_equivalent_under_transposition(self, arg):
      if not isinstance(arg, type(self)):
         return False
      if not len(self) == len(arg):
         return False
      difference = -(NamedChromaticPitch(arg[0], 4) - NamedChromaticPitch(self[0], 4))
      new_npcs = [x + difference for x in self]
      new_npc_seg = NamedChromaticPitchClassSegment(new_npcs)
      return arg == new_npc_seg

   def retrograde(self):
      return NamedChromaticPitchClassSegment(reversed(self))

   def rotate(self, n):
      from abjad.tools import listtools
      named_chromatic_pitch_classes = listtools.rotate(self.named_chromatic_pitch_classes, n)
      return NamedChromaticPitchClassSegment(named_chromatic_pitch_classes)
      
   def transpose(self, melodic_diatonic_interval):
      return NamedChromaticPitchClassSegment([
         npc + melodic_diatonic_interval  for npc in self])
