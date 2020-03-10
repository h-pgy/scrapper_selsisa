from config import usuario, chromedriver_path
import os
from extractor_ano import ExtratorAno
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def gerar_driver(headless):

    if headless:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(chromedriver_path, options = chrome_options)
    else:
        driver = webdriver.Chrome(chromedriver_path)

    return driver

def checar_path(path_dados):

    if not os.path.exists(path_dados):
        os.mkdir(path_dados)

def range_padrao(anos):

    if anos is None:
        anos = range(1999, 2020)

    return anos

def extrair_ano(driver, ano):

    ano = str(ano)
    robo = ExtratorAno(driver, ano, usuario['login'], usuario['senha'])
    df_ano = robo()

    return df_ano

def salvar_csv(df, ano, path_dados):

    nom_arquivo = f'{ano}_aprovacoes_selsisa.csv'
    path_arquivo = os.path.join(path_dados, nom_arquivo)
    df.to_csv(path_arquivo, sep = ';', encoding = 'latin-1')

def extrair(anos = None, path_dados = 'dados', headless = True):

    checar_path(path_dados)
    driver = gerar_driver(headless)
    range_anos = range_padrao(anos)


    for ano in range_anos:

        print(f'Extraindo ano {ano}')
        df_ano = extrair_ano(driver, ano)
        salvar_csv(df_ano, ano, path_dados)
        print(f'Ano {ano} finalizado.')

    print('Todos os anos extraidos')

if __name__ == '__main__':

    extrair(['2020'], 'dados_fev_2020')



