from abjad.tools.containertools.Container import Container
from abjad.tools.measuretools.Measure import Measure


def comment_measures_in_container_with_measure_numbers(container, style = 'comment'):
   r'''Label measure numbers in `container` according to `style`.

   .. note:: functionality current not implemented.

   Turn measure number labels on with ``style = 'comment'``. ::

      abjad> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
      abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
      abjad> measuretools.comment_measures_in_container_with_measure_numbers(staff, style = 'comment') # doctest: +SKIP
      abjad> f(staff) # doctest: +SKIP
      \new Staff {
              % start measure 1
              {
                      \time 2/8
                      c'8
                      d'8
              }
              % stop measure 1
              % start measure 2
              {
                      \time 2/8
                      e'8
                      f'8
              }
              % stop measure 2
              % start measure 3
              {
                      \time 2/8
                      g'8
                      a'8
              }
              % stop measure 3
      }

   Turn measure number labels off with ``style = None``. ::

      abjad> measuretools.comment_measures_in_container_with_measure_numbers(staff, style = None) # doctest: +SKIP
      abjad> f(staff) # doctest: +SKIP
      \new Staff {
              {
                      \time 2/8
                      c'8
                      d'8
              }
              {
                      \time 2/8
                      e'8
                      f'8
              }
              {
                      \time 2/8
                      g'8
                      a'8
              }
      }

   .. versionchanged:: 1.1.2
      renamed ``label.measure_numbers( )`` to
      ``measuretools.comment_measures_in_container_with_measure_numbers( )``.
   '''

   if isinstance(container, Measure):
      container._formatter.number.self = style
   else:
      container._formatter.number.measures = style
