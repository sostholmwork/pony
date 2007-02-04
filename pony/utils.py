from itertools import imap, ifilter
from operator import itemgetter
from inspect import isfunction
from os import urandom
from re import compile

def copy_func_attrs(new_func, old_func):
    new_func.__name__ = old_func.__name__
    new_func.__doc__ = old_func.__doc__
    new_func.__module__ = old_func.__module__
    new_func.__dict__.update(old_func.__dict__)
    if not hasattr(old_func, 'original_func'):
        new_func.original_func = old_func

def simple_decorator(old_dec):
    def new_dec(old_func):
        def new_func(*args, **keyargs):
            return old_dec(old_func, *args, **keyargs)
        copy_func_attrs(new_func, old_func)
        return new_func
    copy_func_attrs(new_dec, old_dec)
    return new_dec

def decorator(old_dec):
    def new_dec(old_func):
        new_func = old_dec(old_func)
        copy_func_attrs(new_func, old_func)
        return new_func
    copy_func_attrs(new_dec, old_dec)
    return new_dec

def decorator_with_params(old_dec):
    def new_dec(*args, **keyargs):
        if len(args) == 1 and isfunction(args[0]) and not keyargs:
            old_func = args[0]
            new_func = old_dec()(old_func)
            copy_func_attrs(new_func, old_func)
            return new_func
        else:
            even_more_new_dec = old_dec(*args, **keyargs)
            copy_func_attrs(even_more_new_dec, old_dec)
            return even_more_new_dec
    copy_func_attrs(new_dec, old_dec)
    return new_dec

def error_method(*args, **kwargs):
    raise TypeError

ident_re = compile(r'[A-Za-z_]\w*')

# is_ident = ident_re.match
def is_ident(string):
    'is_ident(string) -> bool'
    return bool(ident_re.match(string))

def import_module(name):
    "import_module('a.b.c') -> <module a.b.c>"
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]: mod = getattr(mod, comp)
    return mod

def new_guid():
    'new_guid() -> new_binary_guid'
    return buffer(urandom(16))

def guid2str(guid):
    """guid_binary2str(binary_guid) -> string_guid

    >>> guid2str(unxehlify('ff19966f868b11d0b42d00c04fc964ff'))
    '6F9619FF-8B86-D011-B42D-00C04FC964FF'
    """
    assert isinstance(guid, buffer) and len(guid) == 16
    guid = str(guid)
    return '%s-%s-%s-%s-%s' % tuple(map(hexlify, (
        guid[3::-1], guid[5:3:-1], guid[7:5:-1], guid[8:10], guid[10:])))

def str2guid(s):
    """guid_str2binary(str_guid) -> binary_guid

    >>> unhexlify(str2guid('6F9619FF-8B86-D011-B42D-00C04FC964FF'))
    'ff19966f868b11d0b42d00c04fc964ff'
    """
    assert isinstance(s, basestring) and len(s) == 36
    a, b, c, d, e = map(unhexlify, (s[:8],s[9:13],s[14:18],s[19:23],s[24:]))
    reverse = slice(-1, None, -1)
    return buffer(''.join((a[reverse], b[reverse], c[reverse], d, e)))


