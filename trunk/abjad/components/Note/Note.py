from abjad.components._Leaf import _Leaf
import copy
import re


class Note(_Leaf):
   '''Abjad model of a note:

   ::

      abjad> Note(13, (3, 16))
      Note("cs''8.")
   '''

   __slots__ = ('_note_head', '_pitch', )
   
   def __init__(self, *args, **kwargs):
      from abjad.tools.lilyfiletools._lilypond_leaf_regex import _lilypond_leaf_regex
      if len(args) == 1 and isinstance(args[0], _Leaf):
         leaf = args[0]
         written_duration = leaf.duration.written
         lilypond_multiplier = leaf.duration.multiplier
         if hasattr(leaf, 'pitch'):
            pitch = leaf.pitch
         elif hasattr(leaf, 'pitches') and 0 < len(leaf.pitches):
            pitch = leaf.pitches[0]
         else:
            pitch = None
         self._copy_override_and_set_from_leaf(leaf)
      elif len(args) == 1 and isinstance(args[0], str):
         match = re.match(_lilypond_leaf_regex, args[0])
         chromatic_pitch_class_name, octave_tick_string, duration_body, dots = match.groups( )
         pitch = chromatic_pitch_class_name + octave_tick_string
         written_duration = duration_body + dots
         lilypond_multiplier = None
      elif len(args) == 2:
         pitch, written_duration = args
         lilypond_multiplier = None
      elif len(args) == 3:
         pitch, written_duration, lilypond_multiplier = args
      else:
         raise ValueError('can not initialize note from "%s".' % str(args))
      _Leaf.__init__(self, written_duration, lilypond_multiplier)
      self.note_head = pitch
      self._initialize_keyword_values(**kwargs)

   ## OVERLOADS ##

   #__deepcopy__ = __copy__

   def __getnewargs__(self):
      result = [ ]
      result.append(self.pitch)
      result.extend(_Leaf.__getnewargs__(self))
      return tuple(result)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _body(self):
      result = ''
      if self.pitch:
         result += str(self.pitch)
      result += str(self.duration)
      return [result] 

   @property
   def _compact_representation(self):
      return self._body[0]

   ## PUBLIC ATTRIBUTES ##

   @property
   def fingered_pitch(self):
      r'''Read-only fingered pitch of note::

         abjad> staff = Staff("d''8 e''8 f''8 g''8")
         abjad> piccolo = instrumenttools.Piccolo( )(staff)
         abjad> instrumenttools.transpose_leaves_in_expr_from_sounding_pitch_to_fingered_pitch(staff)

      ::

         abjad> f(staff)
         \new Staff {
            \set Staff.instrumentName = \markup { Piccolo }
            \set Staff.shortInstrumentName = \markup { Picc. }
            d'8
            e'8
            f'8
            g'8
         }

      ::
   
         abjad> staff[0].fingered_pitch
         NamedChromaticPitch("d'")

      Return named chromatic pitch.
      '''
      from abjad.tools import instrumenttools
      from abjad.tools import pitchtools
      if self.pitch_indication_is_at_sounding_pitch:
         instrument = instrumenttools.get_effective_instrument(self)
         if not instrument:
            raise InstrumentError('effective instrument of note can not be determined.')
         t_n = instrument.interval_of_transposition
         t_n *= -1
         fingered_pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(self.pitch, t_n)
         return fingered_pitch
      else:
         return self.pitch

   @apply
   def note_head( ):
      def fget(self):
         '''Get note head of note::

            abjad> note = Note(13, (3, 16))
            abjad> note.note_head
            NoteHead("cs''")

         Set note head of note::

            abjad> note = Note(13, (3, 16))
            abjad> note.note_head = 14
            abjad> note
            Note("d''8.")
         '''
         return self._note_head
      def fset(self, arg):
         from abjad.tools.notetools.NoteHead import NoteHead
         if isinstance(arg, type(None)):
            self._note_head = None
         elif isinstance(arg, NoteHead):
            self._note_head = arg
         else:
            note_head = NoteHead(self, arg)
            self._note_head = note_head
      return property(**locals( ))

   @apply
   def pitch( ):
      def fget(self):
         '''Get named pitch of note::

            abjad> note = Note(13, (3, 16))
            abjad> note.pitch
            NamedChromaticPitch("cs''")

         Set named pitch of note::

            abjad> note = Note(13, (3, 16))
            abjad> note.pitch = 14
            abjad> note
            Note("d''8.")
         '''
         if self.note_head is not None and hasattr(self.note_head, 'pitch'):
            return self._note_head.pitch
         else:
            return None
      def fset(self, arg):
         from abjad.tools import pitchtools
         from abjad.tools.notetools.NoteHead import NoteHead
         if arg is None:
            if self.note_head is not None:
               self.note_head.pitch = None
         else:
            if self.note_head is None:
               self.note_head = NoteHead(self, pitch = None)
            else:
               pitch = pitchtools.NamedChromaticPitch(arg)
               self.note_head.pitch = pitch
      return property(**locals( ))

   @property
   def sounding_pitch(self):
      r'''Read-only sounding pitch of note::

         abjad> staff = Staff("d''8 e''8 f''8 g''8")
         abjad> piccolo = instrumenttools.Piccolo( )(staff)
         abjad> instrumenttools.transpose_leaves_in_expr_from_sounding_pitch_to_fingered_pitch(staff)

      ::

         abjad> f(staff)
         \new Staff {
            \set Staff.instrumentName = \markup { Piccolo }
            \set Staff.shortInstrumentName = \markup { Picc. }
            d'8
            e'8
            f'8
            g'8
         }

      ::
   
         abjad> staff[0].sounding_pitch
         NamedChromaticPitch("d''")

      Return named chromatic pitch.
      '''
      from abjad.tools import instrumenttools
      from abjad.tools import pitchtools
      if self.pitch_indication_is_at_sounding_pitch:
         return self.pitch
      else:
         instrument = instrumenttools.get_effective_instrument(self)
         if not instrument:
            raise InstrumentError('effective instrument of note can not be determined.')
         t_n = instrument.interval_of_transposition
         sounding_pitch = pitchtools.transpose_pitch_carrier_by_melodic_interval(self.pitch, t_n)
         return sounding_pitch
