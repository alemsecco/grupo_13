# Alex Menegatti Secco @alemsecco
# Mariana de Castro @maricastroo
# Grupo 13


# Autômatos Finitos Determinísticos
def estadoInicial(linha, i):
    if i >= len(linha):
        return None # fim da linha, retorna None para indicar que não há mais tokens
    if linha[i].isspace():
        return estadoInicial # se for espaço, permanece no estado inicial para ignorar espaços
    if linha[i].isdigit() or linha[i] == '.':
        return estadoNumero
    if linha[i] in '+-*%^':
        return estadoOperador
    if linha[i] == '/':
        return estadoDivisao
    if linha[i] in '()':
        return estadoParenteses
    if linha[i].isalpha():
        return estadoComando
    return estadoErro

def estadoErro(linha, i): # falha via estado de erro explícito
    raise ValueError(f"Token inválido: {linha[i]}")

def estadoNumero(linha, i): # recebe a linha e o índice atual, extrai um número (inteiro ou real) e retorna o número e o novo índice
    num = linha[i]
    i += 1
    while i < len(linha) and (linha[i].isdigit() or linha[i] == '.'): # continua enquanto for dígito ou ponto decimal
        num += linha[i]
        i += 1
    if num.count('.') > 1: # verifica se o número tem mais de um ponto decimal -> malformado
        raise ValueError(f"Número malformado: {num}")
    return num, i, 0

def estadoOperador(linha, i): # recebe a linha e o índice atual, extrai um operador e retorna o operador e o novo índice
    return linha[i], i + 1, 0

def estadoParenteses(linha, i): # recebe a linha e o índice atual, extrai um parêntese e retorna o parêntese e o novo índice
    token = linha[i]
    delta = 1 if token == '(' else -1
    return token, i + 1, delta

def estadoComando(linha, i): # recebe a linha e o índice atual, extrai um comando/memória (RES ou nome de memória em maiúsculas) e retorna o comando e o novo índice
    cmd = linha[i]
    i += 1
    while i < len(linha) and linha[i].isupper():  # apenas maiúsculas para nomes de memória
        cmd += linha[i]
        i += 1
    if cmd == 'RES' or cmd.isupper():  # RES é keyword, outros devem ser maiúsculos
        return cmd, i, 0
    else:
        raise ValueError(f"Token inválido: {cmd} (nomes de memória devem ser maiúsculos)")
    
def estadoDivisao(linha, i): # recebe a linha e o índice atual, extrai um operador de divisão (/, //) e retorna o operador e o novo índice
    if linha[i] == '/':
        if i + 1 < len(linha) and linha[i + 1] == '/':
            return '//', i + 2, 0
        else:
            return '/', i + 1, 0
    raise ValueError(f"Token inválido: {linha[i]}")

# parseExpressão 
def parseExpressao(linha): # recebe uma linha de texto e retorna um vetor de tokens
    tokens = []
    i = 0
    parenteses = 0
    while True:
        estado = estadoInicial(linha, i)
        if estado is None:
            break
        if estado is estadoInicial:
            # linguagem MEF: espaço fica no estado inicial e avança o índice
            i += 1
            continue
        if estado is estadoErro:
            estado(linha, i)
        token, i, delta = estado(linha, i)
        parenteses += delta
        if parenteses < 0:
            raise ValueError("Parêntese fechado sem abertura correspondente")
        tokens.append(token)
    if parenteses != 0:
        raise ValueError("Parênteses não balanceados")
    return tokens

# testes + escrita de resultados em arquivo
def testeParseExpressao():
    log_lines = []
    try:
        # expressões válidas
        assert parseExpressao("(3.14 2 + (1 5 -) * )") == ['(', '3.14', '2', '+', '(', '1', '5', '-', ')', '*', ')']
        log_lines.append("EXPRESSÃO: (3.14 2 + (1 5 -) *)")
        log_lines.append("Teste expressão válida: OK")
        assert parseExpressao("RES MEM") == ['RES', 'MEM']
        log_lines.append("EXPRESSÃO: RES MEM")
        log_lines.append("Teste comandos RES/MEM: OK")
        # teste para nome de memória qualquer
        assert parseExpressao("RES VAR") == ['RES', 'VAR']
        log_lines.append("EXPRESSÃO: RES VAR")
        log_lines.append("Teste nome de memória qualquer: OK")
        # teste com minúscula deve falhar
        try:
            parseExpressao("res var")
            raise AssertionError("Esperava ValueError para minúsculas")
        except ValueError as e:
            assert "nomes de memória devem ser maiúsculos" in str(e)
            log_lines.append("EXPRESSÃO: res var")
            log_lines.append("Teste rejeição de minúsculas: OK")
        try:
            # teste para número malformado (mais de um ponto decimal)
            parseExpressao("3.14.5 2 +")
            raise AssertionError("Esperava ValueError para número malformado")
        except ValueError as e:
            assert str(e) == "Número malformado: 3.14.5"
            log_lines.append("EXPRESSÃO: 3.14.5 2 +")
            log_lines.append("Teste número malformado: OK")
        try:
            # teste para token inválido
            parseExpressao("3.14 @ +")
            raise AssertionError("Esperava ValueError para token inválido")
        except ValueError as e:
            assert str(e) == "Token inválido: @"
            log_lines.append("EXPRESSÃO: 3.14 @ +")
            log_lines.append("Teste token inválido: OK")
        # teste parenteses não balanceados
        try:            
            parseExpressao("((3 2 +) (1 5 -) +")
            raise AssertionError("Esperava ValueError para parênteses não balanceados")
        except ValueError as e:
            assert str(e) == "Parênteses não balanceados"
            log_lines.append("EXPRESSÃO: ((3 2 +) (1 5 -) +")
            log_lines.append("Teste parênteses não balanceados: OK")
        try:
            parseExpressao("3 2 +)")
            raise AssertionError("Esperava ValueError para parêntese extra fechado")
        except ValueError as e:
            assert "abertura correspondente" in str(e)
            log_lines.append("EXPRESSÃO: 3 2 +)")
            log_lines.append("Teste parêntese extra fechado: OK")
        resultado = "Todos os testes passaram!"
    except AssertionError as e:
        resultado = f"Falha nos testes: {e}"
        log_lines.append(resultado)
    except Exception as e:
        resultado = f"Erro inesperado nos testes: {e}"
        log_lines.append(resultado)

    with open("ultima_exec_teste_parseExpressao.txt", "w", encoding="utf-8") as f:
        for linha in log_lines:
            f.write(linha + "\n")
        f.write(resultado + "\n")

    print(resultado)
    return resultado
    
if __name__ == "__main__": 
    testeParseExpressao()
    




