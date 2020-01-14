# core.NS - functional Python with Namespaces.

  core.NS is a Application Framework built around functional approach in the Python
programming language. There is no objects or "object-oriented" approach as we know.
Second "pillar" of the core.NS is an idea of "Namespaces". And based on those two concepts, we will be building our applications.

## First steps

  As a first steps, you will be expected, that there is a guidance on how to install
and do the first try-run of the tool.

### Installation
  ```
  pip install -U corens
  ```

### ... in the beginning
  ```
  Python 3.7.4 (default, Jul  9 2019, 18:13:23)
  [Clang 10.0.1 (clang-1001.0.46.4)] on darwin
  Type "help", "copyright", "credits" or "license" for more information.
  >>> from corens import *
  >>> ns, f, F = NS()
  >>> f("/bin/stamp")()
  1578869315.8705332
  >>>
  ```

  In this example, you are creating a namespace, alongside with partially-evaluated functions for resolving and executing functions in namespace and partially-evaluated function for exporting namespace functions into a builtin functions. Then you are resolving and executing partially-evaluated function referred as _/bin/stamp_ inside namespace. This function will return you a current timestamp.

## Why bother ?
