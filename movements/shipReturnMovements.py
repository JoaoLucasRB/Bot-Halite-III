#!/usr/bin/env python3
# Python 3.6

import hlt  # Importa o SDK Halite, que permite interagir com o jogo.
from hlt import constants # Esta biblioteca contem os valores constantes.
from hlt.positionals import Direction # Esta biblioteca contem a metadata de direcao.
from hlt.positionals import Position # Esta biblioteca contem a metadata de posicao.
import random # Esta biblioteca permite você gerar numeros aleatorios.
from movements import turnStrategy as tS # Esta biblioteca contem as funcoes para a estrategia do turno.

# Funcao para adicionar/remover barcos da lista de retorno
def returnAddRem(turn_number, ship, base, listReturn, command_queue):
    # Se o barco estiver cheio, adiciona a lista de retorno
    # Caso contrario, se o barco estiver na base, remove da lista de retorno
    if turn_number == 360 and not ship.id in listReturn:
        listReturn.append(ship.id)
    elif turn_number > 420 and ship.halite_amount > 400 and not ship.id in listReturn:
        listReturn.append(ship.id)
    if ship.is_full and not ship.id in listReturn:
        listReturn.append(ship.id)
    elif ship.id in listReturn and ship.position == base:
        listReturn.remove(ship.id)

# Funcao para mover o barco na direcao da base
def returnShip(game_map, ship, base, listNextPos, command_queue):
    baseCard = base.get_surrounding_cardinals() # Lista com as posicoes cardeais da base

    # Condicionais para forcar o barco a vir pela laterais Oeste ou Leste da base
    if ship.position.y == base.y:
        randomDir = random.choice([Direction.North, Direction.South])
        position  = Position(ship.position.x+randomDir[0], ship.position.y+randomDir[1])
        if not position in listNextPos:
            listNextPos.append(position)
            command_queue.append(ship.move(randomDir))
        else:
            listNextPos.append(ship.position)
            command_queue.append(ship.stay_still())
    
    # Condicional para mover o barco na direcao da base
    elif not ship.position in baseCard:
        position1 = Position(base.x, base.y-1)
        position2 = Position(base.x, base.y+1)
        if game_map.calculate_distance(ship.position, position1) < game_map.calculate_distance(ship.position, position2):
            returnPosition = position1
        else:
            returnPosition = position2
        direction = game_map.naive_navigate(ship, returnPosition) # Contem o retorno de naive_navigate (Direction)
        position = Position(ship.position.x+direction[0], ship.position.y+direction[1]) # calcula a posicao da direcao
        # se a posicao nao estiver na lista de proximas posicoes, move para a posicao
        if not position in listNextPos:
            listNextPos.append(position)
            command_queue.append(ship.move(direction)) 
        
        # Caso contrario da o comando para o barco esperar ate o proximo turno
        else:
            listNextPos.append(ship.position)
            command_queue.append(ship.stay_still())
    else:
        direction = game_map.naive_navigate(ship, base) # Contains the return from naive_navigate ( Direction )
        position = Position(ship.position.x+direction[0], ship.position.y+direction[1]) # calculate position from direction
        # If next position not in list of next positions, move on direction
        if not position in listNextPos:
            listNextPos.append(position)
            command_queue.append(ship.move(direction))  
        else:
            listNextPos.append(ship.position)
            command_queue.append(ship.stay_still())  

# Funcao para retornar todos os barcos ate o dropoff mais proximo (Mata todos os barcos)
def endReturn(game_map, ship, base, dropoffs, listNextPos, command_queue):
    game_map[ship.position].mark_unsafe(ship)
    closerUnload = tS.getCloserUnload(game_map, ship, dropoffs, base)
    # Pega a posicao cardeal do dropoff mais proximo
    closerCard = closerUnload.get_surrounding_cardinals()
    # se o barco estiver em uma das posicoes cardeais do dropoff, move o barco com unsafe moves para entregar o halite e matar ele na base
    if ship.position in closerCard:
        direction = game_map.get_unsafe_moves(ship.position, closerUnload)
        command_queue.append(ship.move(direction[0]))
    # Caso contrario, move com naive navigate
    else:
        direction = game_map.naive_navigate(ship, closerUnload)
        position = Position(ship.position.x+direction[0], ship.position.y+direction[1])
        if not position in listNextPos:
            listNextPos.append(position)
            command_queue.append(ship.move(direction))
        else:
            listNextPos(ship.position)
            command_queue.append(ship.stay_still())