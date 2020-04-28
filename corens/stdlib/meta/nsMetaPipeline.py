from corens.ns import *

PIPELINE_GRAMMAR = """
Hello:
  'hello' who=ID
;
"""

_lib = {
    "/etc/meta/pipeline" : PIPELINE_GRAMMAR
}
