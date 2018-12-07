#!/usr/bin/env python3
# Python 3.6

import hlt  # Importa o SDK Halite, que permite interagir com o jogo.
from hlt import constants # Esta biblioteca contem os valores constantes.
from hlt.positionals import Direction # Esta biblioteca contem a metadata de direcao.
from hlt.positionals import Position # Esta biblioteca contem a metadata de posicao.

# Funcao para encontrar a posicao com maior quantidade de halite | Parametros: (Game game_map, Integer largura, Integer altura)
def getHighestValuePosition(game_map, width, height):
    highestValue = 0
    highestPosition = Position(0,0)
    posx = 0
    posy = 0
    # Itera cada posicao do mapa, checa a quantidade e salva nas variaveis o melhor resultado encontrado
    for x in range(0, width):
        posx = x
        for y in range (0, height):
            posy = y
            position = Position(posx, posy)
            if game_map[position].halite_amount > highestValue:
                highestValue = game_map[position].halite_amount
                highestPosition = position
    return highestPosition

# Funcao para encontrar o barco mais proximo da melhor posicao | Paramentros: (Game me, Game game_map, Position melhor_posicao, List lista_de_retorno)
def getCloserShip(me, game_map, highestPosition, listReturn):
    shortestDistance = 1000
    closerShip = 1000
    # Itera todos os barcos, calculando a distancia manhattan da sua posicao ate a melhor posicao, salva o id do barco mais proximo na variavel
    for ship in me.get_ships():
        if game_map.calculate_distance(ship.position, highestPosition) < shortestDistance:
            shortestDistance = game_map.calculate_distance(ship.position, highestPosition)
            closerShip = ship.id
    if ship in listReturn:
        listReturn.remove(closerShip)
    return closerShip

# Funcao para enncontrar o dropoff mais proximo do barco | Parametros: Game game_map, Ship objeto_do_barco, List posicoes_dos_dropoffs, Position posicao_da_base_do_jogador)
def getCloserUnload(game_map, ship, dropoffs, base):
    position = base
    # Se a lista de dropoffs nao estiver nula
    if not dropoffs is None:
        # Itera todos os dropoffs e calcula a distancia manhattan do barco até o dropoff, salva o melhor resultado encontrado na variavel.
        for drop in dropoffs:
            if game_map.calculate_distance(ship.position, drop.position) < game_map.calculate_distance(ship.position, base):
                position = drop.position
            else:
                position = base
    return position
