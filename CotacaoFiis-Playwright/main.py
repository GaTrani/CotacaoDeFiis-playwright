from datetime import date
import time
import datetime
import ListaDeAtivos
from playwright.sync_api import sync_playwright

contError = 0
contAtivos = 0
listaAtivosError = []
with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
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
            if dividendYield == '0,00%':
                print("Próximo ativo...")
            if valorAtivo != '0,00' and dividendYield != '0,00%':
                dados = dados.split()
                linhas = int(len(dados) / 7)
                print(contAtivos, i, ':R$', valorAtivo, 'DY', dividendYield)
                #print('dados:', dados)
                print('linhas:', linhas)
            else:
                print('O ativo nao existe!')

        contAtivos += 1

    time.sleep(10)

horaFim = horaInicio - datetime.datetime.now()
print('Tempo de execução:', horaFim)
print('\nLista de ativos com erros:', listaAtivosError)
print('\nAtivos com erros:', contError)