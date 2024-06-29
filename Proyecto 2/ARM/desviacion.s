.section .data
input_file:     .asciz "input.txt"
buffer:         .space 1024
numbers:        .space 1024
count:          .quad 0
sum:            .quad 0

.section .text
.global _start
_start:
    // Abrir archivo de entrada
    mov x0, #-100
    ldr x1, =input_file
    mov x2, #0
    mov x8, #56
    svc #0
    cbz x0, error
    mov x9, x0
    // Leer contenido del archivo
    mov x0, x9
    ldr x1, =buffer
    mov x2, #1024
    mov x8, #63
    svc #0
    cbz x0, error
    mov x19, x0
    // Cerrar archivo de entrada
    mov x0, x9
    mov x8, #57
    svc #0
    // Parsear números
    mov x20, #0
    ldr x21, =numbers
    mov x22, #0
    ldr x1, =buffer
parse_loop:
    mov x0, x1
    bl atoi
    cmp x0, #-1
    beq parse_end
    str w0, [x21, x22, lsl #2]
    add x22, x22, #1
    add x20, x20, x0
parse_next:
    ldrb w2, [x1], #1
    cmp w2, #','
    b.eq parse_loop
    cmp w2, #0
    b.ne parse_next
parse_end:
    ldr x23, =sum
    str x20, [x23]
    ldr x23, =count
    str x22, [x23]
    // Calcular media
    mov x23, #10
    mul x20, x20, x23
    sdiv x24, x20, x22
    // Calcular varianza
    mov x25, #0
    mov x26, #0
calc_variance_loop:
    ldr w27, [x21, x26, lsl #2]
    mov x28, #10
    mul x27, x27, x28
    sub x27, x27, x24
    mul x27, x27, x27
    add x25, x25, x27
    add x26, x26, #1
    cmp x26, x22
    b.lt calc_variance_loop
    sub x22, x22, #1
    sdiv x25, x25, x22
    // Calcular desviación estándar
    mov x0, x25
    bl sqrt
    
    // Convertir el resultado a un entero (redondeando)
    add x0, x0, #5  // Agregar 5 para redondear
    mov x1, #10
    udiv x0, x0, x1  // Dividir por 10 para obtener el entero redondeado
    
    // Salir del programa con el resultado como código de retorno
    mov x8, #93     // Syscall número para exit
    svc #0

error:
    mov x0, #-1
    mov x8, #93
    svc #0

// Funciones auxiliares
atoi:
    mov x2, #0
    mov x4, #0
atoi_loop:
    ldrb w3, [x0], #1
    cmp w3, #','
    beq atoi_end
    cmp w3, #0
    beq atoi_end
    sub w3, w3, #'0'
    cmp w3, #9
    bhi atoi_end
    mov x5, #10
    mul x2, x2, x5
    add x2, x2, x3
    mov x4, #1
    b atoi_loop
atoi_end:
    cmp x4, #0
    b.eq atoi_invalid
    mov x0, x2
    ret
atoi_invalid:
    mov x0, #-1
    ret

sqrt:
    mov x1, x0
    lsr x0, x0, #1
    mov x2, #0
sqrt_loop:
    mov x3, x0
    udiv x0, x1, x0
    add x0, x0, x3
    lsr x0, x0, #1
    add x2, x2, #1
    cmp x2, #20
    b.lt sqrt_loop
    ret