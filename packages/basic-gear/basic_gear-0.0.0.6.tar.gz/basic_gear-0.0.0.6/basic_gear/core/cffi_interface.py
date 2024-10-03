from cffi import FFI
import os
import platform

ffi = FFI()

# Dichiarazioni delle funzioni C che vogliamo esporre a Python
ffi.cdef("""
    float add(float a, float b);
    float multiply(float a, float b);
    float subtract(float a, float b);
    float divide(float a, float b);
    float mod(float a, float b);
    int create_channel(int port);
""")


# Carichiamo la libreria C compilata
current_dir = os.path.dirname(__file__)
arch = platform.machine()


if platform.system() == 'Darwin':  # MacOS
    if arch == "x86_64": # Intel
        lib_path = os.path.join(current_dir, "libmath_operations.dylib")
        lib_path_tor = os.path.join(current_dir, "libtor_operations.dylib")
    elif arch == "arm64" or arch == "arm64e": 
        lib_path = os.path.join(current_dir, "libmath_operations_arm.dylib")
        lib_path_tor = os.path.join(current_dir, "libtor_operations_arm.dylib")

if platform.system() == 'Linux':  # Linux
    lib_path = os.path.join(current_dir, "libmath_operations.so")
    lib_path_tor = os.path.join(current_dir, "libtor_operations.so")

elif platform.system() == 'Windows':  # Windows
    lib_path = os.path.join(current_dir, "libmath_operations.dll")
    lib_path_tor = os.path.join(current_dir, "libtor_operations.dll")

else:
    raise OSError(f"Unsupported platform: {platform.system()}")

C = ffi.dlopen(lib_path)

# Carica la libreria
C = ffi.dlopen(lib_path)
TOR = ffi.dlopen(lib_path_tor)


# Wrapper per esporre le funzioni a Python
def add(a, b):
    return C.add(a, b)

def multiply(a, b):
    return C.multiply(a, b)

def subtract(a, b):
    return C.subtract(a, b)

def divide(a, b):
    return C.divide(a, b)

def mod(a, b):
    return C.mod(a, b)

def create_channel(port):
    return TOR.create_channel(port)


