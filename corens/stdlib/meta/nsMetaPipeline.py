from corens.ns import *

PIPELINE_GRAMMAR = """
PipelineMeta:
    statements *= Statement
;

Statement:
    TaskStatement | PipeStatement
;

TaskStatement:
name=ID  "of" type=ID "->"
    data *= AssignmentDef
";;"
;

PipeStatement:
name=ID "=>"
    pipe *= PipePair
";;"
;

PipePair:
    name=ID (op=PipeOperation)?
;

PipeOperationCmd:
    "|" | "&" | "!" | "." | ">>>" | "<<<"
;

PipeOperation:
    "[" cmd=PipeOperationCmd name=NameDef "]" | "."
;

AssignmentDef:
    DirectAssignmentDef | ReverseAssignmentDef
;

DirectAssignmentDef:
    name=NameDef  DirectDataAssignmentOp data=Data
;

ReverseAssignmentDef:
    data=Data  ReverseDataAssignmentOp name=NameDef
;

NameDef:
    ID | STRING | NSID
;

NSID:
    "/" ID ("/" ID)*
;

DirectDataAssignmentOp:
    "is" | "<-"
;

ReverseDataAssignmentOp:
    "->" | "as"
;

KV:
    ID ":" Data
;

DICT:
    "{" data *= KV "}"
;

LIST:
    "[" data *= Data "]"
;

Data:
    BASETYPE | KV | DICT | LIST
;

Comment:
  /\\/\\/.*$/
;
"""

_lib = {
    "/etc/meta/pipeline" : PIPELINE_GRAMMAR
}
