section .data
    fmt: db "%d", 10, 0

section .bss
    x: resq 1

section .text
    global main
    extern printf

main:
    mov rax, 5          ; rax = 5
    mov [x], rax        ; x = 5

.loop:
    mov rax, [x]        ; load x
    cmp rax, 0          ; compare x with 0
    jle .end            ; if x <= 0, exit loop

    mov rsi, rax        ; 2nd arg: value to print
    lea rdi, [rel fmt]  ; 1st arg: format string
    xor eax, eax        ; clear rax for printf
    call printf

    mov rax, [x]        ; load x
    sub rax, 1          ; x = x - 1
    mov [x], rax        ; store x

    jmp .loop           ; repeat loop

.end:
    mov rax, 0
    ret