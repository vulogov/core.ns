**core.NS** - Application Framework for Python with a Unix as its grandfather.
==============================================================================

.. caution::
	core.NS is in constant state of development and improvement. While I am striving to keep backward compatibility the best I could, please pay close attention to `"What's New" <whatsnew>`_  chapter of the documentation.

There are many Python Application Frameworks and when I am to introduce you another one, called core.NS. What is the **core.NS** and what it's place in the landscape of the Python packages ?

What is **core.NS** ?
---------------------

**core.NS** is a core application library, built around the idea of the `Namespaces <namespace>`_ . This idea may be a bit unfamiliar to a hardcore developers, who grow in the world of "Object-Oriented Programming", procedural languages, globals and local procedures and variables, scopes and many other things, that you've spend your life around. Although, this idea will be very familiar to everyone, who've been around Unix OS. **core.NS** is a library, for creating and working with "Unix filesystem"-like namespace, created inside application. There will be */bin*, */dev*, */home* and other placeholders you are familiar with. But instead concept that's "everything is file", *core.NS* proposes concept "Everything is a data that you can set and read"

.. note::
	core.NS ZEN rule #1 - *"Everything is a data and everything is accessible and modifiable through a V() procedure."* including functions. Functions are the *"First-Class citizens"* and treated exactly like any data.

Every function and data on **core.NS** namespace addressable by its path, which is exactly like Unix filesystem path. Since data and a code are only logically separated, you do have a total freedom on how allocate them, but me, I am following "good-ol'", time-tested Unix filesystem patterns.

What is the place of the **core.NS** in the landscape of the Python packages
----------------------------------------------------------------------------

**core.NS** is an *"Application Framework"*, means that is the tool for creating applications. And its have everything you need to do that:

# functions and data access primitives
# low-level functionality is separated from your application code with help of *drivers*
 # command-line arguments parsing. You do not have to create parser. The one already provided for you. Just define help texts and functions.
 # Startup and Shutdown functions. You just have to define the functions. All the logic of there execution is provided.
 # "Smart" console
 # "Smart" log subsystem
 # Support for cooperative multitasking via `gevent <http://gevent.org>`_

.. toctree::
  :caption: Current core.NS documentation
  :name: mastertoc
  :maxdepth: 2
  :glob:

  namespace
  whatsnew/*
  manpages/*
