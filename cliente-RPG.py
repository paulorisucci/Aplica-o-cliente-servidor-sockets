import socket
import sys
from RPG import *

BUNITEZA = '*'*30
TAM_MSG = 1024
HOST = '127.0.0.1'
PORT = 40000


def decode_cmd_user(cmd_user):
    cmd_map = {'F': 'FIGHT', 'E': 'EXIT'}

    if cmd_user.upper() in cmd_map:
        cmd_user = cmd_map[cmd_user.upper()]

    elif cmd_user.upper() in cmd_map.values():
        cmd_user = cmd_user.upper()

    else:
        return False

    return cmd_user


def decode_cmd_fight(cmd_user):

    fight_map = ['ATK','DEF','RUN']

    if cmd_user.upper() in fight_map:
        return f'{cmd_user}'
    else:
        return False


creature_map = {
    'GOBLIN':Criatura('GOBLIN', 3, 2, 1, 50),
    'TROLL': Criatura('TROLL', 4, 4, 1, 80),
    'ELF': Criatura('ELF', 6, 5, 2, 200),
    'DARK KNIGHT': Criatura('DARK KNIGHT', 8, 8, 3, 700),
    'DRAGON': Criatura('DRAGON', 11, 10, 6, 5000),
    'MORGAROTH':Criatura('MORGAROTH', 20, 20, 10, 10000)
}

if len(sys.argv) > 1:
    HOST = sys.argv

print('Servidor:',HOST+" "+str(PORT))
serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('''Bem Vindo ao RPG!
Primeiramente, vamos criar o seu personagem''')
nome = input('Digite seu nome: ')
player = Criatura(nome)

print(f'\nBem-vindo \033[0;31;40m{player.name}\033[m. O jogo está prestes a começar!')
print(f'Seus status são:\n{player.presentation()}')
print(BUNITEZA)

while True:

    cmd_player = input('Digite o que deseja fazer (EXIT/E - sair do jogo | FIGHT - lutar):')
    cmd_player = decode_cmd_user(cmd_player.upper())

    if cmd_player == 'FIGHT':
        print('Escolha o inimigo a enfrentar: ')
        print(creature_map.keys())
        print(BUNITEZA)
        try:
            creature = input('Inimigo> ').upper()
            enemy = creature_map[creature]
            print('Status do jogador:\n', player.presentation())
            print(BUNITEZA)
            print(enemy.presentation())
            print(BUNITEZA)
        except:
            print('Inimigo inválido. Tente novamente.')
            continue

        print('Digite como deseja enfrentá-la: (ATK - ATTACK, DEF DEFENDE, RUN)')
        cmd_user = input('Comando> ').upper()

        if not decode_cmd_fight(cmd_user):
            print('Comando inválido. Tente novamente.')
            continue

        cmd_fight = f'{player}\n{enemy}\n{decode_cmd_fight(cmd_user)}\n{cmd_player}'

        if not cmd_fight[2]:
            print('Comando indefinido:',cmd_user)
        else:
            command = sock.sendto(str.encode(cmd_fight), serv)
            result, peer = sock.recvfrom(TAM_MSG)
            result = result.decode().split('\n')

            if result[0] == 'RUN':
                print('Você conseguiu fugir.')
                print(BUNITEZA)
                continue

            winner = convert_str_creature(result[0])
            looser = convert_str_creature(result[1])
            message = result[2]

            print(message)

            if winner.name == player.name:
                player = winner
                enemy = looser
                print(f'Parabéns, você venceu!')
                print(BUNITEZA)
                player.gain_exp(enemy.exp)
            else:
                player = looser
                enemy = winner
                print('VOCÊ PERDEU.\nGAME OVER.')
                print(BUNITEZA)
                break

    elif cmd_player == 'EXIT':

        cmd = f'{player}\n{cmd_player}'
        sock.sendto(str.encode(cmd), serv)
        result = sock.recvfrom(TAM_MSG)
        final_result = result[0].decode()
        print(final_result)
        print(BUNITEZA)
        break

    else:
        print('Comando inválido. Tente novamente.')

sock.close()