"""This module provides utilities for dynamic importing of modules and objects,
with support for caching, handling optional dependencies, and enhanced error
reporting.

**Functions:**

- `get_module(path)`: Attempts to import a module given its dotted path. It handles partial module paths
  and returns the module along with any remaining sub-paths.

- `get_child(path, parent, child)`: Retrieves a child attribute (e.g., a class or function) from a parent
  module or object. Raises an `ImportError` with detailed messages if the child cannot be found.

- `import_object(path, something=None)`: Imports an object specified by a path. If `something` is provided,
  it starts from that object and traverses the attributes according to the path. Otherwise, it imports
  the module specified in the path and retrieves the object.

- `cached_import(*args, **kw)`: A cached version of `import_object`, using `functools.cache` to memoize
  imports and improve performance.

- `required(path, *args, **kw)`: Attempts to import a required module or object. If the import fails,
  it raises an `ImportError` with a helpful message suggesting the package that might need to be installed.
  It can optionally suppress exceptions and log warnings.

- `optional(path, *args, **kw)`: Similar to `required`, but designed for optional dependencies. If the
  module or object cannot be imported, it returns `None` or a specified default value without raising
  an exception.

**Variables:**

- `IGNORED_OBJECT_FIELDS`: A set of attribute names to ignore when checking for attributes in modules
  or objects. These are typically built-in attributes that are not relevant when accessing module members.

- `PACKAGES_MAP`: A mapping of module base names to their corresponding package names. Used to provide
  clearer error messages when an import fails due to a missing package.

- `sort`: Attempts to import `natsort.natsorted` for natural sorting. If not available, it defaults to
  the built-in `sorted` function.

This module enhances dynamic importing capabilities by providing detailed logging, caching, and graceful
handling of optional dependencies. It is especially useful for applications that require runtime import
of modules or need to manage optional features based on the availability of certain packages.
"""

from contextlib import suppress
from functools import cache
from importlib import import_module
from inspect import ismodule

from kalib._internal import to_ascii
from kalib.internals import Who
from kalib.logging import Logging

logger = Logging.get(__name__)


IGNORED_OBJECT_FIELDS = {
    '__builtins__', '__cached__', '__doc__', '__file__', '__loader__',
    '__name__', '__package__', '__path__', '__spec__'}
PACKAGES_MAP = {'magic': 'python-magic', 'git': 'gitpython'}


@cache
def get_module(path):

    chunks = path.split('.')
    count = len(chunks) + 1

    if count == 2:  # noqa: PLR2004
        with suppress(ModuleNotFoundError):
            return import_module(path), ()

    for i in range(1, count):
        chunk = '.'.join(chunks[:count - i])
        with suppress(ModuleNotFoundError):
            return import_module(chunk), tuple(chunks[count - i:])

    msg = f"ImportError: {path} ({chunk!a} isn't exists)"
    raise ImportError(msg)


def get_child(path, parent, child):
    if ismodule(parent):
        __import__(parent.__name__, globals(), locals(), [str(child)])

    if not hasattr(parent, child):
        from kalib.misc import sourcefile

        if not ismodule(parent):
            raise ImportError(
                f"{path} (object {Who(parent)!a} hasn't attribute "
                f"{child!a}{sourcefile(parent, 'in %a')})")

        if not set(dir(parent)) - IGNORED_OBJECT_FIELDS:
            chunk = f'{Who(parent)}.{child}'
            raise ImportError(
                f'{path} (from partially initialized module '
                f'{chunk!a}, most likely due to a circular import'
                f'{sourcefile(parent, "from %a")}) or just not found')

        raise ImportError(
            f"{path} (module {Who(parent)!a} hasn't member {child!a}"
            f"{sourcefile(parent, 'in %a')})")

    return getattr(parent, child)


def import_object(path, something=None):
    if path is something is None:
        raise TypeError('all arguments is None')

    if isinstance(path, str | bytes):
        path = to_ascii(path)

    if not isinstance(path, str):
        if something is None:
            msg = (
                f"{Who.Is(path)} isn't str, but "
                f'second argument (import path) is None')
            raise TypeError(msg)
        path, something = something, path

    logger.debug(f'lookup: {path}')

    if something:
        locator = f'{Who(something)}.{path}'
        sequence = path.split('.')

    else:
        locator = f'{path}'
        something, sequence = get_module(path)

        if something is None:
            raise ImportError(f"{path} (isn't exists?)")

    if not sequence:
        logger.debug(f'import path: {Who(something)}')

    else:
        logger.debug(
            f'split path: {Who(something)} '
            f'(module) -> {".".join(sequence)} (path)')

    for name in sequence:
        something = get_child(locator, something, name)

    logger.debug('load ok: %s', path)
    return something


@cache
def cached_import(*args, **kw):
    return import_object(*args, **kw)


def required(path, *args, **kw):

    throw = kw.pop('throw', True)
    quiet = kw.pop('quiet', False)
    default = kw.pop('default', None)

    def wrap_uncacheable(*args, **kw):
        try:
            return cached_import(*args, **kw)

        except TypeError:
            return import_object(*args, **kw)

    try:
        return wrap_uncacheable(path, *args, **kw)

    except ImportError as e:

        if not quiet or throw:
            base = path.split('.', 1)[0]
            package = (PACKAGES_MAP.get(base) or base).replace('_', '-')

            msg = (
                f"couldn't import required({path=}, *{args=}, **{kw=}); "
                f'(need extra {package=}?)')

            if not quiet:
                Logging.Default.warning(msg, trace=True)

            if throw:
                raise ImportError(msg) from e

    return default


def optional(path, *args, **kw):
    kw.setdefault('quiet', True)
    kw.setdefault('throw', False)
    return required(path, *args, **kw)


sort = optional('natsort.natsorted', default=sorted)
