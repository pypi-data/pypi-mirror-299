import os
import sys

print(f"Initializing base64c package")
print(f"Python version: {sys.version}")
print(f"sys.path: {sys.path}")
print(f"Current directory: {os.getcwd()}")
print(f"Contents of current directory: {os.listdir('.')}")

try:
    from .base64c import b64encode, b64decode, standard_b64decode, standard_b64encode, urlsafe_b64decode, urlsafe_b64encode
    print("Successfully imported from .base64c")
except ImportError as e:
    print(f"Failed to import from .base64c: {e}")
    print(f"Contents of parent directory: {os.listdir('..')}")
    print(f"Contents of current package directory: {os.listdir(os.path.dirname(__file__))}")
    print(f"sys.modules keys: {list(sys.modules.keys())}")
    if 'base64c.base64c' in sys.modules:
        print(f"base64c.base64c module: {sys.modules['base64c.base64c']}")
    else:
        print("base64c.base64c not in sys.modules")

__all__ = ['b64encode', 'b64decode', 'standard_b64decode', 'standard_b64encode', 'urlsafe_b64decode', 'urlsafe_b64encode']

print(f"Finished initializing base64c package. __all__: {__all__}")
print(f"Final contents of the base64c module: {dir()}")