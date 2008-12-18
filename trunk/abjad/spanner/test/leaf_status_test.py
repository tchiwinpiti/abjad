from abjad import *


def test_leaf_status_01( ):
   '''
   Spanner attached to flat container.
   '''

   t = Voice(run(4))
   appictate(t)
   p = NewSpanner(t)

   r'''
   \new Voice {
      c'8
      cs'8
      d'8
      ef'8
   }
   '''

   assert p._isMyFirstLeaf(t[0])
   for leaf in t[1 : ]:
      assert not p._isMyFirstLeaf(leaf)
   assert p._isMyLastLeaf(t[-1])
   for leaf in t[ : -1]:
      assert not p._isMyLastLeaf(leaf)
   for leaf in t:
      assert not p._isMyOnlyLeaf(leaf)


def test_leaf_status_02( ):
   '''
   Spanner attached to container with nested contents.
   '''

   t = Voice(run(4))
   t.insert(2, Sequential(run(2)))
   appictate(t)
   p = NewSpanner(t[ : 3])

   r'''
   \new Voice {
      c'8
      cs'8
      {
         d'8
         ef'8
      }
      e'8
      f'8
   }
   '''

   assert p._isMyFirstLeaf(t[0])
   assert p._isMyLastLeaf(t[2][1])


def test_leaf_status_03( ):
   '''
   Spanner attached to container with parallel nested contents.
   '''

   t = Voice(run(4))
   t.insert(2, Parallel(Sequential(run(2)) * 2))
   appictate(t)
   p = NewSpanner(t[ : 3])

   r'''
   \new Voice {
      c'8
      cs'8
      <<
         {
            d'8
            ef'8
         }
         {
            e'8
            f'8
         }
      >>
      fs'8
      g'8
   }
   '''

   assert p._isMyFirstLeaf(t[0])
   assert p._isMyLastLeaf(t[1])
