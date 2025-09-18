from base64 import b64decode
from io import BytesIO
import pickle as _pickle

ALLOWED_MODULES = ['__main__', 'app', 'request']
UNSAFE_NAMES = ['__setattr__', '__delattr__', '__dict__', '__getattribute__', '__getitem__', '__subclasses__', 'eval']
BLACKLISTED_NAMES = ['__globals__', '__import__', '__base__', '__builtins__', 'os', 'sys', 'system', 'popen', 'open', 'read', 'communicate']

class RestrictedUnpickler(_pickle.Unpickler):
    def find_class(self, module, name):
        print(module, name)
        if (module in ALLOWED_MODULES and not any(name.startswith(f"{name_}.") for name_ in UNSAFE_NAMES) and not any(name.startswith(f"{name__}") for name__ in BLACKLISTED_NAMES)):
            return super().find_class(module, name)
        raise _pickle.UnpicklingError()
    
def unpickle(data):
    for name_ in BLACKLISTED_NAMES:
        if name_.encode() in b64decode(data):
            return 'hacked'
    return RestrictedUnpickler(BytesIO(b64decode(data))).load()
