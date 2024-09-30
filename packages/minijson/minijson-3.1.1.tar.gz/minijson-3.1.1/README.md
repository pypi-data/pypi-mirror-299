MiniJSON
========

MiniJSON is a codec for a compact binary representation of a superset of JSON
(binary values) are supported.

Documentation is available [here](https://smokserwis.docs.smok.co/minijson/),
along with the MiniJSON format specification.

Note
----

Active development of **minijson** is moved to this fork.
[Dronehub](https://github.com/Dronehub) has no interest in further
developing this awesome technology.

Installation
------------

You should be able to install it from our own PyPI:

```bash
pip install --extra-index-url https://git.dms-serwis.com.pl/api/v4/projects/284/packages/pypi/simple minijson
```

There should be plenty of binaries available for multiple platforms. If you'd
like a new one, just file an issue
If there are no binary wheels precompiled for this platform, you will need to
compile it yourself.
Alternatively, you can
[file an issue](https://git.dms-serwis.com.pl/smokserwis/minijson/-/issues)
and I'll do my best to compile a wheel for you.

Compiling own wheels
--------------------

If there's no wheel, and you'd like to compile it on your own, you'll
require [Cython](https://cython.org/) installed.
