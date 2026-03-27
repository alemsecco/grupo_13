def executar_expressao(tokens, memoria, historico):
    pilha = []

    for i, token in enumerate(tokens):

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

            if len(pilha) >= 1:
                n = int(pilha.pop())
                if n <= 0 or n > len(historico):
                    raise ValueError("Erro! Índice inválido")
                pilha.append(historico[-n])
            else:
                pilha.append(historico[-1])

            continue

        # variável
        elif token.isalpha() and len(token) == 1:
            if i + 1 < len(tokens) and tokens[i + 1] == "MEM":
                continue

            if token not in memoria:
                raise ValueError(f"Erro! Variável '{token}' não definida")

            pilha.append(memoria[token])
            continue

        else:
            raise ValueError(f"Token inválido: {token}")

    if len(pilha) == 1:
        resultado = pilha[0]

        # histórico não poluído por comandos de memória ou consulta
        if "MEM" not in tokens and "RES" not in tokens:
            historico.append(resultado)

        return resultado

    elif len(pilha) == 0:
        return None

    else:
        raise ValueError("Erro! Expressão inválida")


def parenteses_aninhados(tokens):
    saida = []
    operadores = []

    precedencia = {
        '+': 1, '-': 1,
        '*': 2, '/': 2, '//': 2, '%': 2, '^': 3
    }

    for token in tokens:
        if token.lstrip('-').replace('.', '', 1).isdigit() or (token.isalpha() and len(token) == 1):
            saida.append(token)

        elif token in precedencia:
            while (operadores and operadores[-1] != "(" and
                   precedencia.get(operadores[-1], 0) >= precedencia[token]):
                saida.append(operadores.pop())

            operadores.append(token)

        elif token == "(":
            operadores.append(token)

        elif token == ")":
            while operadores and operadores[-1] != "(":
                saida.append(operadores.pop())

            if not operadores:
                raise ValueError("Erro! Parênteses desbalanceados")

            operadores.pop()

    while operadores:
        if operadores[-1] == "(":
            raise ValueError("Erro! Parênteses desbalanceados")
        saida.append(operadores.pop())

    return saida


def rodar_testes_e_salvar():
    log = []

    try:
        memoria = {}
        historico = []

        # (3.14 2.0 +) round para evitar erro de precisão float
        res1 = executar_expressao(["3.14", "2.0", "+"], memoria, historico)
        assert round(res1, 2) == 5.14
        log.append("3.14 2.0 + = 5.14 OK")

        # (3.14.5 2.0 +) ERRO
        try:
            executar_expressao(["3.14.5", "2.0", "+"], memoria, historico)
            log.append("Erro: 3.14.5 deveria ter falhado")
        except ValueError:
            log.append("3.14.5 2.0 + (inválido) OK")

        # MEM e variáveis
        executar_expressao(["10", "X", "MEM"], memoria, historico)
        assert executar_expressao(["X"], memoria, historico) == 10
        log.append("MEM X = 10 OK")

        # Histórico (N RES)
        historico.clear()
        executar_expressao(["4", "5", "+"], memoria, historico) # hist: [9.0]
        executar_expressao(["2", "5", "-"], memoria, historico) # hist: [9.0, -3.0]

        res_res1 = executar_expressao(["1", "RES"], memoria, historico)
        assert res_res1 == -3
        log.append("1 RES = -3 OK")

        res_res2 = executar_expressao(["2", "RES"], memoria, historico)
        assert res_res2 == 9
        log.append("2 RES = 9 OK")

        # parênteses aninhados
        rpn = parenteses_aninhados(["(", "2", "+", "3", ")", "*", "4"])
        assert executar_expressao(rpn, memoria, historico) == 20
        log.append("(2+3)*4 = 20 OK")

        resultado_final = "Todos os testes passaram!"

    except Exception as e:
        # no caso de erro, logamos o tipo exato do erro para ajudar no debug
        import traceback
        resultado_final = f"Erro: {traceback.format_exc()}"
        log.append("Ocorreu um erro durante a execução.")

    with open("resultado_testes.txt", "w", encoding="utf-8") as f:
        for linha in log:
            f.write(linha + "\n")
        f.write(resultado_final)

    print(resultado_final)


if __name__ == "__main__":
    rodar_testes_e_salvar()
