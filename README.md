# Analisador Léxico

Este projeto foi elaborado para a disciplina de Construção de Interpretadores do curso de Bacharelado de Ciência da Computação na PUCPR.

O objetivo do trabalho é construir um analisador léxico para processar expressões aritméticas em notação polonesa reversa (RPN) a partir de um arquivo .txt e utilizar máquinas de estado finito implementadas com funções para tal. Esse analisador irá gerar um código Assembly a partir dos tokens, compatível com a arquitetura ARMv7 DEC1-SOC(v16.1), representando o programa de testes.

O projeto possui essencialmente quatro partes.

## Parte 1 - parseExpressao()
1. Implementação do analisador léxico usando Autômatos Finitos Determinísticos (AFDs), com cada estado como uma função (estadoNumero, estadoOperador, estadoParenteses, etc.). 
2. Implementação de uma função parseExpressao() que analisa uma linha de uma expressão RPN e extrai os tokens. Essa função divide a linha em tokens utilizando AFDs.
3. Validação de tokens:
- Números reais, usando ponto como separador decimal;
- Operadores (+, -, *, /, %, ^);
- Comandos especiais (RES, MEM) e parênteses;
4. Detecção de erros (números malformados, tokens inválidos)
5. Implementação de funções de teste para o analisador léxico, cobrindo entradas válidas e inválidas

Interface:
- Recebe uma linha de texto e retorna um vetor de tokens;
- Fornece tokens válidos para executarExpressao. 

## Parte 2 - executarExpressao()

Copyright © 2026 Alex Menegatti Secco e Mariana de Castro