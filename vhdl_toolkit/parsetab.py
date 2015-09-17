
# /home/nic30/Documents/workspace/hw_synthesis/hw_synthesis_helpers/vhdl_toolkit/parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = '9195A5F7E05E627AC0F404F95AEB41BA'
    
_lr_action_items = {'NAME':([0,5,6,7,8,9,10,11,],[3,13,13,13,13,13,13,13,]),'*':([1,2,3,12,13,14,15,16,17,18,19,20,],[-9,8,-10,8,-10,-7,-6,-5,8,8,8,-8,]),')':([1,12,13,14,15,16,17,18,20,],[-9,20,-10,-7,-6,-5,-4,-3,-8,]),'/':([1,2,3,12,13,14,15,16,17,18,19,20,],[-9,7,-10,7,-10,-7,-6,-5,7,7,7,-8,]),'NUMBER':([0,5,6,7,8,9,10,11,],[1,1,1,1,1,1,1,1,]),'=':([3,],[11,]),'+':([1,2,3,12,13,14,15,16,17,18,19,20,],[-9,10,-10,10,-10,-7,-6,-5,-4,-3,10,-8,]),'$end':([1,2,3,4,13,14,15,16,17,18,19,20,],[-9,-2,-10,0,-10,-7,-6,-5,-4,-3,-1,-8,]),'-':([0,1,2,3,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,],[6,-9,9,-10,6,6,6,6,6,6,6,9,-10,-7,-6,-5,-4,-3,9,-8,]),'(':([0,5,6,7,8,9,10,11,],[5,5,5,5,5,5,5,5,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,5,6,7,8,9,10,11,],[2,12,14,15,16,17,18,19,]),'statement':([0,],[4,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> NAME = expression','statement',3,'p_statement_assign','valueInterpret.py',49),
  ('statement -> expression','statement',1,'p_statement_expr','valueInterpret.py',53),
  ('expression -> expression + expression','expression',3,'p_expression_binop','valueInterpret.py',58),
  ('expression -> expression - expression','expression',3,'p_expression_binop','valueInterpret.py',59),
  ('expression -> expression * expression','expression',3,'p_expression_binop','valueInterpret.py',60),
  ('expression -> expression / expression','expression',3,'p_expression_binop','valueInterpret.py',61),
  ('expression -> - expression','expression',2,'p_expression_uminus','valueInterpret.py',68),
  ('expression -> ( expression )','expression',3,'p_expression_group','valueInterpret.py',72),
  ('expression -> NUMBER','expression',1,'p_expression_number','valueInterpret.py',76),
  ('expression -> NAME','expression',1,'p_expression_name','valueInterpret.py',80),
]
