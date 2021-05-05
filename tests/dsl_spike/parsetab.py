
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'COUNT SYMBOL\n    chemical_equation :\n    chemical_equation : species_list\n    species_list :  species_list speciesspecies_list : species\n    species : SYMBOL\n    species : SYMBOL COUNT\n    '
    
_lr_action_items = {'$end':([0,1,2,3,4,5,6,],[-1,0,-2,-4,-5,-3,-6,]),'SYMBOL':([0,2,3,4,5,6,],[4,4,-4,-5,-3,-6,]),'COUNT':([4,],[6,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'chemical_equation':([0,],[1,]),'species_list':([0,],[2,]),'species':([0,2,],[3,5,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> chemical_equation","S'",1,None,None,None),
  ('chemical_equation -> <empty>','chemical_equation',0,'p_chemical_equation','test_ply_chem_example.py',48),
  ('chemical_equation -> species_list','chemical_equation',1,'p_chemical_equation','test_ply_chem_example.py',49),
  ('species_list -> species_list species','species_list',2,'p_species_list','test_ply_chem_example.py',59),
  ('species_list -> species','species_list',1,'p_species','test_ply_chem_example.py',64),
  ('species -> SYMBOL','species',1,'p_single_species','test_ply_chem_example.py',70),
  ('species -> SYMBOL COUNT','species',2,'p_single_species','test_ply_chem_example.py',71),
]
