# Instrucciones
1. Compilar el codigo de ASM: as -o add.o add.s
2. Crear la libreria de c++: gcc -shared -o libadd.so add.o
3. Correr el codigo de python: python uso_ctypes.py