#!/usr/bin/env python3
# Python 3.6

import hlt  # Importa o SDK Halite, que permite interagir com o jogo.
from hlt import constants # Esta biblioteca contem os valores constantes.
from hlt.positionals import Direction # Esta biblioteca contem a metadata de direcao.
from hlt.positionals import Position # Esta biblioteca contem a metadata de posicao.
import random # Esta biblioteca permite você gerar numeros aleatorios.
from movements import mapStrategy as mS # Esta biblioteca contem as funcoes para a estrategia do mapa.
from movements import shipMovements as sM # Esta biblioteca contem as funcoes para o movimento dos barcos.
from movements import shipReturnMovements as sR # Esta biblioteca contem as funcoes para os movimentos de retorno dos barcos.
from movements import turnStrategy as tS # Esta biblioteca contem as funcoes para a estrategia do turno.

""" <<<Game Begin>>> """

game = hlt.Game() # Este objeto game contem o estado inicial do jogo.
# Neste ponto a variavel "game" é populada com os dados iniciais do mapa.

game.ready("MyPythonBot") # Manda o sinal para o servidor de que o bot esta pronto.

listReturn = [] # Lista com o id de todos os barcos que vao retornar/estao retornando para a base (tipo: int).
listConfMoveShips = [] # Lista com o id de todos os barcos que tem seu movimento para o turno confirmado(tipo: int).
sShip = [] # Lista com o id dos barcos selecionados para a estrategia do mapa (tipo: int).
shipyards = [] # Lista com as possiveis posicoes de todos os shipyards do mapa (tipo: Position).

"""   <<<Game Loop>>> """


while True: # Este loop gerencia cada turno do jogo. O objeto game muda todo turno, e se atualiza seu estado chamando a funcao update_frame().
    game.update_frame() # Atualiza o estado do jogo.
    me = game.me # Objeto com a metadata do jogador.
    game_map = game.game_map # Objeto com a metadata do mapa.
    command_queue = [] # Lista com todos os comandos que vao ser executados neste turno.
    base = me.shipyard.position # Contem a posicao da base do bot.
    listNextPos = [] # Lista com todas as posicoes confirmadas que os barcos vao tomar no proximo turno.
    
    # Caso o jogo esteja no turno 20, faz a busca por todas as shipyards do jogo de acordo com a quantidade de jogadores, e passa o resultado para a lista shipyards.
    if game.turn_number == 20:
        shipyards = mS.getShipyardPositions(base,game_map.width,mS.getPlayerQty(base,game_map.width))
        for position in shipyards:
            if position != base:
                closerShip = tS.getCloserShip(me, game_map, position, listReturn)
                sShip.append(closerShip)
            elif position == base:
                shipyards.remove(position)

    # Caso o jogo esteja abaixo do turno 250, toma as decisoes de movimento comum.
    elif game.turn_number < 250:
        # Caso o turno seja maior que 20, envia os barcos selecionados para a estrategia do mapa ate suas posicoes.
        if game.turn_number > 20:
            for i in range(len(sShip)):
                for ship in me.get_ships():
                    if ship.id == sShip[i]:
                        if ship.id in listReturn:
                            listReturn.remove(ship.id)
                        sM.shipMoveToHighest(game_map, ship, shipyards[i], listNextPos, command_queue)
                        listConfMoveShips.append(ship.id)
        
        # Itera todos os barcos existentes.
        for ship in me.get_ships():
            
            # Caso o barco não tenha recebido nenhum comando.
            if not ship.id in listConfMoveShips:
                game_map[ship.position].mark_unsafe(ship) # Marca a posicao atual do barco como unsafe (utilizado no naive_navigate).
                sR.returnAddRem(game.turn_number, ship, base, listReturn, command_queue) # Chama a funcao para checar se o barco precisa ser adicionado/removido da lista de retorno.
                
                # Checa se o barco esta retornando para a base.
                if ship.id in listReturn:
                    sR.returnShip(game_map, ship, base, listNextPos, command_queue) # Chama a funcao para retornar o barco a posicao de dropoff.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.

                # Caso contrario, checa a quantidade de halite da posicao atual do barco, se estiver abaixo de 90, vai para outra posicao.
                elif game_map[ship.position].halite_amount < 90:
                    sM.moveShip(game_map, ship, base, listNextPos, command_queue) # Chama a funcao para mover o barco.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.

                # Caso contrario, manda o barco ficar na posicao e coletar halite.
                else:
                    command_queue.append(ship.stay_still()) # Comando para ficar parado.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.

    # Caso o jogo esteja no turno 250, toma as decisoes de movimento para a posicao com maior quantidade de halite no mapa (usada para gerar o segundo dropoff e mover os barcos para uma area nao explorada).
    elif game.turn_number == 250:
        highestPosition = tS.getHighestValuePosition(game_map, game_map.width, game_map.height) # Pega a posicao do mapa com a maior quantidade de halite
        closerShip = tS.getCloserShip(me, game_map, highestPosition, listReturn) # Pega o barco mais proximo da posicao

        # Itera todos os barcos existentes.
        for ship in me.get_ships():
            
            # Caso o barco não tenha recebido nenhum comando.
            if not ship.id in listConfMoveShips:
                game_map[ship.position].mark_unsafe(ship) # Marca a posicao atual do barco como unsafe (utilizado no naive_navigate).
                sR.returnAddRem(game.turn_number, ship, base, listReturn, command_queue) # Chama a funcao para checar se o barco precisa ser adicionado/removido da lista de retorno.
                
                # Checa se o barco esta retornando para a base.
                if ship.id in listReturn:
                    sR.returnShip(game_map, ship, base, listNextPos, command_queue) # Chama a funcao para retornar o barco a posicao de dropoff.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.
                
                # Caso contrario, checa a quantidade de halite da posicao atual do barco, se estiver abaixo de 40, vai para outra posicao.
                elif game_map[ship.position].halite_amount < 40:
                    sM.moveShip(game_map, ship, base, listNextPos, command_queue) # Chama a funcao para mover o barco.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.
                
                # Caso contrario, manda o barco ficar na posicao e coletar halite.
                else:
                    command_queue.append(ship.stay_still()) # Comando para ficar parado.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.

    # Caso o jogo esteja no turno 260, toma as decisoes para criacao do dropoff               
    elif game.turn_number == 260:

        # Itera todos os barcos existentes.
        for ship in me.get_ships():
           
            # Caso o barco não tenha recebido nenhum comando.
            if not ship.id in listConfMoveShips:

                # Checa se o id do barco e igual o do closerShip, e se a quantidade total de halite e maior que 4000, se for cria um dropoff.
                if ship.id == closerShip and me.halite_amount > 4000:
                    command_queue.append(ship.make_dropoff()) # Comando para gerar um dropoff.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.
                
                # Caso contrario, Checa se o barco esta retornando para a base.
                elif ship.id in listReturn:
                    sR.returnShip(game_map, ship, base, listNextPos, command_queue) # Chama a funcao para retornar o barco a posicao de dropoff.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.
                
                # Caso contrario, checa a quantidade de halite da posicao atual do barco, se estiver abaixo de 40, vai para outra posicao.
                elif game_map[ship.position].halite_amount < 40:
                    sM.moveShip(game_map, ship, base, listNextPos, command_queue) # Chama a funcao para mover o barco.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.

                # Caso contrario, manda o barco ficar na posicao e coletar halite.
                else:
                    command_queue.append(ship.stay_still()) # Comando para ficar parado.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.

    # Caso o jogo esteja entre o turno 250 e 270, move todos os barcos na direcao da posicao com maior quantidade de halite.
    elif game.turn_number > 250 and game.turn_number < 270:

        # Itera todos os barcos existentes.
        for ship in me.get_ships():

            # Caso o barco não tenha recebido nenhum comando.
            if not ship.id in listConfMoveShips:
                game_map[ship.position].mark_unsafe(ship) # Marca a posicao atual do barco como unsafe (utilizado no naive_navigate).
                sM.shipMoveToHighest(game_map, ship, highestPosition, listNextPos, command_queue) # Move o barco na direcao da posicao com maior quantidade de halite.
                listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.
    
    # Caso o jogo esteja entre o turno 270 e 462, toma as decisoes de movimento comum.
    elif game.turn_number > 270 and game.turn_number < 462:

        # Itera todos os barcos existentes.
        for ship in me.get_ships():
            
            # Caso o barco não tenha recebido nenhum comando.
            if not ship.id in listConfMoveShips:
                game_map[ship.position].mark_unsafe(ship) # Marca a posicao atual do barco como unsafe (utilizado no naive_navigate).
                closerUnload = tS.getCloserUnload(game_map, ship, me.get_dropoffs(), base) # Chama a funcao para pegar o dropoff mais proximo.
                sR.returnAddRem(game.turn_number, ship, closerUnload, listReturn, command_queue)  # Chama a funcao para checar se o barco precisa ser adicionado/removido da lista de retorno.
                
                # Checa se o barco esta retornando para a base.
                if ship.id in listReturn:
                    sR.returnShip(game_map, ship, closerUnload, listNextPos, command_queue)  # Chama a funcao para retornar o barco a posicao de dropoff.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.

                # Caso contrario, checa a quantidade de halite da posicao atual do barco, se estiver abaixo de 40, e o jogo esteja abaixo do turno 360, vai para a proxima posicao.
                elif game_map[ship.position].halite_amount < 40 and game.turn_number < 360:
                    sM.moveShip(game_map, ship, base, listNextPos, command_queue) # Chama a funcao para mover o barco.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.

                # Caso contrario, checa a quantidade de halite da posicao atual do barco, se estiver abaixo de 10, e o jogo esteja acima do turno 360, vai para a proxima posicao.    
                elif game_map[ship.position].halite_amount < 10 and game.turn_number >= 360:
                    sM.moveShip(game_map, ship, base, listNextPos, command_queue) # Chama a funcao para mover o barco.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.
                
                # Caso contrario, manda o barco ficar na posicao e coletar halite.
                else:
                    command_queue.append(ship.stay_still()) # Comando para ficar parado.
                    listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.

    # Caso o jogo esteja acima do turno 462
    elif game.turn_number >= 462:

        # Itera todos os barcos existentes.
        for ship in me.get_ships():

            # Caso o barco não tenha recebido nenhum comando.
            if not ship.id in listConfMoveShips:
                sR.endReturn(game_map, ship, base, me.get_dropoffs(), listNextPos, command_queue) # Chama a funcao para retornar todos os barcos a posicao mais proxima, e se matar.
                listConfMoveShips.append(ship.id) # Adiciona o id do barco a lista de movimentos confirmados.

    # Se o jogo estiver abaixo do turno 200, e a quantidade de halite do jogador for maior que o custo do barco (1000), e a shipyard do jogador nao esteja ocupada, gera um novo barco.
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn()) # Comando para gerar um novo barco.
    
    # Caso contrario, se o jogo estiver entre o turno 300 e 360 e a quantidade de halite do jogador for maior que 6000, e a shipyard do jogador nao esteja ocupada, gra um novo barco.
    elif game.turn_number > 300 and game.turn_number < 360 and me.halite_amount > 6000 and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn()) # Comando para gerar um novo barco.
    
    listConfMoveShips.clear() # Limpa a lista de comandos confimados.
    game.end_turn(command_queue) # Envia a lista de comandos para o ambiente do jogo, encerrando o turno.

