Prova realizada em Python para a vaga de estágio da Nasajon onde era necessário criar uma conta no backend de candidatos, confirmar a conta, fazer o login e obter um token de acesso, então desenvolver um programa, que
preferi realizar em Python, para ler um arquivo .csv, enriquecer os resultados através da API do IBGE, gerar um outro arquivo .csv com os dados enriquecidos e corrigidos, então calcular estatísticas com base no mesmo e
enviar para uma API de correção.

A respeito das decisões tomadas no projeto:
Escolhi a abordagem de baixar os municípios da API do IBGE uma só vez para reduzir o número de chamadas necessárias, o que irá melhorar a performance da aplicação. O tratamento dos dados assim também pode ser feito de
forma local uma vez que todos os dados tenham sido baixados corretamente. Após isso, em arquivos separados, realizei a normalização dos nomes para facilitar o tratamento dos dados, visualização e também para que
suas estatísticas pudessem ser analisadas corretamente posteriormente. Assim eles também ficam mais fáceis de serem encontrados.
A estrutura inicial do projeto é separada em diversos arquivos, onde cada um faz uma função específica. Optei por primeiramente tratar os dados e fazer um arquivo que verifica se a API do IBGE está funcionando corretamente,
e então lida com o arquivo .csv original dado, sem a correção dos erros por enquanto. Fiz isso para maior controle do que esse programa faz, para verificar se ele está lidando com os erros de forma correta, e está colocando
os status corretos em cada linha da tabela, sendo eles: OK - para um match único correto, NAO_ENCONTRADO para nenhum match encontrado na base do IBGE, comum onde o nome foi digitado de forma errada, ERRO_API para eventuais
erros da API do IBGE, ou como verifiquei algumas vezes no arquivo, para algum tratamento de normalização que foi feito de forma errada e portanto não conseguiu interagir corretamente com a API, e AMBIGUO para mais de um
match encontrado que será tratado posteriormente em outro arquivo.
Deixei mais detalhes e comentários nos próprios arquivos .py, e vi que a API retornou que os dados estão parcialmente corretos, assumo que por algum erro de cálculo em algum dos arquivos.
