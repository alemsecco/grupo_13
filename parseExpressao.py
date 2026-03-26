# Alex Menegatti Secco @alemsecco
# Mariana de Castro @maricastroo
# Grupo 13

"""
Implementar parseExpressao(std::string linha, std::vector<std::string>& _tokens_) (ou equivalente em Python/C) para analisar uma linha de expressão RPN e extrair tokens.

Implementar o analisador léxico usando Autômatos Finitos Determinísticos (AFDs), com cada estado como uma função (ex.: estadoNumero, estadoOperador, estadoParenteses).

Validar tokens:

Números reais (ex.: 3.14) usando ponto como separador decimal;
Operadores (+, -, *, /, %, ^);
Comandos especiais (RES, MEM) e parênteses;
Detectar erros como números malformados (ex.: 3.14.5) ou tokens inválidos;
Criar funções de teste para o analisador léxico, cobrindo entradas válidas e inválidas
Tarefas Específicas:

Escrever parseExpressao para dividir a linha em tokens usando um Autômato Finito Determinístico;
Interface:

Recebe uma linha de texto e retorna um vetor de tokens;
Fornece tokens válidos para executarExpressao. 
A palavra parser usada neste texto deve ser interpretada em seu sentido mais amplo: percorrer, varrer, um texto ou uma coleção de dados. Neste caso, refere-se o processo de análise léxica. O uso de expressões regulares, ou das bibliotecas de expressões regulares disponíveis em Python, C ou C++, para a implementação do analisador léxico, é proibido e resultará no zeramento do trabalho.
"""

def estadoNumero(linha, i):
    num = linha[i]
    i += 1
    while i < len(linha) and (linha[i].isdigit() or linha[i] == '.'):
        num += linha[i]
        i += 1
    if num.count('.') > 1:
        raise ValueError(f"Número malformado: {num}")
    return num, i

def estadoOperador(linha, i):
    return linha[i], i + 1 

def estadoParenteses(linha, i):
    return linha[i], i + 1

def estadoComando(linha, i):
    cmd = linha[i]
    i += 1
    while i < len(linha) and linha[i].isalpha():
        cmd += linha[i]
        i += 1
    if cmd in ['RES', 'MEM']:
        return cmd, i
    else:
        raise ValueError(f"Token inválido: {cmd}")

def parseExpressao(linha):
    tokens = []
    i = 0
    while i < len(linha):
        if linha[i].isspace():
            i += 1
            continue
        elif linha[i].isdigit() or linha[i] == '.':
            token, i = estadoNumero(linha, i)
            tokens.append(token)
        elif linha[i] in '+-*/%^':
            token, i = estadoOperador(linha, i)
            tokens.append(token)
        elif linha[i] in '()':
            token, i = estadoParenteses(linha, i)
            tokens.append(token)
        elif linha[i].isalpha():
            token, i = estadoComando(linha, i)
            tokens.append(token)
        else:
            raise ValueError(f"Token inválido: {linha[i]}")
    return tokens

# Testes
def testeParseExpressao():
    assert parseExpressao("3.14 + 2 * (1 - 5)") == ['3.14', '+', '2', '*', '(', '1', '-', '5', ')']
    assert parseExpressao("RES MEM") == ['RES', 'MEM']
    try:
        parseExpressao("3.14.5 + 2")
    except ValueError as e:
        assert str(e) == "Número malformado: 3.14.5"
    try:        parseExpressao("3.14 + @")
    except ValueError as e:
        assert str(e) == "Token inválido: @"
    print("Todos os testes passaram!")
    
if __name__ == "__main__": 
    testeParseExpressao()



