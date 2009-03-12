from abjad.helpers.components_unspan_shallow import components_unspan_shallow
from abjad.helpers.fracture_around_components import fracture_around_components


def fracture_unspan_components(component_list):
   '''Fracture to the left of leftmost component in list;
      fracture to the right of rightmost component in list;
      unspan all components in list;
      return components in list.'''

   fracture_around_components(component_list)
   components_unspan_shallow(component_list)
   
   return component_list
