.data
    @ --- Variaveis e Constantes ---
    contador_historico: .word 0        @ Guarda quantas linhas ja rodaram
    historico: .space 400              @ Espaco para 100 resultados
    num_0: .double 3.14
    num_1: .double 2.0
    num_2: .double 1.5
    num_3: .double 2.0
    num_4: .double 3.0
    num_5: .double 4.0
    num_6: .double 5.0
    var_MEM: .float 0.0
    num_7: .double 2
    num_8: .double 5.8
    num_9: .double 2.0
    num_10: .double 6.13
    num_11: .double 5.6
    num_12: .double 2.7
    num_13: .double 5
    num_14: .double 3
    num_15: .double 2
    num_16: .double 4
    num_17: .double 6
    num_18: .double 10.0
    num_19: .double 3.0
    num_20: .double 10.0
    num_21: .double 3.0
    num_22: .double 2.0
    num_23: .double 2

.text
.global _start
_start:

    @ --- Linha 1 ---
    ldr r0, =num_0
    vldr s0, [r0]
    vpush {s0}
    ldr r0, =num_1
    vldr s0, [r0]
    vpush {s0}
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vadd.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    @ --- Salva no historico ---
    vpop {s0}                   @ Pega resultado final
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #2              @ offset = linha * 4
    ldr r0, =historico
    add r0, r0, r3              
    vstr s0, [r0]               @ Salva!
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 2 ---
    ldr r0, =num_2
    vldr s0, [r0]
    vpush {s0}
    ldr r0, =num_3
    vldr s0, [r0]
    vpush {s0}
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vmul.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    ldr r0, =num_4
    vldr s0, [r0]
    vpush {s0}
    ldr r0, =num_5
    vldr s0, [r0]
    vpush {s0}
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vmul.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vdiv.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    @ --- Salva no historico ---
    vpop {s0}                   @ Pega resultado final
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #2              @ offset = linha * 4
    ldr r0, =historico
    add r0, r0, r3              
    vstr s0, [r0]               @ Salva!
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 3 ---
    ldr r0, =num_6
    vldr s0, [r0]
    vpush {s0}
    vpop {s0}               @ Pega valor para salvar
    ldr r0, =var_MEM
    vstr s0, [r0]             @ Salva em MEM
    vpush {s0}              @ Mantem na pilha
    @ --- Salva no historico ---
    vpop {s0}                   @ Pega resultado final
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #2              @ offset = linha * 4
    ldr r0, =historico
    add r0, r0, r3              
    vstr s0, [r0]               @ Salva!
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 4 ---
    ldr r0, =num_7
    vldr s0, [r0]
    vpush {s0}
    @ --- Comando RES ---
    vpop {s0}               @ Pega o 'N' (em float)
    vcvt.s32.f32 s0, s0     @ Converte N pra inteiro
    vmov r1, s0             @ Move N para r1
    ldr r2, =contador_historico
    ldr r2, [r2]            @ r2 = linhas executadas
    sub r2, r2, r1          @ r2 = indice (total - N)
    lsl r2, r2, #2          @ Multiplica por 4 bytes
    ldr r0, =historico
    add r0, r0, r2          @ Endereco alvo
    vldr s0, [r0]           @ Carrega o resultado antigo
    vpush {s0}
    @ --- Salva no historico ---
    vpop {s0}                   @ Pega resultado final
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #2              @ offset = linha * 4
    ldr r0, =historico
    add r0, r0, r3              
    vstr s0, [r0]               @ Salva!
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 5 ---
    ldr r0, =num_8
    vldr s0, [r0]
    vpush {s0}
    ldr r0, =num_9
    vldr s0, [r0]
    vpush {s0}
    @ --- Potenciacao (^) ---
    vpop {s1}               @ B (Expoente)
    vpop {s0}               @ A (Base)
    vcvt.s32.f32 s1, s1     @ Converte expoente pra inteiro
    vmov r1, s1             @ r1 = contador do loop
    vmov.f32 s2, #1.0       @ s2 = resultado inicia em 1.0
loop_pot_inicio_0:
    cmp r1, #0              @ B chegou a 0?
    ble loop_pot_fim_0 @ Se sim, sai do loop
    vmul.f32 s2, s2, s0     @ resultado = resultado * base
    sub r1, r1, #1          @ diminui o contador B
    b loop_pot_inicio_0 @ volta pro inicio
loop_pot_fim_0:
    vpush {s2}              @ Guarda o resultado
    @ --- Salva no historico ---
    vpop {s0}                   @ Pega resultado final
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #2              @ offset = linha * 4
    ldr r0, =historico
    add r0, r0, r3              
    vstr s0, [r0]               @ Salva!
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 6 ---
    ldr r0, =num_10
    vldr s0, [r0]
    vpush {s0}
    ldr r0, =num_11
    vldr s0, [r0]
    vpush {s0}
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vadd.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    ldr r0, =num_12
    vldr s0, [r0]
    vpush {s0}
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vmul.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    @ --- Salva no historico ---
    vpop {s0}                   @ Pega resultado final
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #2              @ offset = linha * 4
    ldr r0, =historico
    add r0, r0, r3              
    vstr s0, [r0]               @ Salva!
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 7 ---
    ldr r0, =num_13
    vldr s0, [r0]
    vpush {s0}
    ldr r0, =num_14
    vldr s0, [r0]
    vpush {s0}
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vadd.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    ldr r0, =num_15
    vldr s0, [r0]
    vpush {s0}
    ldr r0, =num_16
    vldr s0, [r0]
    vpush {s0}
    ldr r0, =num_17
    vldr s0, [r0]
    vpush {s0}
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vsub.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vmul.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vdiv.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    @ --- Salva no historico ---
    vpop {s0}                   @ Pega resultado final
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #2              @ offset = linha * 4
    ldr r0, =historico
    add r0, r0, r3              
    vstr s0, [r0]               @ Salva!
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 8 ---
    ldr r0, =num_18
    vldr s0, [r0]
    vpush {s0}
    ldr r0, =num_19
    vldr s0, [r0]
    vpush {s0}
    @ --- Divisao Inteira (//) ---
    vpop {s1}               @ B
    vpop {s0}               @ A
    vdiv.f32 s2, s0, s1     @ A / B
    vcvt.s32.f32 s2, s2     @ Int(A / B)
    vcvt.f32.s32 s2, s2     @ Volta pra Float
    vpush {s2}
    @ --- Salva no historico ---
    vpop {s0}                   @ Pega resultado final
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #2              @ offset = linha * 4
    ldr r0, =historico
    add r0, r0, r3              
    vstr s0, [r0]               @ Salva!
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 9 ---
    ldr r0, =num_20
    vldr s0, [r0]
    vpush {s0}
    ldr r0, =num_21
    vldr s0, [r0]
    vpush {s0}
    @ --- Resto (%) ---
    vpop {s1}               @ B
    vpop {s0}               @ A
    vdiv.f32 s2, s0, s1     @ A / B
    vcvt.s32.f32 s2, s2     @ Int(A / B)
    vcvt.f32.s32 s2, s2     @ Float(Int(A / B))
    vmul.f32 s2, s2, s1     @ (Int(A / B) * B)
    vsub.f32 s2, s0, s2     @ A - (Int(A / B) * B)
    vpush {s2}
    @ --- Salva no historico ---
    vpop {s0}                   @ Pega resultado final
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #2              @ offset = linha * 4
    ldr r0, =historico
    add r0, r0, r3              
    vstr s0, [r0]               @ Salva!
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 10 ---
    ldr r0, =var_MEM
    vldr s0, [r0]             @ Le de MEM
    vpush {s0}
    ldr r0, =num_22
    vldr s0, [r0]
    vpush {s0}
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vmul.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    ldr r0, =num_23
    vldr s0, [r0]
    vpush {s0}
    @ --- Comando RES ---
    vpop {s0}               @ Pega o 'N' (em float)
    vcvt.s32.f32 s0, s0     @ Converte N pra inteiro
    vmov r1, s0             @ Move N para r1
    ldr r2, =contador_historico
    ldr r2, [r2]            @ r2 = linhas executadas
    sub r2, r2, r1          @ r2 = indice (total - N)
    lsl r2, r2, #2          @ Multiplica por 4 bytes
    ldr r0, =historico
    add r0, r0, r2          @ Endereco alvo
    vldr s0, [r0]           @ Carrega o resultado antigo
    vpush {s0}
    vpop {s1}               @ Tira B
    vpop {s0}               @ Tira A
    vadd.f64 s2, s0, s1      @ Calcula S2 = A op B
    vpush {s2}              @ Devolve pra pilha
    @ --- Salva no historico ---
    vpop {s0}                   @ Pega resultado final
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #2              @ offset = linha * 4
    ldr r0, =historico
    add r0, r0, r3              
    vstr s0, [r0]               @ Salva!
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Fim do Programa ---
    mov r7, #1                  @ Syscall exit
    svc #0