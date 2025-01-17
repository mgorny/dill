#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2008-2016 California Institute of Technology.
# Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/dill/blob/master/LICENSE

# author, version, license, and long description
__version__ = '0.3.6.dev0'
__author__ = 'Mike McKerns'

__doc__ = """
-----------------------------
dill: serialize all of python
-----------------------------

About Dill
==========

``dill`` extends python's ``pickle`` module for serializing and de-serializing
python objects to the majority of the built-in python types. Serialization
is the process of converting an object to a byte stream, and the inverse
of which is converting a byte stream back to a python object hierarchy.

``dill`` provides the user the same interface as the ``pickle`` module, and
also includes some additional features. In addition to pickling python
objects, ``dill`` provides the ability to save the state of an interpreter
session in a single command.  Hence, it would be feasable to save an
interpreter session, close the interpreter, ship the pickled file to
another computer, open a new interpreter, unpickle the session and
thus continue from the 'saved' state of the original interpreter
session.

``dill`` can be used to store python objects to a file, but the primary
usage is to send python objects across the network as a byte stream.
``dill`` is quite flexible, and allows arbitrary user defined classes
and functions to be serialized.  Thus ``dill`` is not intended to be
secure against erroneously or maliciously constructed data. It is
left to the user to decide whether the data they unpickle is from
a trustworthy source.

``dill`` is part of ``pathos``, a python framework for heterogeneous computing.
``dill`` is in active development, so any user feedback, bug reports, comments,
or suggestions are highly appreciated.  A list of issues is located at https://github.com/uqfoundation/dill/issues, with a legacy list maintained at https://uqfoundation.github.io/project/pathos/query.


Major Features
==============

``dill`` can pickle the following standard types:

    - none, type, bool, int, long, float, complex, str, unicode,
    - tuple, list, dict, file, buffer, builtin,
    - both old and new style classes,
    - instances of old and new style classes,
    - set, frozenset, array, functions, exceptions

``dill`` can also pickle more 'exotic' standard types:

    - functions with yields, nested functions, lambdas,
    - cell, method, unboundmethod, module, code, methodwrapper,
    - dictproxy, methoddescriptor, getsetdescriptor, memberdescriptor,
    - wrapperdescriptor, xrange, slice,
    - notimplemented, ellipsis, quit

``dill`` cannot yet pickle these standard types:

    - frame, generator, traceback

``dill`` also provides the capability to:

    - save and load python interpreter sessions
    - save and extract the source code from functions and classes
    - interactively diagnose pickling errors


Current Release
===============

The latest released version of ``dill`` is available from:

    https://pypi.org/project/dill

``dill`` is distributed under a 3-clause BSD license.


Development Version
===================

You can get the latest development version with all the shiny new features at:

    https://github.com/uqfoundation

If you have a new contribution, please submit a pull request.


Installation
============

``dill`` can be installed with ``pip``::

    $ pip install dill

To optionally include the ``objgraph`` diagnostic tool in the install::

    $ pip install dill[graph]

For windows users, to optionally install session history tools::

    $ pip install dill[readline]


Requirements
============

``dill`` requires:

    - ``python`` (or ``pypy``), **==2.7** or **>=3.7**
    - ``setuptools``, **>=42**
    - ``wheel``, **>=0.1**

Optional requirements:

    - ``objgraph``, **>=1.7.2**
    - ``pyreadline``, **>=1.7.1** (on windows)


Basic Usage
===========

``dill`` is a drop-in replacement for ``pickle``. Existing code can be
updated to allow complete pickling using::

    >>> import dill as pickle

or::

    >>> from dill import dumps, loads

``dumps`` converts the object to a unique byte string, and ``loads`` performs
the inverse operation::

    >>> squared = lambda x: x**2
    >>> loads(dumps(squared))(3)
    9

There are a number of options to control serialization which are provided
as keyword arguments to several ``dill`` functions:

* with *protocol*, the pickle protocol level can be set. This uses the
  same value as the ``pickle`` module, *HIGHEST_PROTOCOL* or *DEFAULT_PROTOCOL*.
* with *byref=True*, ``dill`` to behave a lot more like pickle with
  certain objects (like modules) pickled by reference as opposed to
  attempting to pickle the object itself.
* with *recurse=True*, objects referred to in the global dictionary are
  recursively traced and pickled, instead of the default behavior of
  attempting to store the entire global dictionary.
* with *fmode*, the contents of the file can be pickled along with the file
  handle, which is useful if the object is being sent over the wire to a
  remote system which does not have the original file on disk. Options are
  *HANDLE_FMODE* for just the handle, *CONTENTS_FMODE* for the file content
  and *FILE_FMODE* for content and handle.
* with *ignore=False*, objects reconstructed with types defined in the
  top-level script environment use the existing type in the environment
  rather than a possibly different reconstructed type.

The default serialization can also be set globally in *dill.settings*.
Thus, we can modify how ``dill`` handles references to the global dictionary
locally or globally::

    >>> import dill.settings
    >>> dumps(absolute) == dumps(absolute, recurse=True)
    False
    >>> dill.settings['recurse'] = True
    >>> dumps(absolute) == dumps(absolute, recurse=True)
    True

``dill`` also includes source code inspection, as an alternate to pickling::

    >>> import dill.source
    >>> print(dill.source.getsource(squared))
    squared = lambda x:x**2

To aid in debugging pickling issues, use *dill.detect* which provides
tools like pickle tracing::

    >>> import dill.detect
    >>> dill.detect.trace(True)
    >>> f = dumps(squared)
    F1: <function <lambda> at 0x108899e18>
    F2: <function _create_function at 0x108db7488>
    # F2
    Co: <code object <lambda> at 0x10866a270, file "<stdin>", line 1>
    F2: <function _create_code at 0x108db7510>
    # F2
    # Co
    D1: <dict object at 0x10862b3f0>
    # D1
    D2: <dict object at 0x108e42ee8>
    # D2
    # F1
    >>> dill.detect.trace(False)

With trace, we see how ``dill`` stored the lambda (``F1``) by first storing
``_create_function``, the underlying code object (``Co``) and ``_create_code``
(which is used to handle code objects), then we handle the reference to
the global dict (``D2``).  A ``#`` marks when the object is actually stored.


More Information
================

Probably the best way to get started is to look at the documentation at
http://dill.rtfd.io. Also see ``dill.tests`` for a set of scripts that
demonstrate how ``dill`` can serialize different python objects. You can
run the test suite with ``python -m dill.tests``. The contents of any
pickle file can be examined with ``undill``.  As ``dill`` conforms to
the ``pickle`` interface, the examples and documentation found at
http://docs.python.org/library/pickle.html also apply to ``dill``
if one will ``import dill as pickle``. The source code is also generally
well documented, so further questions may be resolved by inspecting the
code itself. Please feel free to submit a ticket on github, or ask a
question on stackoverflow (**@Mike McKerns**).
If you would like to share how you use ``dill`` in your work, please send
an email (to **mmckerns at uqfoundation dot org**).


Citation
========

If you use ``dill`` to do research that leads to publication, we ask that you
acknowledge use of ``dill`` by citing the following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    https://uqfoundation.github.io/project/pathos

Please see https://uqfoundation.github.io/project/pathos or
http://arxiv.org/pdf/1202.1056 for further information.

"""

__license__ = """
Copyright (c) 2004-2016 California Institute of Technology.
Copyright (c) 2016-2022 The Uncertainty Quantification Foundation.
All rights reserved.

This software is available subject to the conditions and terms laid
out below. By downloading and using this software you are agreeing
to the following conditions.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met::

    - Redistribution of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    - Redistribution in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentations and/or other materials provided with the distribution.

    - Neither the names of the copyright holders nor the names of any of
      the contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

from ._dill import dump, dumps, load, loads, dump_session, load_session, \
    Pickler, Unpickler, register, copy, pickle, pickles, check, \
    HIGHEST_PROTOCOL, DEFAULT_PROTOCOL, PicklingError, UnpicklingError, \
    HANDLE_FMODE, CONTENTS_FMODE, FILE_FMODE, PickleError, PickleWarning, \
    PicklingWarning, UnpicklingWarning
from . import source, temp, detect

# get global settings
from .settings import settings

# make sure "trace" is turned off
detect.trace(False)

try:
    from importlib import reload
except ImportError:
    try:
        from imp import reload
    except ImportError:
        pass

# put the objects in order, if possible
try:
    from collections import OrderedDict as odict
except ImportError:
    try:
        from ordereddict import OrderedDict as odict
    except ImportError:
        odict = dict
objects = odict()
# local import of dill._objects
#from . import _objects
#objects.update(_objects.succeeds)
#del _objects

# local import of dill.objtypes
from . import objtypes as types

def load_types(pickleable=True, unpickleable=True):
    """load pickleable and/or unpickleable types to ``dill.types``

    ``dill.types`` is meant to mimic the ``types`` module, providing a
    registry of object types.  By default, the module is empty (for import
    speed purposes). Use the ``load_types`` function to load selected object
    types to the ``dill.types`` module.

    Args:
        pickleable (bool, default=True): if True, load pickleable types.
        unpickleable (bool, default=True): if True, load unpickleable types.

    Returns:
        None
    """
    # local import of dill.objects
    from . import _objects
    if pickleable:
        objects.update(_objects.succeeds)
    else:
        [objects.pop(obj,None) for obj in _objects.succeeds]
    if unpickleable:
        objects.update(_objects.failures)
    else:
        [objects.pop(obj,None) for obj in _objects.failures]
    objects.update(_objects.registered)
    del _objects
    # reset contents of types to 'empty'
    [types.__dict__.pop(obj) for obj in list(types.__dict__.keys()) \
                             if obj.find('Type') != -1]
    # add corresponding types from objects to types
    reload(types)

def extend(use_dill=True):
    '''add (or remove) dill types to/from the pickle registry

    by default, ``dill`` populates its types to ``pickle.Pickler.dispatch``.
    Thus, all ``dill`` types are available upon calling ``'import pickle'``.
    To drop all ``dill`` types from the ``pickle`` dispatch, *use_dill=False*.

    Args:
        use_dill (bool, default=True): if True, extend the dispatch table.

    Returns:
        None
    '''
    from ._dill import _revert_extension, _extend
    if use_dill: _extend()
    else: _revert_extension()
    return

extend()
del odict


def license():
    """print license"""
    print (__license__)
    return

def citation():
    """print citation"""
    print (__doc__[-491:-118])
    return

# end of file
