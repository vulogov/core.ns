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
