;simple print

;.data - section for initialized data
; data does not change during program execution
section .data
    fmt: db "%d", 10, 0 ; format string for printf
    msg: db "Hello, World!", 10, 0 ; message to print

section .text
    global main
    extern printf

main:
    lea rdi, [rel msg] ; load address of message into rdi
    xor rax, rax ; clear rax for printf
    call printf ; call printf to print the message
    mov rax, 0 ; return 0 from main
    ret ; return from main

