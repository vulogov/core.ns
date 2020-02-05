Functions
=========

.. note::
	core.NS ZEN rule #3 - Object-Oriented approach is nice, but it doesn't mean that you have to use it everywhere. Good functions are hard to beat. Write functions !

What's differentiate core.NS function from regular Python function. There are reference to a global context, passed to the function as first parameter. If function is a part of the `drivers <drivers.rst>`_ definition, there are two default first parameters. You would say that it will be mundane to pass the same parameter to the each and every functions defined for **core.NS**. Not if you are using *partially applied functions*.

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

	f("add1")("/home/counter")
	print(V("/home/counter"))

The first news is on the line 5. We are referencing function *I()*. This function creates *partially applied function* and stored it in **core.NS** namespace for a latter use. Line 6, we are initializing our counter on the namespace. Then we are creating a what looks like a normal Python function. But, wait. Look at the first parameter - this is **core.NS** function, taking a reference to a namespace. Next "line of the interest" is 13. What you can find inside the function add1, should't cause any troubles. Remember: **core.NS** functions are not pure and *V()* is a function for accessing data stored on namespace. And of course, if you look at source code of *V()* defined in `ns.py <https://github.com/vulogov/core.ns/blob/master/corens/ns.py>`_, you will see that's the V is sure, **core.NS** function too. So, let's take a look at line 13. We are defining function with path */bin/add1* and the function is add1 as we defined it. This function will be converted to a *partially applied function* by the function *I()*. So *I()* is just a *syntax sugar* for *V()*. You can create a partially applied functions with nothing but *V()*, but I will spare details of "now" for now. Then on line 15, we are referencing function that we just define and call the reference with parameter. Remember, *f()* return you the reference on the *partially applied function*. Line 16 shall bring you the fact that the value stored in *"/home/counter"*, indeed increased.

So, the **core.NS** namespace do store *partially applied functions* for which you do not have to remember to pass the first parameter. Parameter bound is "no-error" parameter.
