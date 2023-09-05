# ALGORITMO DE EXECUÇÃO AUTOMÁTICA DE N PARTIDAS 
## By.: UFRBots - Equipe de Futebol de Robôs da UFRB

Este script tem o intuito de executar várias partidas do futebol de robôs sem que seja necessária interferência do usuário e ao fim da execução gerar um arquivo .csv com os resultados.
Foi desenvolvido para agilizar a análise dos gols marcados, gols recebidos e saldo de gols do time.

**É possível [modificar](#modificando-o-script) o arquivo de forma rápida e fácil para que não seja mais necessário indicar os valores solicitados sempre que o script for executado.**

**IMPORTANTE:** Para que o script funcione é necessário que o [rcsoccersim](https://github.com/rcsoccersim/) esteja configurado e funcionando corretamente.

### Permite que

- Execute ou não o monitor de partidas.
- Defina um diretório para os logs das partidas e arquivo .csv.
- Defina uma quantidade variável de partidas a serem executadas.
- Defina um diretório para os times. **Obs.:** Indique a pasta onde está o arquivo ``` start.sh ``` dos times.
- Execute a partida no modo Rápido ou normal.
- Gere um arquivo .csv com os resultados obtidos dos experimentos.

### Como Utilizar

- Abra o terminal na pasta do script.
- Execute o script com o comando ``` python3 match_strategy.py ```.
- Sugiro que **leia os prints** exibidos pelo script.
- **Importante:** Ao adicionar os diretórios **NÃO** é necessário colocar a pasta *home* e nem a pasta do nome de usuário. Por exemplo, caso deseje adicionar um diretório que esteja localizado em ``` home/meuUser/Documentos/Times/timeFinal ``` remova o início e insira apenas ``` Documentos/Times/timeFinal ```.
- Siga o passo a passo exibido no terminal para definir os valores.

**Obs.:** Caso o script não consiga acessar algum diretório indicado pode ser que se trata de permissões do linux, uma das possíveis soluções é abrir o terminal no diretório problemático e executar o comando ``` sudo chmod -R 777 nome_da_pasta. ```.

### Modificando o Script:
<!-- #modificando-o-script -->
É possível "impedir" que alguns valores (diretórios, modo de jogo, etc) não precisem ser solicitados fazendo pequenas alterações no código.

Para isto:

- Abra um script com um editor de código.
- Busque por ``` REDIGITAR VALORES ``` utilizando o atalho CTRL + F.
- Leia os comentários.

Basicamente o script busca por valores definidos como ``` None ``` para decidir se deve ou não solicitar que o valor seja digitado.

Assim, caso queira definir valores fixos basta apenas apagar o valor ``` None ``` e inserir o valor desejado. Não é necessário fazer em todas as variáveis, apenas naquelas que desejar.

Ex.: Vamos supor que você deseja definir um valor fixo para o numero de partidas, sendo assim, busque no código o seguinte trecho:
``` PARTIDAS = None ```.
Em seguida, substitua pelo valor desejado
``` PARTIDAS = 1000 ```
Salve e execute o script.
