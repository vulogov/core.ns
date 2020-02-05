Drivers
=========

.. note::
	core.NS ZEN rule #4 - Drivers are the perfect technics to hide low-level logic from the high-level logic and organize communication between them via `functons <functions.rst>`_

What is the "low-level logic" and why drivers in **core.NS** ? Please allow me to give a simple definition of what is **core.NS** driver:

*The core.NS driver is a element of the code, which besides the reference to the global namespace, having a reference to a context*

Essentially, each driver it is a directory, holding some context-specific data as well as *partial applied functions*, each of them is with two bound arguments: one to a global namespace, another one is to a directory, keeping context. The closest "relative" of the **core.NS** drivers is a Unix drivers with contexts in */dev* . There are low-level logic to work with, for exaple */dev/sda*, */dev/sdb* and so on. Each of this logics, is provided with context and without context are rather abstract.

Let me bring some example. We will extend a functionality of the **core.NS** with the counters. Context for counter driver implementation will be stored in */dev*. Each counter shall have a unique name. Each named counter must have an easy to understand, namespace-based interface. For example, we can call function *f("/dev/counter/create")()* to create counter and *f("/dev/c/$countername/++")()* to increase the value of the counter.

.. code-block:: python
  :linenos:

	def _counter_open(ns, ctx, name):
		c = nsGet(ns, "/dev/c/{}".format(name))
    if c is not None:
        return c
    else:
        c = nsMkdir(ns, "/dev/c/{}".format(name))
				nsSet(ns, "/dev/c/{}/counter".format(name), 0)
				nsSet(ns, "/dev/c/{}/++".format(name), partial(_counter_increase, ns, c))
		return c

	def _counter_increase(ns, ctx):
		_path = ctx["__name__"]
		c = "{}/counter".format(_path)
		nsSet(ns, c, nsGet(ns, c) + 1)
		return nsGet(ns, c)

Unlike in previous examples, in low-level implementations, I am recommending to use functions from *corens.ns* than *V()*. There are reasons for that. Function *_counter_open()* takes extra parameter - name. When we will know the name, first, we are checking if such name in */dev/c* already exists. If not, we shall create directory, initialize default value for the counter and create context-sensitive *partially-applied* function *++*

After that, wrap it in *_tpl = {}* section of the module that you are adding to your **core.NS**.

.. code-block:: python
	_tpl = {
			'counters': {
					'create': _counter_open,
			}
	}

And then use *Mk()* function to initialize driver in */dev* tree as *Mk('counters')*
