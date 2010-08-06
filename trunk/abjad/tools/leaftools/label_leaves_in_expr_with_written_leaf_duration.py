from abjad.tools.leaftools._label_leaves_in_expr_with_leaf_durations import \
   _label_leaves_in_expr_with_leaf_durations


def label_leaves_in_expr_with_written_leaf_duration(expr):
   r'''Label leaves in `expr` with writen leaf duration::

      abjad> tuplet = FixedDurationTuplet((1, 4), macros.scale(3))
      abjad> leaftools.label_leaves_in_expr_with_leaf_durations(tuplet)
      abjad> f(tuplet)
      \times 2/3 {
         c'8 _ \markup { \column { \small 1/8 \small 1/12 } }
         d'8 _ \markup { \column { \small 1/8 \small 1/12 } }
         e'8 _ \markup { \column { \small 1/8 \small 1/12 } }
      }

   Return none.
   '''

   show = ['written']
   return _label_leaves_in_expr_with_leaf_durations(expr, show = show)
