from abjad.tools import leaftools
from abjad.tools import pitchtools
from abjad.tools import voicetools
from abjad.tools.instrumenttools.get_effective_instrument import get_effective_instrument


def leaves_in_expr_are_within_traditional_instrument_ranges(expr):
   '''.. versionadded:: 1.1.2

   True when leaves in `expr` are within traditional instrument ranges::

      abjad> staff = Staff("c'8 r8 <d' fs'>8 r8")
      abjad> instrumenttools.Violin( )(staff)
   
   ::

      abjad> instrumenttools.leaves_in_expr_are_within_traditional_instrument_ranges(staff)
      True

   False otherwise::

      abjad> staff = Staff("c'8 r8 <d fs>8 r8")
      abjad> instrumenttools.Violin( )(staff)
   
   ::

      abjad> instrumenttools.leaves_in_expr_are_within_traditional_instrument_ranges(staff)
      False

   Return boolean.
   '''

   for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
      instrument = get_effective_instrument(leaf)
      if not instrument:
         print 'foo'
         return False
      if pitchtools.is_pitch_carrier(leaf) and not leaf in instrument.traditional_range:
         print 'bar'
         print leaf
         #voice = voicetools.get_first_voice_in_improper_parentage_of_component(leaf)
         #print voice
         #print voice.leaves.index(leaf)
         return False
   else:
      return True
