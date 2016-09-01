voodooconfig
============

.. image:: https://travis-ci.org/esc/voodooconfig.svg?branch=master
      :target: https://travis-ci.org/esc/voodooconfig

Ancilliary library to process and hold a set of options when programming
command-line interfaces.

Example
-------

see: `example.py <example.py>`_

Installation
------------

Install via PyPi::

    $ pip install voodooconfig

What Problem does this Solve?
-----------------------------

Imagine you are writing a command-line utility. This has a set of options with
some sane defaults. Furthermore there are one or more config-files and
additionally some command-line parameters. This class solve the problem of
accumulating all of these. Importantly, this can be done such that values on
the command-line override those from the config-file(s) which again override
the defaults.

Additionally, the `VoodooConfig` class has some voodoo to allow both attribute
and dictionary based access to the options stored within. So for example the
following are equivalent::

    >>> config['api_key']
    'THEKEY'
    >>> config.api_key
    'THEKEY'

This allows you to fill the class in a reflection based style, but at the same
time access the options pythonically::


    >>> loaded_config = {'api_key': 'NEW_KEY'}
    >>> for k,v in loaded_config:
    >>>     config[k] = v

The last feature is that, when loading a config any hyphens are converted to
underscores. This is required, since Python attributes may not contain hyphens.

Mindset
-------

It is a super-simple utility with lots of flexibility. I decided to publish it
as separate package since I have been solving this exact same problem again and
again over the years and didn't want to keep re-inventing the wheel every time.
The interface is also super simple so that it can be combined with any of the
myriad of command-line interface tools that exist in Python. At the core,
options are just a mapping/dictionary so you can use those to insert values
and/or export the options in a format suitable for processing by subsequent
tools.

Limitations
-----------

* Currently it kinda uses YAML as config-file syntax but that can be adapted.
* There is no type-checking or parameter validation.
* There is no way to declare required/optional options and any complex
  relationship between options, e.g. mutually exclusivity, can not be declared.


License
-------

Copyright 2016 Valentin Haenel <valentin@haenel.co>

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
