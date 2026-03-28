# Alex Menegatti Secco @alemsecco
# Mariana de Castro @maricastroo
# Grupo 13

def executarExpressao(tokens, memoria, historico):
    pilha = []

    for i, token in enumerate(tokens):
        if token in ['(', ')']:
            continue

        # número 
        if token.lstrip('-').replace('.', '', 1).isdigit():
            pilha.append(float(token))
            continue

        # operadores
        if token in ['+', '-', '*', '/', '//', '%', '^']:
            if len(pilha) < 2:
                raise ValueError(f"Erro! operador '{token}' precisa de 2 valores")
            
            b = pilha.pop()
            a = pilha.pop()

            if token == "+":
                pilha.append(a + b)
            elif token == "-":
                pilha.append(a - b)
            elif token == "*":
                pilha.append(a * b)
            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("Erro! divisão por zero")
                pilha.append(a / b)
            elif token == "//":
                if b == 0:
                    raise ZeroDivisionError("Erro! divisão por zero")
                pilha.append(a // b)
            elif token == "%":
                if b == 0:
                    raise ZeroDivisionError("Erro! divisão por zero")
                pilha.append(a % b)
            elif token == "^":
                pilha.append(a ** b)

            continue

        # MEM
        elif token == "MEM":
            if len(pilha) < 1 or i == 0:
                raise ValueError("Erro! MEM mal formado")

            nome = tokens[i - 1]

            # aceita qualquer palavra maiuscula
            if not nome.isupper():
                raise ValueError("Erro! Nome inválido")

            valor = pilha.pop()
            memoria[nome] = valor
            pilha.append(valor)  
            continue

        # RES
        elif token == "RES":
            if not historico:
                raise ValueError("Erro! Não há histórico")

            if len(pilha) < 1:
                raise ValueError("Erro! RES precisa de um númer N anterior")
            
            n = int(pilha.pop())
            if n <= 0 or n > len(historico):
                raise ValueError("Erro! Índice inválido")
                
            pilha.append(historico[-n])
            continue

        # variável
        elif token.isupper() or (token.isalpha() and len(token) == 1):

            if i + 1 < len(tokens) and tokens[i + 1] == "MEM":
                continue

            if i ==  len(tokens) - 1 and len(pilha) >= 1:
                valor = pilha.pop()
                memoria[token] = valor
                pilha.append(valor)

            else:
                if token not in memoria:
                    pilha.append(0.0)
                else:
                    pilha.append(memoria[token])
            continue

        raise ValueError(f"Token inválido: {token}")

    if len(pilha) == 1:
        resultado = pilha[0]

        if "MEM" not in tokens and "RES" not in tokens:
            historico.append(resultado)
        elif len(tokens) > 2: # se teve cálculo antes de chamar MEM ou RES, salva o resultado
            historico.append(resultado)
        return resultado

    elif len(pilha) == 0:
        return None

    else:
        raise ValueError("Erro! Expressão inválida, sobram valores perdidos na pilha")


def rodar_testes_e_salvar():
    log = []

    try:
        memoria = {}
        historico = []

        # (3.14 2.0 +) round para evitar erro de precisão float
        res1 = executarExpressao(["3.14", "2.0", "+"], memoria, historico)
        assert round(res1, 2) == 5.14
        log.append("3.14 2.0 + = 5.14 OK")

        # (3.14.5 2.0 +) ERRO
        try:
            executarExpressao(["3.14.5", "2.0", "+"], memoria, historico)
            log.append("Erro: 3.14.5 deveria ter falhado")
        except ValueError:
            log.append("3.14.5 2.0 + (inválido) OK")

        # MEM e variáveis
        executarExpressao(["10", "X", "MEM"], memoria, historico)
        assert executarExpressao(["X"], memoria, historico) == 10
        log.append("MEM X = 10 OK")

        # Histórico (N RES)
        historico.clear()
        executarExpressao(["4", "5", "+"], memoria, historico) # hist: [9.0]
        executarExpressao(["2", "5", "-"], memoria, historico) # hist: [9.0, -3.0]

        res_res1 = executarExpressao(["1", "RES"], memoria, historico)
        assert res_res1 == -3
        log.append("1 RES = -3 OK")

        res_res2 = executarExpressao(["2", "RES"], memoria, historico)
        assert res_res2 == 9
        log.append("2 RES = 9 OK")

        # expressão com parênteses
        historico.clear()
        rpn = ["2", "3", "+", "4", "*"] # equivalente a (2 + 3) * 4
        assert executarExpressao(rpn, memoria, historico) == 20
        log.append("(2+3)*4 = 20 OK")

        # divisão inteira
        res7 = executarExpressao(["10", "3", "//"], memoria, historico)
        assert res7 == 3.0
        log.append("10 3 // = 3 OK")

        # resto de divisao
        res8 = executarExpressao(["10", "3", "%"], memoria, historico)
        assert res8 == 1.0
        log.append("10 3 % = 1 OK")

        # potenciacao
        res9 = executarExpressao(["2", "3", "^"], memoria, historico)
        assert res9 == 8.0
        log.append("2 3 ^ = 8 OK")

        # longa
        executarExpressao(["100", "VARIAVEL", "MEM"], memoria, historico)
        assert memoria.get("VARIAVEL") == 100.0
        log.append("100 VARIAVEL MEM = 100 OK")

        resultado_final = "Todos os testes passaram!"

    except Exception as e:
        # no caso de erro, logamos o tipo exato do erro para ajudar no debug
        import traceback
        resultado_final = f"Erro: {traceback.format_exc()}"
        log.append("Ocorreu um erro durante a execução.")

    with open("execucao/ultimo_teste_executarExpressao.txt", "w", encoding="utf-8") as f:
        for linha in log:
            f.write(linha + "\n")
        f.write(resultado_final)

    print(resultado_final)


if __name__ == "__main__":
    rodar_testes_e_salvar()
