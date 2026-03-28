# Alex Menegatti Secco @alemsecco
# Mariana de Castro @maricastroo
# Grupo 13

def gerarAssembly(todas_linhas_rpn):
    # seção de dados (memória RAM)
    data_section = [
        ".data",
        "    @ --- Variaveis e Constantes ---",
        "    contador_historico: .word 0        @ Guarda quantas linhas ja rodaram",
        "    historico: .space 800              @ Espaco para 100 resultados (8 bytes cada)",
        "    const_um: .double 1.0              @ Constante fixa para a potenciacao",
        "    base_leds: .word 0xFF200000        @ Endereco de hardware dos LEDs vermelhos"
    ]
    
    # seção de texto
    text_section = [
        ".text",
        ".global _start",
        "_start:"
    ]
    
    contador_numeros = 0
    contador_loops = 0  
    variaveis_criadas = set()
    
    # operações em precisão de 64 bits (double)
    mapa_instrucoes = {'+': 'vadd.f64', '-': 'vsub.f64', '*': 'vmul.f64', '/': 'vdiv.f64'}

    for numero_linha, tokens in enumerate(todas_linhas_rpn, start=0):
        text_section.append(f"\n    @ --- Linha {numero_linha + 1} ---")
        
        for i, token in enumerate(tokens):
            if token in ['(', ')']: 
                continue

            # NÚMERO
            if token.lstrip('-').replace('.', '', 1).isdigit():
                nome_const = f"num_{contador_numeros}"
                data_section.append(f"    {nome_const}: .double {token}")
                
                text_section.extend([
                    f"    ldr r0, ={nome_const}",
                    f"    vldr d0, [r0]",
                    f"    vpush {{d0}}"
                ])
                contador_numeros += 1

            # OPERAÇÕES BÁSICAS (+, -, *, /)
            elif token in mapa_instrucoes:
                inst = mapa_instrucoes[token]
                text_section.extend([
                    f"    vpop {{d1}}               @ Tira B",
                    f"    vpop {{d0}}               @ Tira A",
                    f"    {inst} d2, d0, d1      @ Calcula S2 = A op B",
                    f"    vpush {{d2}}              @ Devolve pra pilha"
                ])

            # DIVISÃO INTEIRA (//)
            elif token == '//':
                loop_id = contador_loops
                contador_loops += 1
                text_section.extend([
                    "    @ --- Divisao Inteira (//) em 64-bits puros ---",
                    "    vpop {d1}               @ B (Divisor)",
                    "    vpop {d0}               @ A (Dividendo)",
                    "    vsub.f64 d2, d2, d2     @ d2 = 0.0 (Quociente inicia zerado)",
                    "    ldr r0, =const_um       @ Pega o 1.0 da memoria",
                    "    vldr d3, [r0]           @ d3 = 1.0 (Incremento)",
                    f"loop_div_int_{loop_id}:",
                    "    vcmp.f64 d0, d1         @ Compara A com B",
                    "    vmrs APSR_nzcv, fpscr   @ Passa as flags da FPU para a CPU",
                    f"    blt fim_div_int_{loop_id} @ Se A < B, sai do loop",
                    "    vsub.f64 d0, d0, d1     @ A = A - B",
                    "    vadd.f64 d2, d2, d3     @ Quociente = Quociente + 1.0",
                    f"    b loop_div_int_{loop_id} @ Volta pro inicio do loop",
                    f"fim_div_int_{loop_id}:",
                    "    vpush {d2}              @ Guarda o Quociente na pilha"
                ])

            # RESTO DA DIVISÃO (%)
            elif token == '%':
                loop_id = contador_loops
                contador_loops += 1
                text_section.extend([
                    "    @ --- Resto (%) em 64-bits puros ---",
                    "    vpop {d1}               @ B (Divisor)",
                    "    vpop {d0}               @ A (Dividendo)",
                    f"loop_mod_{loop_id}:",
                    "    vcmp.f64 d0, d1         @ Compara A com B",
                    "    vmrs APSR_nzcv, fpscr   @ Passa as flags da FPU para a CPU",
                    f"    blt fim_mod_{loop_id}   @ Se A < B, o que sobrou no d0 eh o resto",
                    "    vsub.f64 d0, d0, d1     @ A = A - B",
                    f"    b loop_mod_{loop_id}    @ Volta pro inicio do loop",
                    f"fim_mod_{loop_id}:",
                    "    vpush {d0}              @ Guarda o Resto na pilha"
                ])

            # POTENCIAÇÃO (^)
            elif token == '^':
                loop_id = contador_loops
                contador_loops += 1
                text_section.extend([
                    "    @ --- Potenciacao (^) em 64-bits puros ---",
                    "    vpop {d1}               @ B (Expoente)",
                    "    vpop {d0}               @ A (Base)",
                    "    ldr r0, =const_um       @ Pega o endereco do 1.0 na memoria",
                    "    vldr d2, [r0]           @ d2 = 1.0 (O Resultado inicia em 1)",
                    "    vldr d3, [r0]           @ d3 = 1.0 (Constante de subtracao pro expoente)",
                    f"loop_pot_{loop_id}:",
                    "    vcmp.f64 d1, #0.0       @ Compara Expoente (B) com 0.0 diretamente na FPU",
                    "    vmrs APSR_nzcv, fpscr   @ Passa as flags da FPU para a CPU",
                    f"    ble fim_pot_{loop_id}   @ Se Expoente <= 0.0, sai do loop",
                    "    vmul.f64 d2, d2, d0     @ Resultado = Resultado * Base",
                    "    vsub.f64 d1, d1, d3     @ Expoente = Expoente - 1.0",
                    f"    b loop_pot_{loop_id}    @ Volta pro inicio",
                    f"fim_pot_{loop_id}:",
                    "    vpush {d2}              @ Guarda o Resultado na pilha"
                ])

            # COMANDO RES (histórico)
            elif token == "RES":
                text_section.extend([
                    "    @ --- Comando RES ---",
                    "    vpop {d0}               @ Pega o 'N'",
                    "    vcvt.s32.f64 s2, d0     @ Converte N pra int32 no s2 (seguro)",
                    "    vmov r1, s2             @ Move N para r1",
                    "    ldr r2, =contador_historico",
                    "    ldr r2, [r2]            @ r2 = linhas executadas",
                    "    sub r2, r2, r1          @ r2 = indice (total - N)",
                    "    lsl r2, r2, #3          @ Multiplica por 8 bytes (Double)",
                    "    ldr r0, =historico",
                    "    add r0, r0, r2          @ Endereco alvo",
                    "    vldr d0, [r0]           @ Carrega o resultado antigo",
                    "    vpush {d0}"
                ])

            # COMANDO MEM (variáveis)
            elif token.isupper() or (token.isalpha() and len(token) == 1):
                nome_var = f"var_{token}"
                if nome_var not in variaveis_criadas:
                    data_section.append(f"    {nome_var}: .double 0.0")
                    variaveis_criadas.add(nome_var)
                
                # se for o último token da linha -> salvar, se não -> é ler.
                if i == len(tokens) - 1 and len(tokens) > 1 and tokens[i-1] not in ['(', ')']:
                    text_section.extend([
                        f"    vpop {{d0}}               @ Pega valor para salvar",
                        f"    ldr r0, ={nome_var}",
                        f"    vstr d0, [r0]             @ Salva em {token}",
                        f"    vpush {{d0}}              @ Mantem na pilha"
                    ])
                else: 
                    text_section.extend([
                        f"    ldr r0, ={nome_var}",
                        f"    vldr d0, [r0]             @ Le de {token}",
                        f"    vpush {{d0}}"
                    ])

        # FIM DA LINHA: salva resultado no historico
        text_section.extend([
            "    @ --- Salva no historico e Exibe nos LEDs ---",
            "    vpop {d0}                   @ Pega resultado final",
            
            "    @ 1. Imprime o valor inteiro nos LEDs vermelhos (Hardware I/O)",
            "    vcvt.s32.f64 s0, d0         @ Converte D0 para inteiro de 32bits",
            "    vmov r4, s0                 @ Move para R4",
            "    ldr r5, =base_leds          @ Carrega endereco dos LEDs",
            "    ldr r5, [r5]                @ Desreferencia",
            "    str r4, [r5]                @ Liga os LEDs correspondentes ao numero binario",

            "    @ 2. Salva no array de historico",
            "    ldr r1, =contador_historico",
            "    ldr r2, [r1]                @ r2 = linha atual",
            "    mov r3, r2                  ",
            "    lsl r3, r3, #3              @ offset = linha * 8",
            "    ldr r0, =historico",
            "    add r0, r0, r3              ",
            "    vstr d0, [r0]               @ Salva",
            "    add r2, r2, #1              @ Incrementa linha",
            "    str r2, [r1]                "
        ])

    # encerra o programa com loop infinito
    text_section.extend([
        "\n    @ --- Fim do Programa ---",
        "_fim:",
        "    b _fim                      @ Loop infinito para segurar o processador"
    ])

    return '\n'.join(data_section) + '\n\n' + '\n'.join(text_section)


def lerArquivo(nomeArquivo):
    linhas_validas = []
    try:
        with open(nomeArquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:  # ignora linhas em branco
                    linhas_validas.append(linha)
        return linhas_validas
        
    except FileNotFoundError:
        print(f"ERRO FATAL: O arquivo de teste '{nomeArquivo}' não foi encontrado.")
        print("Verifique se o nome está correto e se ele está na mesma pasta do script.")
        return []
    except IOError as e:
        print(f"ERRO FATAL: Não foi possível ler o arquivo '{nomeArquivo}'. Detalhes: {e}")
        return []

# testes gerando txt com a ultima execução
def testarGerarAssembly():
    tokens = ["3.14", "2.0", "+", "RES", "5.0", "X", "MEM"]
    assembly = gerarAssembly(tokens)
    print(assembly)
    print('--- \n')
    with open("gerador_assembly/ultima_exec_gerarAssembly.txt", "w") as f:
        f.write(assembly)

def testarLerArquivo():
    nomeArquivo = "teste1.txt"
    linhas = lerArquivo(nomeArquivo)
    for linha in linhas:
        print(linha)
    with open("gerador_assembly/ultima_exec_lerArquivo.txt", "w") as f:
        for linha in linhas:
            f.write(linha + "\n")

if __name__ == "__main__":
    testarGerarAssembly()
    testarLerArquivo()