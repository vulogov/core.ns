Namespace
=========

.. note::
	core.NS ZEN rule #2 - Well regulated namespace of the data and code elements are more manageable and comprehensible, then an artificial maze of the objects and cryptic defaults for the local and global variables. In a Namespace, you can't be wrong, because, what's you place in the element defined by the path, that's what you will get. All the time.

Namespace - it is a in-memory (actually not only in-memory) tree-like
collection of the data elements. Considering, that the functions are the "First-Class Citizens", those data elements also include functions. Each element defined by it's path. */bin/V* , */config/answer*, */home/MyData*. There are two types of the data elements.

 * Directories. Structure, which can not hold any data by itself, besides certain *metadata*, but which can hold a references to other data elements. For example */bin/V*, directory */bin* keeping a reference to a data element *V*.

 * Data element. It is an atomic, indivisible, placeholder for storing an actual data. Data elements can store a references to another elements, but they are not a directories and they are terminating the path. For example:

    * Directory */bin* can form a finite path, if you are referring this directory, or be a part of the path to a data element, like */bin/V*

    * Data element forming a finite path with the name of the data element at the end. Only directories can be an intermediate parts of the path.

In order to refer an element in the namespace, you must know its path. For `functions <functions.rst>`_, **core.NS** provides special *syntax sugar* which will simplify the search. But for other data elements, function *V()* expects the passing of the full path to the element. There is no *current* or *relative* path. references. Only full path, which provides unquestionable, direct reference of the data element. Function returns *None*, if data element not exists.
