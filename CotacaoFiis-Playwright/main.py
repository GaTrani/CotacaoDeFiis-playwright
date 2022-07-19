import datetime, time
import ListaDeAtivos
from playwright.sync_api import sync_playwright
import BD, sqlite3

contError = 0
contAtivos = 0
cont = 0
listaAtivosError = []
menu = ['Data base', 'Data pgto.', 'Cotação base', 'DY', 'Dividendo']

#CRIAR DATABASE
database = sqlite3.connect('BancoDadosFii.db')
c = database.cursor()

BD.criarTabela()

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False) #removendo ou deixando TRUE nao aparecerá o navegador
    pagina = navegador.new_page()
    horaInicio = datetime.datetime.now()
    print('Hora:', horaInicio)
    for i in ListaDeAtivos.vetorAtivos:
        link = 'https://fiis.com.br/' + i + '/'
        print('Acessando:', link)
        try:
            pagina.goto(link, timeout=10000)
            valorAtivo = pagina.locator('xpath=//*[@id="quotations--infos-wrapper"]/div[1]/span[2]')\
                .text_content(timeout=4000)
            dividendYield = pagina.locator('xpath=//*[@id="informations--indexes"]/td[1]/h3[1]')\
                .text_content(timeout=4000)
            dados = pagina.locator('xpath=//*[@id="last-revenues--table"]/tbody')\
                .text_content(timeout=4000)
        except:
            contError += 1
            listaAtivosError.append(i)
            print('\n\033[31mOcorreu um erro! Ativo', i, 'mudou de nome, nao existe mais ou pagina demorou para responder!\033[m\n')
        else:
            '''if dividendYield == '0,00%':
                print("Próximo ativo...")'''
            if valorAtivo != '0,00' and dividendYield != '0,00%':
                ticker = pagina.locator('xpath=//*[@id="fund-ticker"]').text_content()
                dados = dados.split()
                linhas = int(len(dados) / 7) - 1
                print(contAtivos, i, ':R$', valorAtivo, 'DY', dividendYield)
                print('dados:', dados)
                
                print('linhas:', linhas)
                print('dados 0', dados[7])
                #
                #Inserir dados no Banco de Dados
                #
                cont = 0
                for l in range(0, linhas):
                    for c in range(0, 1):
                        BD.inserirat(ticker, dados[cont + 0], dados[cont + 1], dados[cont + 3], dados[cont + 4], dados[cont + 7])
                        database.commit()
                        cont += 8

            else:
                print('\033[31mO ativo não contém informações. Não existe!\033[m')

        contAtivos += 1

    time.sleep(10)

horaFim = datetime.datetime.now() - horaInicio
print('Tempo de execução:', horaFim)
print('\nLista de ativos com erros:', listaAtivosError)
print('\nAtivos com erros:', contError)