from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.spannertools.PhrasingSlurSpanner._PhrasingSlurSpannerFormatInterface import _PhrasingSlurSpannerFormatInterface


class PhrasingSlurSpanner(Spanner):

   def __init__(self, music = None):
      Spanner.__init__(self, music)
      self._format = _PhrasingSlurSpannerFormatInterface(self)
