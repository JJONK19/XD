.section .data
input_file:    .asciz "input.txt"    // Nombre del archivo de entrada
mode:          .asciz "r"            // Modo de apertura del archivo (lectura)
buffer:        .space 1000           // Espacio para leer el contenido del archivo
numbers:       .space 4000           // Espacio para almacenar hasta 1000 números (4 bytes cada uno)
error_msg:     .asciz "Error al abrir el archivo\n" // Mensaje de error al abrir el archivo
first_value_msg: .asciz "d\n"  // Nuevo mensaje para el primer valor

.section .bss
frequencies:   .space 4096           // Espacio para contar la frecuencia de cada número

.section .text
.global _start

.extern fopen
.extern fread
.extern fclose
.extern printf
.extern atoi

_start:
    // Abrir el archivo
    ldr x0, =input_file
    ldr x1, =mode
    bl fopen
    cbz x0, file_error
    mov x19, x0  // Guardar el puntero del archivo

    // Leer el archivo
    ldr x0, =buffer
    mov x1, #1
    mov x2, #1000
    mov x3, x19
    bl fread

    // Cerrar el archivo
    mov x0, x19
    bl fclose

    // Inicializar variables
    mov x20, #0  // Suma total
    mov x27, #0  // Contador de números
    ldr x28, =numbers  // Arreglo para almacenar números

    // Inicializar variables para la moda
    ldr x24, =frequencies
    mov x25, #0  // Frecuencia más alta
    mov x26, #0  // Valor de la moda

    // Procesar buffer
    ldr x21, =buffer  // Puntero al buffer

process_loop:
    mov x0, x21  // Pasar la dirección actual como argumento a atoi
    bl atoi
    cbz x0, end_processing  // Si atoi devuelve 0, hemos terminado

    // Guardar el número
    str w0, [x28, x27, lsl #2]
    add x27, x27, #1  // Incrementar contador de números

    // Actualizar suma total
    add x20, x20, x0

    // Actualizar frecuencias y moda
    lsl x1, x0, #2
    add x1, x24, x1
    ldr w2, [x1]
    add w2, w2, #1
    str w2, [x1]
    cmp w2, w25
    ble skip_moda_update
    mov w25, w2
    mov x26, x0

skip_moda_update:
    // Avanzar al siguiente número
    mov x1, #0
find_next:
    ldrb w2, [x21], #1
    cmp w2, #','
    beq process_loop
    cmp w2, #0
    beq end_processing
    b find_next

end_processing:
    mov x1, x27

    // Calcular y imprimir promedio
    ucvtf d0, x20
    ucvtf d1, x27
    fdiv d0, d0, d1

    // Imprimir primer valor (minimo)
    mov x8, #93
    ldr x0, [x28]
    svc #0

odd_median:
    mov x0, x27
    lsr x0, x0, #1
    ldr w2, [x28, x0, lsl #2]
    ucvtf d0, w2


file_error:
    ldr x0, =error_msg
    bl printf
    mov x8, #93
    mov x0, #1
    svc #0