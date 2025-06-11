;initializing variables
section .data
    fmt: db "%d", 10, 0 ; format string for printf

; .bss - section for uninitialized data
; variables that will be initialized at runtime
section .bss
    x: resq 1 ; reserve space for one quadword (8 bytes)

; .text - section for code
section .text
    global main ; make main function globally accessible
    extern printf ; declare printf function from C standard library
main:
    mov r10, 5 ; initialize r10 with value 5
    mov [x], r10 ; store value of r10 into variable x
    lea rdi, [rel fmt] ; load address of format string into rdi
    mov rsi, [x] ; load value of x into rsi for printf
    xor eax, eax ; clear rax for printf
    call printf ; call printf to print the value of x
    mov rax, 0 ; return 0 from main
    ret ; return from main