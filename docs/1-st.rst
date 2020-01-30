First steps in core.NS
======================

.. warning::
	**core.NS** has been developed for Python3. Ans specifically for Python 3.6+ There is no plans to backport core.NS to Python2. Sorry, folk!

As we already know, the very first steps in **core.NS** is initialization of the Namespace and receiving ability to call functions and access data objects on the Namespace.

.. code-block:: python
  :linenos:

  Python 3.7.4 (default, Jul  9 2019, 18:13:23)
  [Clang 10.0.1 (clang-1001.0.46.4)] on darwin
  Type "help", "copyright", "credits" or "license" for more information.
  >>> from corens  import *
  >>> ns, f, F = NS()
  >>> V = f("V")
  >>> V("/config/answer")
  42

* On line 4, we are importing a basic functionality of the **core.NS**.     Usually, that is all that you will need.
* On line 5, we are creating new Namespace. This call returns three elements:
  * Reference to a namespace itself. Namespace in fact, is a one, big, complicated Python dictionary. Nothing more than that. You can work with Namespace directly, as you would work with any dictionary, but it is not recommended.
  * Reference to a function *"f()"*. This function is searching and returning you a reference to any other function stored in Namespace.
  * Reference to a function *"F()"*. This function acts similarly to an *f()*, but instead of returning the reference, *F()* install this function in Python builtins
* On line 6, we are referencing function *V()*, which we will need to access data elements.
