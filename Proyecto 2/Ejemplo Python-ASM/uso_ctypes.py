import ctypes

# Cargar la biblioteca compartida
libadd = ctypes.CDLL('./libadd.so')

# Definir la función y sus argumentos y retorno
libadd.add_numbers.argtypes = (ctypes.c_int, ctypes.c_int)
libadd.add_numbers.restype = ctypes.c_int

# Llamar a la función
result = libadd.add_numbers(10, 20)
print(f"Resultado: {result}")
