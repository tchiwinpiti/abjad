from abjad import *
import py.test


def test_ArticulationsInterface_01( ):
   t = Note(0, (1, 4))
   assert len(t.articulations) == 0
   assert t.format == "c'4"


def test_ArticulationsInterface_02( ):
   t = Note(0, (1, 4))
   #t.articulations = ['staccato']
   t.articulations.append('staccato')
   assert len(t.articulations) == 1
   assert t.format == "c'4 -\\staccato"


def test_ArticulationsInterface_03( ):
   '''Articulations can be set as list of (string, direction) pairs.'''
   t = Note(0, (1, 4))
   #t.articulations = [('staccato', 'up')]
   t.articulations.append(('staccato', 'up'))
   assert len(t.articulations) == 1
   assert t.format == "c'4 ^\\staccato"


def test_ArticulationsInterface_04( ):
   t = Note(0, (1, 4))
   #t.articulations = ['staccato', 'marcato']
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   assert t.format == "c'4 -\\marcato -\\staccato"


def test_ArticulationsInterface_05( ):
   '''Articulations can be set as list of (string, direction) pairs.'''
   t = Note(0, (1, 4))
   #t.articulations = [('staccato', 'up'), ('marcato', 'down')]
   t.articulations.extend([('staccato', 'up'), ('marcato', 'down')])
   assert len(t.articulations) == 2
   assert t.format == "c'4 ^\\staccato _\\marcato"


def test_ArticulationsInterface_06( ):
   '''Articulations can be set as list of (string, direction) pairs.'''
   t = Note(0, (1, 4))
   #t.articulations = [('staccato', 'up'), 'marcato']
   t.articulations.extend([('staccato', 'up'), 'marcato'])
   assert len(t.articulations) == 2
   assert t.format == "c'4 -\\marcato ^\\staccato"


def test_ArticulationsInterface_07( ):
   '''Append.'''
   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   assert len(t.articulations) == 1
   assert t.format == "c'4 -\\staccato"


def test_ArticulationsInterface_08( ):
   '''Extend.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   assert t.format == "c'4 -\\marcato -\\staccato"


def test_ArticulationsInterface_09( ):
   '''Sort works on articulations.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   t.articulations.sort( )
   assert len(t.articulations) == 2
   assert t.format == "c'4 -\\marcato -\\staccato"
   
   
def test_ArticulationsInterface_10( ):
   '''Includes works on articulations.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert 'staccato' in t.articulations
   assert 'marcato' in t.articulations


def test_ArticulationsInterface_11( ):
   '''Pop.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   t.articulations.pop( )
   assert len(t.articulations) == 1
   t.articulations.pop( )
   assert len(t.articulations) == 0


def test_ArticulationsInterface_12( ):
   '''Remove.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   t.articulations.remove('staccato')
   assert len(t.articulations) == 1
   t.articulations.remove('marcato')
   assert len(t.articulations) == 0
   
   
def test_ArticulationsInterface_13( ):
   '''Articulations can be set with empty list.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   #t.articulations = [ ]
   t.articulations[:] = [ ]
   assert len(t.articulations) == 0


def test_ArticulationsInterface_14( ):
   '''Articulations can be set with None.'''
   t = Note(0, (1, 4))
   t.articulations.extend(['staccato', 'marcato'])
   assert len(t.articulations) == 2
   #t.articulations = None
   t.articulations[:] = [ ]
   assert len(t.articulations) == 0


def test_ArticulationsInterface_15( ):
   '''Articulations can only be directly set with list or tuple.'''
   t = Note(0, (1, 4))
   assert py.test.raises(Exception, "t.articulations = 'staccato'")
