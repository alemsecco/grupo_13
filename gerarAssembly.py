def gerarAssembly(todas_linhas_rpn):
    # Seção de Dados (Memória RAM)
    data_section = [
        ".data",
        "    @ --- Variaveis e Constantes ---",
        "    contador_historico: .word 0        @ Guarda quantas linhas ja rodaram",
        "    historico: .space 400              @ Espaco para 100 resultados"
    ]
    
    # Seção de Texto
    text_section = [
        ".text",
        ".global _start",
        "_start:"
    ]
    
    contador_numeros = 0
    contador_loops = 0  # criar nomes de loops únicos para a potência
    variaveis_criadas = set()
    
    # Operações básicas suportadas nativamente
    mapa_instrucoes = {'+': 'vadd.f64', '-': 'vsub.f64', '*': 'vmul.f64', '/': 'vdiv.f64'}

    for numero_linha, tokens in enumerate(todas_linhas_rpn, start=0):
        text_section.append(f"\n    @ --- Linha {numero_linha + 1} ---")
        
        for i, token in enumerate(tokens):
            if token in ['(', ')']: 
                continue

            # 1. NÚMERO
            if token.lstrip('-').replace('.', '', 1).isdigit():
                nome_const = f"num_{contador_numeros}"
                data_section.append(f"    {nome_const}: .double {token}")
                
                text_section.append(f"    ldr r0, ={nome_const}")
                text_section.append(f"    vldr s0, [r0]")
                text_section.append(f"    vpush {{s0}}")
                contador_numeros += 1

            # 2. OPERAÇÕES BÁSICAS (+, -, *, /)
            elif token in mapa_instrucoes:
                inst = mapa_instrucoes[token]
                text_section.extend([
                    f"    vpop {{s1}}               @ Tira B",
                    f"    vpop {{s0}}               @ Tira A",
                    f"    {inst} s2, s0, s1      @ Calcula S2 = A op B",
                    f"    vpush {{s2}}              @ Devolve pra pilha"
                ])

            # 3. DIVISÃO INTEIRA (//)
            elif token == '//':
                text_section.extend([
                    "    @ --- Divisao Inteira (//) ---",
                    "    vpop {s1}               @ B",
                    "    vpop {s0}               @ A",
                    "    vdiv.f32 s2, s0, s1     @ A / B",
                    "    vcvt.s32.f32 s2, s2     @ Int(A / B)",
                    "    vcvt.f32.s32 s2, s2     @ Volta pra Float",
                    "    vpush {s2}"
                ])

            # 4. RESTO DA DIVISÃO (%)
            elif token == '%':
                text_section.extend([
                    "    @ --- Resto (%) ---",
                    "    vpop {s1}               @ B",
                    "    vpop {s0}               @ A",
                    "    vdiv.f32 s2, s0, s1     @ A / B",
                    "    vcvt.s32.f32 s2, s2     @ Int(A / B)",
                    "    vcvt.f32.s32 s2, s2     @ Float(Int(A / B))",
                    "    vmul.f32 s2, s2, s1     @ (Int(A / B) * B)",
                    "    vsub.f32 s2, s0, s2     @ A - (Int(A / B) * B)",
                    "    vpush {s2}"
                ])

            # 5. POTENCIAÇÃO (^)
            elif token == '^':
                loop_id = contador_loops
                contador_loops += 1
                text_section.extend([
                    "    @ --- Potenciacao (^) ---",
                    "    vpop {s1}               @ B (Expoente)",
                    "    vpop {s0}               @ A (Base)",
                    "    vcvt.s32.f32 s1, s1     @ Converte expoente pra inteiro",
                    "    vmov r1, s1             @ r1 = contador do loop",
                    "    vmov.f32 s2, #1.0       @ s2 = resultado inicia em 1.0",
                    f"loop_pot_inicio_{loop_id}:",
                    "    cmp r1, #0              @ B chegou a 0?",
                    f"    ble loop_pot_fim_{loop_id} @ Se sim, sai do loop",
                    "    vmul.f32 s2, s2, s0     @ resultado = resultado * base",
                    "    sub r1, r1, #1          @ diminui o contador B",
                    f"    b loop_pot_inicio_{loop_id} @ volta pro inicio",
                    f"loop_pot_fim_{loop_id}:",
                    "    vpush {s2}              @ Guarda o resultado"
                ])

            # 6. COMANDO RES (Histórico)
            elif token == "RES":
                text_section.extend([
                    "    @ --- Comando RES ---",
                    "    vpop {s0}               @ Pega o 'N' (em float)",
                    "    vcvt.s32.f32 s0, s0     @ Converte N pra inteiro",
                    "    vmov r1, s0             @ Move N para r1",
                    "    ldr r2, =contador_historico",
                    "    ldr r2, [r2]            @ r2 = linhas executadas",
                    "    sub r2, r2, r1          @ r2 = indice (total - N)",
                    "    lsl r2, r2, #2          @ Multiplica por 4 bytes",
                    "    ldr r0, =historico",
                    "    add r0, r0, r2          @ Endereco alvo",
                    "    vldr s0, [r0]           @ Carrega o resultado antigo",
                    "    vpush {s0}"
                ])

            # 7. COMANDO MEM (Variáveis)
            elif token.isupper() or (token.isalpha() and len(token) == 1):
                nome_var = f"var_{token}"
                if nome_var not in variaveis_criadas:
                    data_section.append(f"    {nome_var}: .float 0.0")
                    variaveis_criadas.add(nome_var)
                
                # Se for o último token da linha, é salvar. Se não, é ler.
                if i == len(tokens) - 1 and len(tokens) > 1 and tokens[i-1] not in ['(', ')']:
                    text_section.extend([
                        f"    vpop {{s0}}               @ Pega valor para salvar",
                        f"    ldr r0, ={nome_var}",
                        f"    vstr s0, [r0]             @ Salva em {token}",
                        f"    vpush {{s0}}              @ Mantem na pilha"
                    ])
                else: 
                    text_section.extend([
                        f"    ldr r0, ={nome_var}",
                        f"    vldr s0, [r0]             @ Le de {token}",
                        f"    vpush {{s0}}"
                    ])

        # --- FIM DA LINHA: Salva resultado no historico ---
        text_section.extend([
            "    @ --- Salva no historico ---",
            "    vpop {s0}                   @ Pega resultado final",
            "    ldr r1, =contador_historico",
            "    ldr r2, [r1]                @ r2 = linha atual",
            "    mov r3, r2                  ",
            "    lsl r3, r3, #2              @ offset = linha * 4",
            "    ldr r0, =historico",
            "    add r0, r0, r3              ",
            "    vstr s0, [r0]               @ Salva!",
            "    add r2, r2, #1              @ Incrementa linha",
            "    str r2, [r1]                "
        ])

    # Encerra o programa
    text_section.extend([
        "\n    @ --- Fim do Programa ---",
        "    mov r7, #1                  @ Syscall exit",
        "    svc #0"
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

# testes
def testarGerarAssembly():
    tokens = ["3.14", "2.0", "+", "RES", "5.0", "MEM"]
    assembly = gerarAssembly(tokens)
    print(assembly)
    print('--- \n')

def testarLerArquivo():
    nomeArquivo = "teste.txt"
    linhas = lerArquivo(nomeArquivo)
    for linha in linhas:
        print(linha)

if __name__ == "__main__":
    testarGerarAssembly()
    testarLerArquivo()