# Analisador Léxico
Alex Menegatti Secco ([@alemsecco](https://github.com/alemsecco))

Mariana de Castro ([@maricastroo](https://github.com/maricastroo))

Este projeto foi elaborado para a disciplina de Construção de Interpretadores do curso de Bacharelado de Ciência da Computação na PUCPR, ministrada pelo professor Frank Coelho de Alcantara. O projeto é a primeira fase da construção de um compilador.

O objetivo do trabalho é construir um analisador léxico para processar expressões aritméticas em notação polonesa reversa (RPN) a partir de um arquivo .txt e utilizar máquinas de estado finito implementadas com funções para tal. Esse analisador irá gerar um código Assembly a partir dos tokens, compatível com a arquitetura ARMv7 DEC1-SOC(v16.1), representando o programa de testes.

O projeto possui essencialmente quatro partes.

## Parte 1 - parseExpressao e Analisador Léxico com Autômato Finito Determinístico
1. Implementação do analisador léxico usando Autômatos Finitos Determinísticos (AFDs), com cada estado como uma função (estadoNumero, estadoOperador, estadoParenteses, etc.). 
2. Implementação de uma função parseExpressao(linha) que analisa uma linha de uma expressão RPN e extrai os tokens. Essa função divide a linha em tokens utilizando AFDs.
3. Validação de tokens:
    - Números reais, usando ponto como separador decimal;
    - Operadores (+, -, *, /, %, ^);
    - Comandos especiais (RES, MEM) e parênteses;
4. Detecção de erros (números malformados, tokens inválidos).
5. Implementação de funções de teste para o analisador léxico, cobrindo entradas válidas e inválidas.

Interface:
- Recebe uma linha de texto e retorna um vetor de tokens;
- Fornece tokens válidos para executarExpressao. 

## Parte 2 - executarExpressao e Gerenciamento de Memória
1. Teste dos AFDs com várias entradas.
2. Implementação da função executarExpressao(tokens, memoria, historico) mapeando e gerenciando múltiplas variáveis na memória, além de lidar com parênteses.
3. Gerenciamento da memória MEM para comandos (V MEM) e (MEM).
4. Manutenção de histórico de resultados que suportam (N RES).
5. Criação de funções de teste validando a execução de expressões e comandos especiais:
    - Uso de pilha para avaliar expressões RPN;
    - Operações com precisão de 64 bits;
    - Divisão inteira e resto tratados separadamente.

Interface:
- Recebe tokens de parseExpressao e atualiza resultados e memória;
- Fornece resultados para exibirResultados e Assembly.

## Parte 3 - gerarAssembly e Leitura de Arquivo
1. Teste de expressões RPN.
2. Implementação da função gerarAssembly(todas_linhas_rpn), que recebe o vetor de tokens gerado pelo analisador léxico e traduz para Assembly ARMv7, processando expressões puramente na FPU (Double 64-bits).
3. Implementação de comunicação de I/O em hardware (MMIO), convertendo o resultado final de cada linha e mapeando-o para acender os LEDs Vermelhos (LEDR) da placa DE1-SoC no endereço 0xFF200000.
4. Implementação da função lerArquivo(nomeArquivo) que lê o arquivo de entrada.
5. Criação de funções de teste para validar as outras funções implementadas:
    - Testes com arquivos contendo 10 linhas, incluindo expressões aninhadas e comandos especiais;
    - Verificação de erros de abertura de arquivo, exibindo mensagens claras.

Interface:
- lerArquivo fornece linhas para parseExpressao;
- gerarAssembly produz código Assembly.

## Parte 4 - exibirResultados, Interface do Usuário e Testes
1. Implementação da função exibirResultados(), que exibe os resultados das expressões de forma clara.
2. Implementação e gerenciamento da interface do main, chamando as funções lerArquivo, parseExpressao, executarExpressao, e exibirResultados e fazendo a leitura de argumento na linha de comando.
3. Correção de eventuais problemas de entrada e criação de funções de teste para validar a saída e o comportamento do programa.
4. Teste utilizando arquivos fornecidos, verificando saídas para expressões simples e complexas;
5. Teste da MEF com comandos especiais.

Interface:
- Usa resultados de executarExpressao para exibir saídas;
- Gerencia a execução do programa via argumento de linha de comando.

## Instruções para compilação, execução e teste
### Pré-requisitos

Para rodar e testar este projeto, você precisará de:
1. Python 3.12  ou superior (para executar o compilador).
2. Acesso à internet para utilizar o simulador **[CPULator](https://cpulator.01xz.net/?sys=arm-de1soc)** (para executar o código Assembly gerado).

### Estrutura dos Arquivos

* `main.py`: O orquestrador central do projeto.
* `teste1.txt`, `teste2.txt`, `teste3.txt`: Arquivos contendo as expressões RPN de teste.
* `saida_arm.s`: Arquivo Assembly gerado automaticamente após a compilação.
* `analisador_lexico`: Pasta contendo o analisador léxico e AFDs, juntamente ao teste individual da função.
* `gerador_assembly`: Pasta contendo o gerador de código Assembly e o leitor de arquivo, juntamente aos testes individuais das funções.
* `execucao`: Pasta contendo a execução das expressões que fornece resultados para exibir saídas e a função que lida com parênteses aninhados, juntamente ao teste individual da função de execução.

### Como Compilar (Gerar o Assembly)

1. Clone este repositório para a sua máquina.
2. Abra o terminal na pasta onde os arquivos estão localizados.
3. Execute o compilador passando os argumentos na linha de comando (main.py e caminho do arquivo de teste). Exemplo de comando:
    ```bash
   python main.py teste1.txt
    ```
4. O console exibirá a leitura dos tokens e o interpretador de prova real, além de exibir os resultados das expressões.
5. Se não houver erros de sintaxe no arquivo de texto, o compilador criará (ou sobrescreverá) um arquivo chamado saida_arm.s na mesma pasta.

### Como Executar e Testar (No CPULator)
Com o arquivo saida_arm.s gerado, siga estes passos para testar o código no hardware simulado:
1. Acesse o CPULator e certifique-se de que a arquitetura selecionada é ARMv7 DEC1-SoC.
2. Abra o arquivo saida_arm.s em um editor de texto, copie todo o seu conteúdo e cole na área de edição principal do CPULator (exclua o que estiver na tela antes de colar).
3. Pressione o botão F5 ou clique em "Compile and Load".
4. Se a compilação for bem-sucedida, clique no botão "Run" (F3) ou execute passo a passo usando "Step Into" (F2).
5. Ao final da execução de cada linha, o resultado ficará salvo no topo da pilha de memória.
6. Visualização do Resultado: Ao final da execução de cada linha matemática, o valor inteiro do resultado será exibido visualmente através dos LEDs Vermelhos (LEDR) na interface da placa do simulador.
7. Para uma análise profunda de depuração, também é possível consultar as variáveis salvas na RAM (ex: var_MEM, var_A) e o array de histórico acessando a aba Memory no painel lateral e procurando pela secção .data.

Copyright © 2026 Alex Menegatti Secco e Mariana de Castro