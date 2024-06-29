.section .data
archivo_entrada:  .asciz "input.txt"    // Nombre del archivo de entrada
modo:             .asciz "r"            // Modo de apertura del archivo (lectura)
buffer:           .space 1000           // Espacio para leer el contenido del archivo
mensaje_resultado: .asciz "Números menores o iguales a 150: %d\n"  // Mensaje para mostrar el resultado
mensaje_error:    .asciz "Error al abrir el archivo\n" // Mensaje de error al abrir el archivo

.section .text
.global _start

.extern fopen
.extern fread
.extern fclose
.extern printf
.extern strtod

_start:
    // Abrir el archivo
    ldr x0, =archivo_entrada
    ldr x1, =modo
    bl fopen
    cbz x0, error_archivo
    mov x19, x0          // Puntero del archivo que se abrió

    // Leer el archivo
    ldr x0, =buffer
    mov x1, #1           // Tamaño de lectura: 1 byte
    mov x2, #1000        // Número máximo de elementos a leer
    mov x3, x19
    bl fread

    // Cerrar el archivo 
    mov x0, x19
    bl fclose

    // Inicializar variables
    mov x20, #0          // Contador de números menores o iguales a 150
    ldr x21, =buffer     // Dirección del buffer

bucle_analisis:
    mov x0, x21          // Dirección actual del buffer
    mov x1, x21          // Dirección para el puntero de fin
    bl strtod            // Convertir a double
    
    // Comparar el número con 150.0
    fmov d1, #151.0      // Comparar con 151.0
    fcmp d0, d1
    bge saltar_incremento  // Si es mayor o igual a 151, no incrementar
    add x20, x20, #1     // Incrementar el contador si es menor a 151 (es decir, <= 150)

saltar_incremento:
    // Avanzar al siguiente número
    mov x21, x1          // Actualizar la posición en el buffer
    ldrb w2, [x21]
    cmp w2, #0           // Comprobar si hemos llegado al final
    beq fin_analisis
    add x21, x21, #1     // Saltar la coma
    b bucle_analisis

fin_analisis:
    // Imprimir el resultado
    ldr x0, =mensaje_resultado
    mov x1, x20
    bl printf

    // Salir del programa
    mov x8, #93          // syscall: exit
    mov x0, x20          // Poner el contador como código de salida
    svc #0

error_archivo:
    ldr x0, =mensaje_error
    bl printf
    mov x8, #93          // syscall: exit
    mov x0, #1           // Código de error
    svc #0