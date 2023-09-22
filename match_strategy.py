import os
import subprocess
from time import sleep
import io
import csv
import threading
import signal
import time
from datetime import date

# Não faço ideia do que seja, nem mexi.
RESULT_COMAND_SERVER = ''

# Coleta path do usuário do sistema
USER_PATH = os.path.expanduser('~')

def command(cmd, type=2):
    global RESULT_COMAND_SERVER
    if (type == 1):
        buffer = subprocess.getoutput(cmd)
        RESULT_COMAND_SERVER = str(buffer)
    else:
        os.system(cmd)

def startMatch():
    global RESULT_COMAND_SERVER

    if(MONITOR != 1):
        # Percorre diretórios para a pasta de Log e executa o monitor com reconexão automática
        input_ = "cd ~ && cd " + DIR_LOG + " && rcssmonitor --auto-reconnect-mode on"
        
        # Prepara e inicia thread de execução do monitor
        t0 = threading.Thread(target=command, args=(input_, 1))
        t0.start()

        #Aguarda para evitar sobreposição dos processos.
        sleep(3)

    # Início da execução da estratégia
    inicio = time.time()
    # Array para armazenar os resultados dos jogos
    results = []

    # Loop das partidas
    for i in range(PARTIDAS):

        # modo normal
        input_ = "cd ~ && cd " + DIR_LOG + " && rcssserver server::auto_mode = true"

        # Verifica se o modo rápido foi selecionado e configura execução do modo rápido
        if (int(GAME_MODE) == 2):
            input_ = "cd ~ && cd " + DIR_LOG + \
                " && rcssserver server::auto_mode = true server::nr_extra_halfs = 0 server::penalty_shoot_outs = false  server::synch_mode=true"

        #  iniciando servidor
        t1 = threading.Thread(target=command, args=(input_, 1))

        # adicionando time atual
        input_ = 'cd && cd ' + str(DIR_OUR_TIME) + ' && ./start.sh'
        t2 = threading.Thread(target=command, args=(input_, 2))

        # adicionando time adversário
        input_ = 'cd && cd ' + str(DIR_OPP_TIME) + ' && ./start.sh'
        t3 = threading.Thread(target=command, args=(input_, 2))

        # Executa as threads de Servidor, time atual e time adversário
        t1.start()
        sleep(3)
        t2.start()
        sleep(1)
        t3.start()
        sleep(3)

        # All threads running in parallel, now we wait
        t1.join()
        t2.join()
        t3.join()

        # Obtendo placar
        scores = ['0', '0']
        buf = io.StringIO(RESULT_COMAND_SERVER)
        limit = 10000
        while True:
            line = buf.readline()
            limit = limit - 1
            if (limit == 0):
                break
            if "Score" in line:
                scores = line.replace(" ", "").replace("Score:", "").replace(
                    "\n", "").replace("\t", "").split('-')
                break

        results.append(tuple([int(scores[0]), int(scores[1]), (int(scores[0]) - int(scores[1])), DIR_OPP_TIME]))
        # Verifica se deve Salvar CSV ao final de cada partida
        if(EACH_GAME == 1):
            # Executa função para criar csv dos resultados.
            saveScore(f'{USER_PATH}/{DIR_LOG}/resultados_{date.today()}.csv', results)
            results.clear()

        sleep(5)

    # Fim da execução da estratégia
    fim = time.time()

    # Executa funções para criar csv dos resultados e tempo.
    if(EACH_GAME != 1):
        saveScore(f'{USER_PATH}/{DIR_LOG}/resultados_{date.today()}.csv', results)
    saveTime(f'{USER_PATH}/{DIR_LOG}/time.csv', fim-inicio)

def saveScore(path_file, results):
    #opening_type = 'a' if os.path.isfile(path_file) else opening_type = 'w'

    # Define tipo de abertura do arquivo para criar um novo.
    opening_type = 'w'

    # Caso o arquivo já exista define o tipo de abertura para alterar o conteúdo.
    if(os.path.isfile(path_file)):
        opening_type = 'a'

    # Abre o arquivo e adiciona o conteúdo.
    with open(path_file, opening_type) as f:
        csv_writer = csv.writer(f)
        # Verifica tipo de abertura
        if opening_type == 'w': 
            # Adiciona colunas no csv
            csv_writer.writerow(['Our score', 'Opponent score', 'Goal balance', 'Opponent'])

        # Adiciona resultados
        csv_writer.writerows(results)
        f.close()
    

def saveTime(path_file, time):
    #opening_type = 'a' if os.path.isfile(path_file) else opening_type = 'w'

    # Define tipo de abertura do arquivo para criar um novo.
    opening_type = 'w'

    # Caso o arquivo já exista define o tipo de abertura para alterar o conteúdo.
    if(os.path.isfile(path_file)):
        opening_type = 'a'

    # Abre o arquivo e adiciona o conteúdo.
    with open(path_file, opening_type) as f:
        csv_writer = csv.writer(f)

        # Verifica tipo de abertura
        if opening_type == 'w': 
            csv_writer.writerow(['time (s)'])

        # Adiciona resultados
        csv_writer.writerow([time]) 
        f.close()

def main():

    # Definindo variáveis Globais

    # Numero de Partidas a serem jogadas.
    global PARTIDAS

    # Pasta para salvar os Logs e csv final. Ps.: Colocar o diretório a partir da pasta do usuário.
    global DIR_LOG

    # Pasta que contém o time da UFRBots
    global DIR_OUR_TIME

    # Pasta do Oponente
    global DIR_OPP_TIME

    # GAME_MODE: 1 - normal | 2 - rápido
    global GAME_MODE

    # Indica se deve abrir o monitor ou não.
    global MONITOR

    # Indica se deve salvar o CSV a cada partida. 1 = Salvar csv ao final da partida.
    global EACH_GAME

    # Indica se deve repetir o script.
    repeat = 1

    print("====================================================================================================")
    print("====================================================================================================")
    print("ALGORITMO DE EXECUÇÃO AUTOMÁTICA DE N PARTIDAS - By.: UFRBots - Equipe de Futebol de Robôs da UFRB")
    print("----------------------------------------------------------------------------------------------------")
    print("Este script busca executar de forma automática uma grande quantidade de partidas " +
        "e basta apenas apontar os diretórios corretamente após a execução.")
    print("----------------------------------------------------------------------------------------------------")
    print("IMPORTANTE:")
    print("Caso queira evitar digitar os diretórios sempre que executar, é necessário alterar o script.\n" +
        "Para isto, após abrir o script com um EDITOR, percorra até a função main() e " + 
        "altere os locais indicados pelos comentários.")
    print("Obs.: Procurar pelo comentário (ctrl+f): REDIGITAR VALORES")
    print("====================================================================================================")
    print("====================================================================================================")

    # Indica se o rcssmonitor deve ser aberto ou não.
    # Caso queira que a pergunta não apareça mais, altere seu valor inicial para 1 ou para None.
    # None indica que por padrão abrirá o monitor.
    # 1 indica que por padrão NÃO abrirá o monitor.
    # Qualquer outro valor indica que a pergunta será realizada.
    MONITOR = 0

    # Caso deseje salvar ao final de cada partida, altere seu valor para 1
    EACH_GAME = None

    # Verifica se deve ou não perguntar sobre o rcssmonitor.
    if(MONITOR != 1 and MONITOR != None):
        print("\nO Parâmetro a seguir indica se você deseja que o rcssmonitor NÃO seja aberto. " +
            "Por padrão ele sempre abrirá.")
        MONITOR = input("Desativar rcssmonitor? (1- Sim | Default: Não.) ")

        if(not MONITOR.isnumeric()):
           MONITOR = 0
        else:
            MONITOR = int(MONITOR)

    # Verifica se deve salvar ao final de cada partida
    if(EACH_GAME == None):
        print("\nDeseja salvar o resultado ao final de cada partida?\nPs.: Pode tornar a execução mais lenta.")
        EACH_GAME = input("(1- Sim | Defalt: Não) ")

        if(not EACH_GAME.isnumeric()):
            EACH_GAME = 0
        else:
            EACH_GAME = int(EACH_GAME)

    DIR_LOG = None #"Documentos/Scripts/Logs"
    while True:
        if(DIR_LOG == None or DIR_LOG == ""):
            DIR_LOG = input("\nDigite o diretório da pasta para salvar os Logs e csv. \nPs.: Coloque diretório completo (SEM Home). \n" + 
                            "IMPORTANTE: NÃO coloque diretórios com caracteres especiais ou espaço no Nome das Pastas.\n" +
                            "IMPORTANTE: Caso não o algoritmo exiba 'can't sudo to', execute o comando sudo chmod -R 777 nome_da_pasta.\n")
        else:
            break

    while repeat == 1:

        # =========================================REDIGITAR VALORES=======================================================================================
        # =================================================================================================================================================
        # =================================================================================================================================================
        # SEÇÃO PARA NÃO NECESSITAR REDIGITAR OS VALORES.
        # ATENÇÃO: DEIXE O VALOR None PARA INDICAR QUE DESEJA DIGITAR UM VALOR DIFERENTE AO EXECUTAR O SCRIPT.
        # RECOMENDO DEIXAR A VARIÁVEL DIR_OPP_TIME EM BRANCO.
        # -------------------------------------------------------------------------------------------------------
        # Abaixo estão alguns exemplos em como os valores devem ser adicionados nas variáveis.
        # Obs.: Lembrar que são EXEMPLOS. O diretório depende do seu computador.
        PARTIDAS = None #100
        DIR_OUR_TIME = None #"Documentos/UFRBots/UFRBots2D/Time_novo/UFRBots2D/src"
        DIR_OPP_TIME = None #"Documentos/UFRBots/adversarios/UFRBots2D/Binarios_de_outros_times/RoboCup_2022/HELIOS_SS2D_RC2022_D4_BIN/helios2022/bin"
        # GAME_MODE: 1 - normal | 2 - rápido
        GAME_MODE = None #2
        # IMPORTANTE: A variável de log e monitor estão um pouco mais acima, antes do seu while.
        # =================================================================================================================================================
        # =================================================================================================================================================
        # =================================================================================================================================================
                
        while True:
            if(PARTIDAS == None):
                PARTIDAS = int(input("\nDigite o número de partidas a serem jogadas: "))

            if(DIR_OUR_TIME == None):
                DIR_OUR_TIME = input("\nDigite o diretório do time da UFRBots. Ps.: Pasta que contém o start.sh. \n" + 
                            "IMPORTANTE: NÃO coloque diretórios com caracteres especiais ou espaço no Nome das Pastas.\n" +
                            "IMPORTANTE: Caso não o algoritmo exiba 'can't sudo to', execute o comando sudo chmod -R 777 nome_da_pasta.\n")

            if(DIR_OPP_TIME == None):
                DIR_OPP_TIME = input("\nDigite o diretório do time ADVERSÁRIO. Ps.: Pasta que contém o start.sh. \n" + 
                            "IMPORTANTE: NÃO coloque diretórios com caracteres especiais ou espaço no Nome das Pastas.\n" +
                            "IMPORTANTE: Caso não o algoritmo exiba 'can't sudo to', execute o comando sudo chmod -R 777 nome_da_pasta.\n")
            
            if(1 != GAME_MODE != 2):
                GAME_MODE = int(input("\nDigite o modo de jogo (1 - normal | 2 - rápido): "))
            
            if(PARTIDAS != None and DIR_OUR_TIME != None and DIR_OPP_TIME != None and (GAME_MODE == 1 or GAME_MODE == 2)):
                break

        startMatch()
        print("\n\n\n\n******************** All matches have been played ********************")

        repeat = input("Deseja executar o script novamente? (1- Sim): ")

        if(not repeat.isnumeric()):
            repeat = 0
        else:
            repeat = int(repeat)

        if(repeat != 1):
            break

    print("Encerrando script...")
    sleep(5)
    os.kill(os.getppid(), signal.SIGHUP)

if __name__ == '__main__':
    main()
