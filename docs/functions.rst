Functions
=========

.. note::
	core.NS ZEN rule #3 - Object-Oriented approach is nice, but it doesn't mean that you have to use it everywhere. Good functions are hard to beat. Write functions !

What's differentiate core.NS function from regular Python function. There are reference to a global context, passed to the function as first parameter. If function is a part of the `drivers`_ definition, there are two default first parameters. You would say that it will be mundane to pass the same parameter to the each and every functions defined for **core.NS**. Not if you are using *partially applied functions*.

What is the *partially applied function* ? Without going too deep in the theory of Lambda calculus and Functional Programming, I'll try to give a perfectly simple definition to this, in the reality, quite complicated term. *Partially applied function* is such function which is bound with some of its parameters without actual execution of this function. The reference on the function and bound parameters are serving as a reference on this function that you can call, without specify parameters, that you already bound. Let me illustrate this concept with this simple example:

.. code-block:: python
  :linenos:

	from corens  import *

	ns, f, F = NS()
	V = f("V")
	I = f("I")
	V("/home/counter", 0)

	def add1(ns, _path):
		V = f("V")
		V(_path, V(_path)+1)
		return V(_path)

	I("/bin/add1", add1)

	f("add1", "/home/counter")
	print(V("/home/counter"))
