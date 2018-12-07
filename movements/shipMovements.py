#!/usr/bin/env python3
# Python 3.6

import hlt  # Importa o SDK Halite, que permite interagir com o jogo.
from hlt import constants # Esta biblioteca contem os valores constantes.
from hlt.positionals import Direction # Esta biblioteca contem a metadata de direcao.
from hlt.positionals import Position # Esta biblioteca contem a metadata de posicao.
import random # Esta biblioteca permite você gerar numeros aleatorios.

# Funcao para decidir o movimento do barco.
def moveShip(game_map, ship, base, listNextPos, command_queue):
    arrayPosition = ship.position.get_surrounding_cardinals() # Lista com todas as posicoes cardeais do barco.
    values = [] # Lista com a quantidade de halite de cada posicao cardeal do barco.

    # Itera cada posicao cardeal do barco
    for pos in arrayPosition:
        values.append(game_map[pos].halite_amount) # Adiciona os valores de halite das posicoes a lista values.
    valuesSorted = sorted(values, key=int, reverse = True) # Organiza os valores em ordem decrescente.
    confMove = False # Flag para a confirmacao do movimento.
    # Percorre cada posicao de valuesSorted em ordem decrescente de acordo com o index relacional.
    # Checando valuesSorted[0]
    position = arrayPosition[values.index(valuesSorted[0])] # Pega a posicao de index igual a valuesSorted[0]
    direction = arrayPosition.index(position) # Pega a direcao de index igual a posicao
    
    # Se a direcao for igual a X e a posicao nao estiver ocupada nem na lista de proximas posicoes, move o barco
    if direction == 0 and not game_map[position].is_occupied and not position in listNextPos:
        confMove = True
        listNextPos.append(position)
        command_queue.append(ship.move(Direction.North))
    elif direction == 1 and not game_map[position].is_occupied and not position in listNextPos:
        confMove = True
        listNextPos.append(position)
        command_queue.append(ship.move(Direction.South))
    elif direction == 2 and not game_map[position].is_occupied and not position in listNextPos:
        confMove = True
        listNextPos.append(position)
        command_queue.append(ship.move(Direction.East))
    elif direction == 3 and not game_map[position].is_occupied and not position in listNextPos:
        confMove = True
        listNextPos.append(position)
        command_queue.append(ship.move(Direction.West))
            
    # Caso o barco nao tenha um movimento confirmado
    # Checando valuesSorted[1]
    if not confMove:
        position = arrayPosition[values.index(valuesSorted[1])]
        direction = arrayPosition.index(position)
        if direction == 0 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.North))
        elif direction == 1 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.South))
        elif direction == 2 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.East))
        elif direction == 3 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.West))
       
    # Caso o barco nao tenha um movimento confirmado
    # Checando valuesSorted[2]
    if not confMove:
        position = arrayPosition[values.index(valuesSorted[2])]
        direction = arrayPosition.index(position)
        if direction == 0 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.North))
        elif direction == 1 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.South))
        elif direction == 2 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.East))
        elif direction == 3 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.West))
      
    # Caso o barco nao tenha um movimento confirmado
    # Checando valuesSorted[3]
    if not confMove:
        position = arrayPosition[values.index(valuesSorted[3])]
        direction = arrayPosition.index(position)
        if direction == 0 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.North))
        elif direction == 1 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.South))
        elif direction == 2 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.East))
        elif direction == 3 and not game_map[position].is_occupied and not position in listNextPos:
            confMove = True
            listNextPos.append(position)
            command_queue.append(ship.move(Direction.West))
        
    # Caso o barco nao tenha um movimento confirmado
    # Da o comando para ficar parado e esperar o proximo turno
    if not confMove and ship.position != base:
        confMove = True
        listNextPos.append(position)
        command_queue.append(ship.stay_still())
    
    
# Funcao para mover o ship na direcao da melhor posicao
def shipMoveToHighest(game_map, ship, highestPosition, listNextPos, command_queue):
    direction = game_map.naive_navigate(ship, highestPosition) # Contains the return from naive_navigate ( Direction )
    position = Position(ship.position.x+direction[0], ship.position.y+direction[1]) # calculate position from direction
    # If next position not in list of next positions, move on direction
    if not position in listNextPos:
        listNextPos.append(position)
        command_queue.append(ship.move(direction))    

# Funcao para forcar o barco a sair da base (nao utilizada)
"""def leaveBase(game_map, ship, base, listNextPos, command_queue):
    positionWest = Position(base.x-1, base.y)
    positionEast = Position(base.x+1, base.y)
    if game_map[positionWest].halite_amount > game_map[positionEast].halite_amount:
        if not game_map[positionWest].is_occupied and not positionWest in listNextPos:
            listNextPos.append(positionWest)
            command_queue.append(ship.move(Direction.West))
        else:
            listNextPos.append(ship.position)
            command_queue.append(ship.stay_still())
    elif game_map[positionEast].halite_amount > game_map[positionWest].halite_amount:
        if not game_map[positionEast].is_occupied and not positionEast in listNextPos:
            listNextPos.append(positionEast)
            command_queue.append(ship.move(Direction.East))
        else:
            listNextPos.append(ship.position)
            command_queue.append(ship.stay_still())
    else:
        randomDirection = random.choice([Direction.East, Direction.West])
        if randomDirection == Direction.East:
            listNextPos.append(positionEast)
            command_queue.append(ship.move(Direction.East))
        else:
            listNextPos.append(positionWest)
            command_queue.append(ship.move(Direction.West))"""