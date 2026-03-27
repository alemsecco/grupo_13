def executar_expressao(tokens):
    pilha = []

    # pilha RPN para simular a execução da expressão
    for token in tokens:
        try:
            # converter para número 
            valor = float(token)
            pilha.append(valor)

        except ValueError:
            # tratamento de erros para operadores, pois precisam ter 2 valores
            if token in ['+', '-', '*', '/', '//', '%', '^']:
                if len(pilha) < 2:
                    raise ValueError(f"Erro! o operador '{token}' necessita de 2 valores para ser executado")

                # ultimo que entra é o primeiro a sair
                b = pilha.pop() # ultimo 
                a = pilha.pop() # anterior 
                
                if token == "+":
                    pilha.append(a + b) # entrada 5 3 + -> empilhando (5) -> 5 (3) -> 5,3. Operador + desempilha ou seja, b= pilha.pop remove o ultimo (3)e remove o prox (5) e o append calcula e coloca novamente.

                elif token == "-":
                    pilha.append(a - b)
            
                elif token == "*":
                    pilha.append(a * b)

                elif token == "/":
                    if b == 0:
                        raise ZeroDivisionError("Erro! Não é permitida divisão por zero.")
                    pilha.append(a / b)

                elif token == "//":
                    if b == 0:
                        raise ZeroDivisionError("Erro! Não é permitida divisão por zero.")
                    pilha.append(a // b)

                elif token == "%":
                    if b == 0:
                        raise ZeroDivisionError("Erro! Não é permitida divisão por zero.")
                    pilha.append(a % b)

                elif token == "^":
                    pilha.append(a ** b)

            else:
                raise ValueError(f"Token inválido: {token}")

    # deve terminar com um valor na pilha
    if len(pilha) != 1:
        raise ValueError("Erro! A expressão é inválida, verifique se os operadores e valores estão corretos.")
    
    return pilha[0]


# testes
def testar():
    testes = [
        ["3.14", "2.0", "+"],
        ["2.14.5", "2.0", "+"], # token inválido
        ["7", "3", "4", "*", "+"], # 7 + (3 * 4) = 19
        ["10", "0", "/"],
    ]

    for tokens in testes:
        try:
            resultado = executar_expressao(tokens)
            print(f"{tokens} → {resultado}")
        except Exception as e:
            print(f"{tokens} → ERRO: {e}")

testar()