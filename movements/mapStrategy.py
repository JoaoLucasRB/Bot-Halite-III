import hlt  # Importa o SDK Halite, que permite interagir com o jogo.
from hlt import constants # Esta biblioteca contem os valores constantes.
from hlt.positionals import Direction # Esta biblioteca contem a metadata de direcao.
from hlt.positionals import Position # Esta biblioteca contem a metadata de posicao.

# Funcao para pegar a quantidade de jogadores de acordo com o tamanho do mapa e a posicao inicial do jogador | Parametros: (Position posicao_da_base_do_jogador, Integer largura_do_mapa)
def getPlayerQty(base, x_mapSize):
    if x_mapSize == 32:
        if base == Position(8,16) or base == Position(23,16):
            return 2
        elif base == Position(8,8) or base == Position(8,23) or base == Position(23,8) or base == Position(23,23):
            return 4
    elif x_mapSize == 40:
        if base == Position(11,20) or base == Position(28,20):
            return 2
        elif base == Position(11,11) or base == Position(28,11) or base == Position(11,28) or base == Position(28,28):
            return 4
    elif x_mapSize == 48:
        if base == Position(12,24) or base == Position(35,24):
            return 2
        elif base == Position(14,14) or base == Position(33,14) or base == Position(14,33) or base == Position(33,33):
            return 4
    elif x_mapSize == 56:
        if base == Position(14,28) or base == Position(41,28):
            return 2
        elif base == Position(18,18) or base == Position(37,18) or base == Position(18,37) or base == Position(37,37):
            return 4
    elif x_mapSize == 64:
        if base == Position(16,32) or base == Position(47,32):
            return 2
        elif base == Position(21,21) or base == Position(42,21) or base == Position(21,42) or base == Position(42,42):
            return 4

# Funcao para determinar a posicao das bases dos outros jogadores | Parametros: (Position posicao_da_base_do_jogador, Integer largura_do_mapa, Integer quantidade_de_jogadores)    
def getShipyardPositions(base, x_mapSize, playerQty):   
    shipyards = []
    # sizeX_Y | X - Largura do mapa | Y- Quantidade de jogadores
    size32_2 = [Position(8,16), Position(23,16)]
    size32_4 = [Position( 8, 8), Position( 8,23), Position(23, 8), Position(23,23)]
    size40_2 = [Position(11,20), Position(28,20)]
    size40_4 = [Position(11,11), Position(28,11), Position(11,28), Position(28,28)]
    size48_2 = [Position(12,24), Position(35,24)]
    size48_4 = [Position(14,14), Position(33,14), Position(14,33), Position(33,33)]
    size56_2 = [Position(14,28), Position(41,28)]
    size56_4 = [Position(18,18), Position(37,18), Position(18,37), Position(37,37)]
    size64_2 = [Position(16,32), Position(47,32)]
    size64_4 = [Position(21,21), Position(42,21), Position(21,42), Position(42,42)]
    
    if x_mapSize == 32:
        if playerQty == 2:
            shipyards = size32_2
        if playerQty == 4:
            shipyards = size32_4
    elif x_mapSize == 40:
        if playerQty == 2:
            shipyards = size40_2
        if playerQty == 4:
            shipyards = size40_4
    elif x_mapSize == 48:
        if playerQty == 2:
            shipyards = size48_2
        if playerQty == 4:
            shipyards = size48_4
    elif x_mapSize == 56:
        if playerQty == 2:
            shipyards = size56_2
        if playerQty == 4:
            shipyards = size56_4
    elif x_mapSize == 64:
        if playerQty == 2:
            shipyards = size64_2
        if playerQty == 4:
            shipyards = size64_4
    return shipyards