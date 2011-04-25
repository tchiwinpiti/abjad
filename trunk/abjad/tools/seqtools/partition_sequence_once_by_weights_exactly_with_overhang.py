from abjad.tools.seqtools._partition_sequence_elements_by_weights_exactly import \
   _partition_sequence_elements_by_weights_exactly


def partition_sequence_once_by_weights_exactly_with_overhang(sequence, weights):
   '''.. versionadded:: 1.1.1

   Partition `sequence` elements once by `weights` exactly with overhang::

      abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
      abjad> groups = seqtools.partition_sequence_once_by_weights_exactly_with_overhang(sequence, [3, 9])
      [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]

   Return list sequence element reference lists.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.group_sequence_elements_once_by_weights_exactly_with_overhang( )`` to
      ``seqtools.partition_sequence_once_by_weights_exactly_with_overhang( )``.
   '''

   return _partition_sequence_elements_by_weights_exactly(
      sequence, weights, cyclic = False, overhang = True)
