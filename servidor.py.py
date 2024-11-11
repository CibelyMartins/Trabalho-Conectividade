import socket
import threading

# Lista de clientes conectados
clientes = []

# Função para enviar mensagens para todos os clientes
def enviar_para_todos(mensagem, cliente_removido=None):
    for cliente in clientes:
        if cliente != cliente_removido:  # Não envia para o cliente que enviou
            try:
                cliente.send(mensagem.encode('utf-8'))
            except:
                # Se não conseguir enviar, desconecta o cliente
                clientes.remove(cliente)
                cliente.close()

# Função que trata cada cliente
def lidar_com_cliente(cliente, endereco):
    # Recebe o nome do cliente
    nome = cliente.recv(1024).decode('utf-8')
    clientes.append(cliente)  # Adiciona o cliente à lista
    print(f'{nome} entrou no chat.')

    # Notifica todos os clientes que um novo usuário entrou
    enviar_para_todos(f'{nome} entrou no chat.')

    while True:
        try:
            # Recebe mensagem do cliente
            mensagem = cliente.recv(1024).decode('utf-8')
            if mensagem.lower() == 'sair':
                break  # Se digitar 'sair', o cliente sai
            enviar_para_todos(f'{nome}: {mensagem}', cliente)
        except:
            break  # Se algo der errado, sai do loop

    # Quando o cliente sai, remove da lista e notifica a saída
    clientes.remove(cliente)
    cliente.close()
    enviar_para_todos(f'{nome} saiu do chat.')

# Função principal do servidor
def iniciar_servidor():
    host = '0.0.0.0'  # Aceita conexões de qualquer IP
    porta = 9999

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, porta))
    servidor.listen(5)

    print(f"Servidor iniciado em {host}:{porta}")

    while True:
        cliente, endereco = servidor.accept()  # Aceita nova conexão
        print(f'Nova conexão de {endereco}')
        # Cria uma nova thread para lidar com o cliente
        threading.Thread(target=lidar_com_cliente, args=(cliente, endereco)).start()

# Inicia o servidor
iniciar_servidor()
