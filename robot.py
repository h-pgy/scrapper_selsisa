from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
from collections import OrderedDict

class BaseRobot:

    def _wait_login(self, driver, id_element):
        '''Abstrai as esperas necessarias para o login'''

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, id_element)))

    def _wait_hierarquia(self, driver):
        '''Espera o sistema buscar e validar a hierarquia na tela de login'''

        self._wait_login(driver, 'ctl00_Principal_lblNmHierarquia')

    def _wait_usuario(self, driver):
        '''Espera o sistema buscar e validar o usuario na tela de login'''

        self._wait_login(driver, 'ctl00_Principal_lblNmUsuario')

    def login(self, driver, senha, usuario):
        '''Realiza o processo de login'''

        driver.get('http://web4.prodam/sd0241_spmf/forms/frmLogin.aspx')

        hierarquia = driver.find_element_by_name('ctl00$Principal$txtHierarquia')
        user = driver.find_element_by_name('ctl00$Principal$txtUsuario')
        passw = driver.find_element_by_name('ctl00$Principal$txtSenha')

        hierarquia.send_keys('selsisa')
        user.click()
        self._wait_hierarquia(driver)
        user.send_keys(usuario)
        passw.click()
        self._wait_usuario(driver)
        passw.send_keys(senha)
        botao_ok = driver.find_element_by_name('ctl00$Principal$btnLogin')
        botao_ok.click()

    def entrar_menu_relatorio(self, driver):
        '''Entra no menu de Relatório do sistema, na pagina após o login'''

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'navigation')))
        menu = driver.find_element_by_id('navigation')
        head = menu.find_element_by_class_name('head')
        head.click()

    def entrar_relatorio_aprovados(self, driver):
        '''Seleciona o relatorio de alvaras aprovados e entra na pagina dele'''

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'navigation')))
        menu = driver.find_element_by_id('navigation')
        head = menu.find_element_by_class_name('head')
        action = ActionChains(driver)
        action.move_to_element(head).perform()
        items_menu = menu.find_elements_by_tag_name('li')
        aprovados = items_menu[1]
        action.move_to_element(aprovados).perform()
        aprovados.click()

    def preencher_datas(self, driver, data_inici, data_final):
        '''Preenche as datas e clica para gerar o relatorio para este periodo'''

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'ctl00_Principal_txtDtInicial')))
        inicial = driver.find_element_by_id('ctl00_Principal_txtDtInicial')
        final = driver.find_element_by_id('ctl00_Principal_txtDtFinal')
        botao_consulta = driver.find_element_by_id('ctl00_Principal_btnConsultar')
        inicial.send_keys(data_inici)
        final.send_keys(data_final)

        botao_consulta.click()

    def mudar_para_relatorio(self, driver, max_tentativas):
        '''Muda para a janela de popup do relatorio, com um maximo de X tentativas'''

        tentativas = 0
        while tentativas < max_tentativas:
            try:
                janela_relatorio = driver.window_handles[1]
                driver.switch_to.window(janela_relatorio)
                break
            except IndexError:
                tentativas += 1
                print(tentativas)
                time.sleep(1)
        if tentativas >= max_tentativas:
            raise RuntimeError('Maximo de tentativas para abrir a janela do relatorio')

    def esperar_dados_aparecerem(self, driver):
        '''Metodo para esperar os dados aparecerem no pop up de relatorio'''

        id_dados = 'ReportViewer1_ctl05'
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, id_dados)))


    def proxima_pagina(self, driver):
        '''Muda de pagina dentro do pop up do relatorio (next page)'''

        id_botao_next = 'ReportViewer1_ctl05_ctl00_Next_ctl00_ctl00'
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, id_botao_next)))
        botao_next = driver.find_element_by_id(id_botao_next)
        botao_next.click()

    def total_paginas(self, driver):
        '''Obtem o total de paginas do relatorio'''

        id_total_pag = 'ReportViewer1_ctl05_ctl00_TotalPages'
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, id_total_pag)))
        total_pag = driver.find_element_by_id(id_total_pag)
        total_pag = int(total_pag.text)

        return total_pag

    def pegar_num_pag_atual(self, driver):
        '''Obtem o numero de pagina atual no pop up do relatorio'''

        input_pag = driver.find_element_by_name('ReportViewer1$ctl05$ctl00$CurrentPage')
        num_pag = input_pag.get_attribute('value')

        return int(num_pag)

    def gerar_sopa(self, driver):
        '''Gera um beautiful soup com o html da pagina
        que esta aberta no driver'''

        soup = BeautifulSoup(driver.page_source)

        return soup

    def pegar_header(self, driver):
        '''Extrai o header do relatorio'''

        sopa = self.gerar_sopa(driver)
        parsed = []
        ancora = sopa.find(text='Unidade')
        header = ancora.parent.parent.parent
        for div in header.find_all('div'):
            parsed.append(div.text)
        return parsed

    def pegar_tabela(self, sopa):
        '''Pega o elemento da tabela com os dados da pagina
        de relatorio'''

        #a pagina contem 5 milhoes de tabelas, a tabela de dados eh a 38
        table = sopa.find_all('table')[38]

        return table

    def pegar_table_rows(self, tabela):
        '''Extrai as linhas da tabela de dados'''

        trs = tabela.find_all('tr')[1:]

        return trs

    def parsear_table_rows(self, tamanho_linha, trs):
        '''Extrai as linhas da tabela, no formato de uma lista
        de listas em que cada lista interna representa uma linha'''

        rows = []
        new_row = []
        count = 0
        for tr in trs:
            tds = tr.find_all('td')[1:]
            for td in tds:
                div = td.find('div')
                if div:
                    content = div.text.strip()
                else:
                    content = ''
                new_row.append(content)
                count += 1
                if count != 0 and count % tamanho_linha == 0:
                    rows.append(new_row)
                    new_row = []
        return rows

    def parsear_pagina(self, driver, tamanho_linha):
        '''Parseia os dados da pagina de relatorio, em excecao
        do header que soh aparece na primeira pagina'''

        sopa = gerar_sopa(driver)
        tabela = pegar_tabela(sopa)
        rows = pegar_table_rows(tabela)
        pag = parsear_table_rows(tamanho_linha, rows)

        return pag

    def parsear_todas_paginas(self, driver):
        '''Pega todas as paginas de um determinado relatorio e retorna
        a lista com os nomes das colunas e uma lista de listas com as
        linhas (dados)'''

        data = []
        total_pag = self.total_paginas(driver)
        header = self.pegar_header(driver)
        tamanho_linha = len(header)
        for i in range(total_pag):

            pag_atual = self.pegar_num_pag_atual(driver)
            assert i == pag_atual
            linhas = self.parsear_pagina(driver, tamanho_linha)
            data.extend(linhas)

        return header, data





