section .data
    msg: db "x is greater than 3", 10, 0

section .bss
    x: resq 1

section .text
    global main
    extern printf

main:
    mov rax, 5          ; rax = 5
    mov [x], rax        ; x = 5

    mov rax, [x]        ; load x
    cmp rax, 3          ; compare x with 3
    jle .endif          ; if x <= 3, jump to endif

    ; if-body: x > 3
    lea rdi, [rel msg]  ; rdi = address of msg
    xor eax, eax        ; clear rax for printf
    call printf

.endif:
    mov rax, 0
    ret