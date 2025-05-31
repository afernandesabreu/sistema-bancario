import os

# VARIAVEIS
# Variáveis relacionadas às operações bancárias
saldo = 0.00
limite = 500.00
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

# Variáveis de menu
menu = """
Escolha uma Opção:
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair 

> """

menu2 = """
Você já é cliente de nossa instituição?
Escolha uma opção:
[s] Sim
[n] Não
[q] Sair

> """

# Variáveis relacionadas ao cliente
cliente_nome, cliente_data_nascimento, cliente_cpf, cliente_endereco = "", "", "", ""
lista_cliente = []
dicionario_cliente_contas = {}

# Variáveis relacionadas à conta bancária
numero_agencia = "0001"
numero_conta = "" # Deve ser sequencial começando em 1.
cliente_conta = "" 
lista_conta_corrente = []


# DEFINIÇÃO DE FUNÇÕES
def cadastrar_cliente() -> tuple[str, str, str, str]:
    limpar_tela()
    nome = input('Nome Completo: ')
    nascimento = input('Data de Nascimento (dd/mm/aaaa): ')
    cpf = input('CPF (apenas números, sem pontos): ')
    endereco = input('Endereço: ')
    print('Cliente cadastrado com sucesso.')
    return nome, nascimento, cpf, endereco

def conferir_existencia_cliente(cpf: str, dicionario: dict) -> bool:
    cpf = input('Por favor, informe o número de seu CPF (sem pontos): ')
    if cpf in dicionario:
        return True

def decisao_abrir_conta() -> bool:
    while True:
        limpar_tela()
        decisao = input('Gostaria de abrir uma conta bancária em nossa instituição? (s/n)\n> ').lower()
        if decisao == 's':
            return True
        elif decisao == 'n':
            limpar_tela()
            print('Obrigado por acessar nosso sistema.\nO Banco Python está sempre de portas abertas.')
            return False
        else:
            print('Opção inválida.')

def decisao_novo_cliente() -> bool:
    while True:
        limpar_tela()
        print('Parabéns! Seu cadastro foi realizado com sucesso.')
        decisao = input('Gostaria de realizar uma operação bancária neste momento? (s/n)\n> ').lower()
        if decisao == 's':
            return True
        elif decisao == 'n':
            limpar_tela()
            print('Obrigado por acessar nosso sistema.\nO Banco Python está sempre de portas abertas.')
            return False
        else:
            print('Opção inválida.')

def gerenciar_operacao_bancaria(saldo: float, extrato: str, numero_saques: int) -> None:
    while True:
        limpar_tela()
        opcao = input(menu).lower()
        if opcao == 'd':
            limpar_tela()
            print('Depósito')
            valor_depositado = obter_valor_valido('Por favor, informe o valor da operação: R$ ')
            saldo = processar_deposito(saldo, valor_depositado)
            extrato += f"Depósito: R$ {valor_depositado:>7.2f}\n"
            gerar_extrato(saldo, extrato, numero_saques, LIMITE_SAQUES)

        elif opcao == 's':
            limpar_tela()
            print('Saque')
            valor_a_ser_sacado = obter_valor_valido('Por favor, informe o valor para operação: R$ ')
            saldo_anterior = saldo
            saldo, numero_saques = processar_saque(valor_a_ser_sacado, saldo, numero_saques, LIMITE_SAQUES, limite)
            if saldo < saldo_anterior:
                extrato += f"Saque:    R$ {valor_a_ser_sacado:>7.2f}\n"
            gerar_extrato(saldo, extrato, numero_saques, LIMITE_SAQUES)

        elif opcao == 'e':
            limpar_tela()
            print('Extrato')
            gerar_extrato(saldo, extrato, numero_saques, LIMITE_SAQUES)

        elif opcao == 'q':
            limpar_tela()
            print('Saindo do Sistema')
            break
        else:
            print('Operação Inválida, por favor, selecione novamente a operação desejada.')

def gerar_extrato(saldo_atual: float, historico_transacoes: str, num_saques_feitos: int, limite_total_saques: int) -> None:
    saques_restantes = limite_total_saques - num_saques_feitos
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXTRATO BANCÁRIO<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    if not historico_transacoes:
        print("\nNão foram realizadas movimentações.")
    else:
        print("\nHistórico de Transações:")
        print(historico_transacoes.strip())

    print(f"\nSeu saldo é de: R$ {saldo_atual:.2f}")
    print(f"Você ainda pode realizar {saques_restantes} operação(ões) de saque hoje.")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXTRATO BANCÁRIO<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def obter_valor_valido(prompt: str) -> float:
    while True:
        limpar_tela()
        valor_string = input(prompt)
        try:
            valor_float = float(valor_string)
            if valor_float > 0:
                return valor_float
            else:
                print('O valor informado não pode ser igual ou menor que 0.')
        except ValueError:
            print('Valor inválido. Por favor, informe um valor númérico.')

def processar_deposito(saldo_atual: float, valor_depositado: float) -> float:
    novo_saldo = saldo_atual + valor_depositado
    print('Depósito realizado com sucesso')
    return novo_saldo

def processar_quantidade_saque(numero_saques_realizados: int) -> int:
        numero_saques_realizados += 1
        return numero_saques_realizados
    
def processar_saque(valor_sacado: float,
                    saldo_atual: float,
                    numero_saques_feitos: int,
                    limite_num_saques: int,
                    limite_valor_saque: float) -> tuple[float, int]:
    if not verifica_quantidade_saque(numero_saques_feitos, limite_num_saques):
        return saldo_atual, numero_saques_feitos
    if not verifica_limite_saque(valor_sacado, limite_valor_saque):
        return saldo_atual, numero_saques_feitos
    if valor_sacado > saldo_atual:
        print(f'A operação falhou. Saldo insuficiente. Saldo atual: R${saldo_atual:.2f}')
        return saldo_atual, numero_saques_feitos
    
    saldo_atual -= valor_sacado
    numero_saques_feitos = processar_quantidade_saque(numero_saques_feitos)
    print('Saque realizado com sucesso.')
    return saldo_atual, numero_saques_feitos

def verifica_quantidade_saque(numero_saques_realizados: int, numero_saques_possiveis: int) -> bool:
    if numero_saques_realizados < numero_saques_possiveis:
        return True
    else:
        print(f'O número máximo de operações de saque por dia é de {numero_saques_possiveis}. Você já alcançou este limite.')
        return False

def verifica_limite_saque(valor_saque: float, valor_limite_saque: float) -> bool:
    if valor_saque <= valor_limite_saque:
        return True
    else:
        print('Você ultrapassou o valor permitido para esta operação. Valor limite por saque: R$500,00')
        return False

# INPUT CLIENTE
print('Bem-vindo ao Banco Python.')
while True:
    limpar_tela()
    opcao = input(menu2).lower()
    if opcao == 's':
        if conferir_existencia_cliente(cliente_cpf, dicionario_cliente_contas):
            print('Bem-vindo')
            gerenciar_operacao_bancaria(saldo, extrato, numero_saques)
        else:
            print('Você não se encontra cadastrado em nossa instituição bancária.')
            decisao = decisao_abrir_conta()
            if decisao == True:
                cliente_nome, cliente_data_nascimento, cliente_cpf, cliente_endereco = cadastrar_cliente()
            cliente_lista = [cliente_nome, cliente_data_nascimento, cliente_cpf, cliente_endereco]
            dicionario_cliente_contas[cliente_cpf] = cliente_lista
            gerenciar_operacao_bancaria(saldo, extrato, numero_saques)
    elif opcao == 'n':
        if decisao_abrir_conta():
            cliente_nome, cliente_data_nascimento, cliente_cpf, cliente_endereco = cadastrar_cliente()
            cliente_lista = [cliente_nome, cliente_data_nascimento, cliente_cpf, cliente_endereco]
            dicionario_cliente_contas[cliente_cpf] = cliente_lista
            if decisao_novo_cliente():
                gerenciar_operacao_bancaria(saldo, extrato, numero_saques)
            break
        else:
            break
    elif opcao == 'q':
        limpar_tela()
        print('Obrigado por acessar nosso sistema.\nO Banco Python está sempre de portas abertas.\n')
        break
    else:
        limpar_tela()
        print('Opção inválida.')