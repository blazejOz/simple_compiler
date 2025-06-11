section .data
    msg_gt: db "x is greater than 3", 10, 0
    msg_le: db "x is less or equal to 3", 10, 0

section .bss
    x: resq 1

section .text
    global main
    extern printf

main:
    mov rax, 2          ; rax = 2
    mov [x], rax        ; x = 2

    mov rax, [x]        ; load x
    cmp rax, 3          ; compare x with 3
    jle .else           ; if x <= 3, jump to else

    ; if-body: x > 3
    lea rdi, [rel msg_gt]
    xor eax, eax
    call printf
    jmp .endif

.else:
    lea rdi, [rel msg_le]
    xor eax, eax
    call printf

.endif:
    mov rax, 0
    ret