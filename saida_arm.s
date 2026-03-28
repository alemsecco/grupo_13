.data
    @ --- Variaveis e Constantes ---
    contador_historico: .word 0        @ Guarda quantas linhas ja rodaram
    historico: .space 800              @ Espaco para 100 resultados (8 bytes cada)
    const_um: .double 1.0              @ Constante fixa para a potenciacao
    base_leds: .word 0xFF200000        @ Endereco de hardware dos LEDs vermelhos
    num_0: .double 3.14
    num_1: .double 2.0
    num_2: .double 1.5
    num_3: .double 2.0
    num_4: .double 3.0
    num_5: .double 4.0
    num_6: .double 5.0
    var_X: .double 0.0
    var_MEM: .double 0.0
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
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_1
    vldr d0, [r0]
    vpush {d0}
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vadd.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    @ --- Salva no historico e Exibe nos LEDs ---
    vpop {d0}                   @ Pega resultado final
    @ 1. Imprime o valor inteiro nos LEDs vermelhos (Hardware I/O)
    vcvt.s32.f64 s0, d0         @ Converte D0 para inteiro de 32bits
    vmov r4, s0                 @ Move para R4
    ldr r5, =base_leds          @ Carrega endereco dos LEDs
    ldr r5, [r5]                @ Desreferencia
    str r4, [r5]                @ Liga os LEDs correspondentes ao numero binario
    @ 2. Salva no array de historico
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #3              @ offset = linha * 8
    ldr r0, =historico
    add r0, r0, r3              
    vstr d0, [r0]               @ Salva
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 2 ---
    ldr r0, =num_2
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_3
    vldr d0, [r0]
    vpush {d0}
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vmul.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    ldr r0, =num_4
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_5
    vldr d0, [r0]
    vpush {d0}
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vmul.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vdiv.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    @ --- Salva no historico e Exibe nos LEDs ---
    vpop {d0}                   @ Pega resultado final
    @ 1. Imprime o valor inteiro nos LEDs vermelhos (Hardware I/O)
    vcvt.s32.f64 s0, d0         @ Converte D0 para inteiro de 32bits
    vmov r4, s0                 @ Move para R4
    ldr r5, =base_leds          @ Carrega endereco dos LEDs
    ldr r5, [r5]                @ Desreferencia
    str r4, [r5]                @ Liga os LEDs correspondentes ao numero binario
    @ 2. Salva no array de historico
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #3              @ offset = linha * 8
    ldr r0, =historico
    add r0, r0, r3              
    vstr d0, [r0]               @ Salva
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 3 ---
    ldr r0, =num_6
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =var_X
    vldr d0, [r0]             @ Le de X
    vpush {d0}
    ldr r0, =var_MEM
    vldr d0, [r0]             @ Le de MEM
    vpush {d0}
    @ --- Salva no historico e Exibe nos LEDs ---
    vpop {d0}                   @ Pega resultado final
    @ 1. Imprime o valor inteiro nos LEDs vermelhos (Hardware I/O)
    vcvt.s32.f64 s0, d0         @ Converte D0 para inteiro de 32bits
    vmov r4, s0                 @ Move para R4
    ldr r5, =base_leds          @ Carrega endereco dos LEDs
    ldr r5, [r5]                @ Desreferencia
    str r4, [r5]                @ Liga os LEDs correspondentes ao numero binario
    @ 2. Salva no array de historico
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #3              @ offset = linha * 8
    ldr r0, =historico
    add r0, r0, r3              
    vstr d0, [r0]               @ Salva
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 4 ---
    ldr r0, =num_7
    vldr d0, [r0]
    vpush {d0}
    @ --- Comando RES ---
    vpop {d0}               @ Pega o 'N'
    vcvt.s32.f64 s2, d0     @ Converte N pra int32 no s2 (seguro)
    vmov r1, s2             @ Move N para r1
    ldr r2, =contador_historico
    ldr r2, [r2]            @ r2 = linhas executadas
    sub r2, r2, r1          @ r2 = indice (total - N)
    lsl r2, r2, #3          @ Multiplica por 8 bytes (Double)
    ldr r0, =historico
    add r0, r0, r2          @ Endereco alvo
    vldr d0, [r0]           @ Carrega o resultado antigo
    vpush {d0}
    @ --- Salva no historico e Exibe nos LEDs ---
    vpop {d0}                   @ Pega resultado final
    @ 1. Imprime o valor inteiro nos LEDs vermelhos (Hardware I/O)
    vcvt.s32.f64 s0, d0         @ Converte D0 para inteiro de 32bits
    vmov r4, s0                 @ Move para R4
    ldr r5, =base_leds          @ Carrega endereco dos LEDs
    ldr r5, [r5]                @ Desreferencia
    str r4, [r5]                @ Liga os LEDs correspondentes ao numero binario
    @ 2. Salva no array de historico
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #3              @ offset = linha * 8
    ldr r0, =historico
    add r0, r0, r3              
    vstr d0, [r0]               @ Salva
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 5 ---
    ldr r0, =num_8
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_9
    vldr d0, [r0]
    vpush {d0}
    @ --- Potenciacao (^) em 64-bits puros ---
    vpop {d1}               @ B (Expoente)
    vpop {d0}               @ A (Base)
    ldr r0, =const_um       @ Pega o endereco do 1.0 na memoria
    vldr d2, [r0]           @ d2 = 1.0 (O Resultado inicia em 1)
    vldr d3, [r0]           @ d3 = 1.0 (Constante de subtracao pro expoente)
loop_pot_0:
    vcmp.f64 d1, #0.0       @ Compara Expoente (B) com 0.0 diretamente na FPU
    vmrs APSR_nzcv, fpscr   @ Passa as flags da FPU para a CPU
    ble fim_pot_0   @ Se Expoente <= 0.0, sai do loop
    vmul.f64 d2, d2, d0     @ Resultado = Resultado * Base
    vsub.f64 d1, d1, d3     @ Expoente = Expoente - 1.0
    b loop_pot_0    @ Volta pro inicio
fim_pot_0:
    vpush {d2}              @ Guarda o Resultado na pilha
    @ --- Salva no historico e Exibe nos LEDs ---
    vpop {d0}                   @ Pega resultado final
    @ 1. Imprime o valor inteiro nos LEDs vermelhos (Hardware I/O)
    vcvt.s32.f64 s0, d0         @ Converte D0 para inteiro de 32bits
    vmov r4, s0                 @ Move para R4
    ldr r5, =base_leds          @ Carrega endereco dos LEDs
    ldr r5, [r5]                @ Desreferencia
    str r4, [r5]                @ Liga os LEDs correspondentes ao numero binario
    @ 2. Salva no array de historico
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #3              @ offset = linha * 8
    ldr r0, =historico
    add r0, r0, r3              
    vstr d0, [r0]               @ Salva
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 6 ---
    ldr r0, =num_10
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_11
    vldr d0, [r0]
    vpush {d0}
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vadd.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    ldr r0, =num_12
    vldr d0, [r0]
    vpush {d0}
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vmul.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    @ --- Salva no historico e Exibe nos LEDs ---
    vpop {d0}                   @ Pega resultado final
    @ 1. Imprime o valor inteiro nos LEDs vermelhos (Hardware I/O)
    vcvt.s32.f64 s0, d0         @ Converte D0 para inteiro de 32bits
    vmov r4, s0                 @ Move para R4
    ldr r5, =base_leds          @ Carrega endereco dos LEDs
    ldr r5, [r5]                @ Desreferencia
    str r4, [r5]                @ Liga os LEDs correspondentes ao numero binario
    @ 2. Salva no array de historico
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #3              @ offset = linha * 8
    ldr r0, =historico
    add r0, r0, r3              
    vstr d0, [r0]               @ Salva
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 7 ---
    ldr r0, =num_13
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_14
    vldr d0, [r0]
    vpush {d0}
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vadd.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    ldr r0, =num_15
    vldr d0, [r0]
    vpush {d0}
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vmul.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    ldr r0, =num_16
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_17
    vldr d0, [r0]
    vpush {d0}
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vsub.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vdiv.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    @ --- Salva no historico e Exibe nos LEDs ---
    vpop {d0}                   @ Pega resultado final
    @ 1. Imprime o valor inteiro nos LEDs vermelhos (Hardware I/O)
    vcvt.s32.f64 s0, d0         @ Converte D0 para inteiro de 32bits
    vmov r4, s0                 @ Move para R4
    ldr r5, =base_leds          @ Carrega endereco dos LEDs
    ldr r5, [r5]                @ Desreferencia
    str r4, [r5]                @ Liga os LEDs correspondentes ao numero binario
    @ 2. Salva no array de historico
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #3              @ offset = linha * 8
    ldr r0, =historico
    add r0, r0, r3              
    vstr d0, [r0]               @ Salva
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 8 ---
    ldr r0, =num_18
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_19
    vldr d0, [r0]
    vpush {d0}
    @ --- Divisao Inteira (//) em 64-bits puros ---
    vpop {d1}               @ B (Divisor)
    vpop {d0}               @ A (Dividendo)
    vsub.f64 d2, d2, d2     @ d2 = 0.0 (Quociente inicia zerado)
    ldr r0, =const_um       @ Pega o 1.0 da memoria
    vldr d3, [r0]           @ d3 = 1.0 (Incremento)
loop_div_int_1:
    vcmp.f64 d0, d1         @ Compara A com B
    vmrs APSR_nzcv, fpscr   @ Passa as flags da FPU para a CPU
    blt fim_div_int_1 @ Se A < B, sai do loop
    vsub.f64 d0, d0, d1     @ A = A - B
    vadd.f64 d2, d2, d3     @ Quociente = Quociente + 1.0
    b loop_div_int_1 @ Volta pro inicio do loop
fim_div_int_1:
    vpush {d2}              @ Guarda o Quociente na pilha
    @ --- Salva no historico e Exibe nos LEDs ---
    vpop {d0}                   @ Pega resultado final
    @ 1. Imprime o valor inteiro nos LEDs vermelhos (Hardware I/O)
    vcvt.s32.f64 s0, d0         @ Converte D0 para inteiro de 32bits
    vmov r4, s0                 @ Move para R4
    ldr r5, =base_leds          @ Carrega endereco dos LEDs
    ldr r5, [r5]                @ Desreferencia
    str r4, [r5]                @ Liga os LEDs correspondentes ao numero binario
    @ 2. Salva no array de historico
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #3              @ offset = linha * 8
    ldr r0, =historico
    add r0, r0, r3              
    vstr d0, [r0]               @ Salva
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 9 ---
    ldr r0, =num_20
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =num_21
    vldr d0, [r0]
    vpush {d0}
    @ --- Resto (%) em 64-bits puros ---
    vpop {d1}               @ B (Divisor)
    vpop {d0}               @ A (Dividendo)
loop_mod_2:
    vcmp.f64 d0, d1         @ Compara A com B
    vmrs APSR_nzcv, fpscr   @ Passa as flags da FPU para a CPU
    blt fim_mod_2   @ Se A < B, o que sobrou no d0 eh o resto
    vsub.f64 d0, d0, d1     @ A = A - B
    b loop_mod_2    @ Volta pro inicio do loop
fim_mod_2:
    vpush {d0}              @ Guarda o Resto na pilha
    @ --- Salva no historico e Exibe nos LEDs ---
    vpop {d0}                   @ Pega resultado final
    @ 1. Imprime o valor inteiro nos LEDs vermelhos (Hardware I/O)
    vcvt.s32.f64 s0, d0         @ Converte D0 para inteiro de 32bits
    vmov r4, s0                 @ Move para R4
    ldr r5, =base_leds          @ Carrega endereco dos LEDs
    ldr r5, [r5]                @ Desreferencia
    str r4, [r5]                @ Liga os LEDs correspondentes ao numero binario
    @ 2. Salva no array de historico
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #3              @ offset = linha * 8
    ldr r0, =historico
    add r0, r0, r3              
    vstr d0, [r0]               @ Salva
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Linha 10 ---
    ldr r0, =var_X
    vldr d0, [r0]             @ Le de X
    vpush {d0}
    ldr r0, =num_22
    vldr d0, [r0]
    vpush {d0}
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vmul.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    ldr r0, =num_23
    vldr d0, [r0]
    vpush {d0}
    @ --- Comando RES ---
    vpop {d0}               @ Pega o 'N'
    vcvt.s32.f64 s2, d0     @ Converte N pra int32 no s2 (seguro)
    vmov r1, s2             @ Move N para r1
    ldr r2, =contador_historico
    ldr r2, [r2]            @ r2 = linhas executadas
    sub r2, r2, r1          @ r2 = indice (total - N)
    lsl r2, r2, #3          @ Multiplica por 8 bytes (Double)
    ldr r0, =historico
    add r0, r0, r2          @ Endereco alvo
    vldr d0, [r0]           @ Carrega o resultado antigo
    vpush {d0}
    vpop {d1}               @ Tira B
    vpop {d0}               @ Tira A
    vadd.f64 d2, d0, d1      @ Calcula S2 = A op B
    vpush {d2}              @ Devolve pra pilha
    @ --- Salva no historico e Exibe nos LEDs ---
    vpop {d0}                   @ Pega resultado final
    @ 1. Imprime o valor inteiro nos LEDs vermelhos (Hardware I/O)
    vcvt.s32.f64 s0, d0         @ Converte D0 para inteiro de 32bits
    vmov r4, s0                 @ Move para R4
    ldr r5, =base_leds          @ Carrega endereco dos LEDs
    ldr r5, [r5]                @ Desreferencia
    str r4, [r5]                @ Liga os LEDs correspondentes ao numero binario
    @ 2. Salva no array de historico
    ldr r1, =contador_historico
    ldr r2, [r1]                @ r2 = linha atual
    mov r3, r2                  
    lsl r3, r3, #3              @ offset = linha * 8
    ldr r0, =historico
    add r0, r0, r3              
    vstr d0, [r0]               @ Salva
    add r2, r2, #1              @ Incrementa linha
    str r2, [r1]                

    @ --- Fim do Programa ---
_fim:
    b _fim                      @ Loop infinito para segurar o processador