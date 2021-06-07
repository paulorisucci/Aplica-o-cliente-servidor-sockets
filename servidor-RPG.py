import socket
import time
import traceback
from RPG import *
import threading

TAM_MSG = 1024
HOST = '0.0.0.0'
PORT = 40000


def processa_msg_jogador(message, jogador):

    message = message.decode()
    print('Cliente', jogador, 'enviou\n', message)
    command = message.split('\n')

    if command[-1] == 'FIGHT':
        player = convert_str_creature(command[0]) #
        enemy = convert_str_creature(command[1]) # '{self._name}\n{self._level}\n{self._atk}\n{self._def}'
        action = command[2] # 'ATK/DEF/RUN'

        result = embate(player, enemy, action)

        if result == 'RUN':
            sock.sendto(str.encode('RUN'), jogador)

        winner, looser = result
        message = f'{winner}\n{looser}\nO vencedor do confronto foi {winner.name}.'

    else:
        mutex.acquire()
        #time.sleep(5)
        player_atual = convert_str_creature(command[0])
        highscore = open('highscore.txt', 'r')
        highscore.seek(0)
        highscore_content = highscore.read()

        if highscore_content == '':
            highscore = open('highscore.txt', 'w')
            highscore.write(f'{player_atual}')
            message = f'Você foi o primeiro player a jogar. Seu score foi registrado como recorde atual:\n{player_atual}'

        else:
            best_player = convert_str_creature(highscore_content)

            if player_atual.exp > best_player.exp:
                highscore = open('highscore.txt', 'w')
                message = f'''Parabéns, {player_atual.name}. Você conseguiu bater o recorde!
Highscore atual: {player_atual.presentation()}'''
                highscore.write(f'{player_atual}')
            else:
                message = f'''Você ainda não conseguiu bater o recorde.
Highscore atual: {best_player.presentation()}'''
        highscore.seek(0)
        highscore.close()
        mutex.release()
    sock.sendto(str.encode(message), jogador)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv = (HOST, PORT)
sock.bind(serv)
mutex = threading.Semaphore(1)
t1 = threading.Thread()
t1.start()
while True:
    try:
        msg, jogador = sock.recvfrom(TAM_MSG)
        print(jogador, msg.decode())
        t2 = threading.Thread(target=processa_msg_jogador, args=(msg, jogador))
        t2.start()
    except Exception as E:
        traceback.print_exc()
        break

sock.close()