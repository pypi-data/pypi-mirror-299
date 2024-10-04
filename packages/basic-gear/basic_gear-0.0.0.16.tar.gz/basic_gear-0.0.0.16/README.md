# basic-gear

gcc -shared -o basic_gear/shared_library/libmath_operations.dylib -fPIC basic_gear/src/math_operations.c
test : file basic_gear/shared_library/libmath_operations.dylib
out : basic_gear/shared_library/libmath_operations.dylib: Mach-O 64-bit dynamically linked shared library arm64

test: file basic_gear/shared_library/libmath_operations.dll
out: basic_gear/shared_library/libmath_operations.dll: PE32+ executable (DLL) (console) x86-64, for MS Windows

test: file basic_gear/shared_library/libmath_operations_arm.dylib
out: basic_gear/shared_library/libmath_operations_arm.dylib: Mach-O 64-bit dynamically linked shared library arm64
