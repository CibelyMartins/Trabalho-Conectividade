import socket
import threading

# Função para receber as mensagens do servidor
def receber_mensagens(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode('utf-8')
            print(mensagem)  # Exibe a mensagem
        except:
            print("Erro na conexão com o servidor.")
            break

# Função principal do cliente
def iniciar_cliente():
    host = '192.168.18.43'  # IP do servidor (altere conforme necessário)
    porta = 9999

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((host, porta))
    except:
        print("Não foi possível conectar ao servidor.")
        return

    nome = input("Digite seu nome: ")  # Recebe o nome do cliente
    cliente.send(nome.encode('utf-8'))  # Envia o nome para o servidor

    # Cria uma thread para receber as mensagens do servidor
    threading.Thread(target=receber_mensagens, args=(cliente,)).start()

    # Loop principal para enviar mensagens
    while True:
        mensagem = input()  # Recebe mensagem do usuário
        if mensagem.lower() == 'sair':
            cliente.send("sair".encode('utf-8'))
            cliente.close()
            break
        cliente.send(mensagem.encode('utf-8'))  # Envia mensagem para o servidor

# Inicia o cliente
iniciar_cliente()
