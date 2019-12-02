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

    def gerar_sopa(self, driver):
        '''Gera um beautiful soup com o html da pagina
        que esta aberta no driver'''

        soup = BeautifulSoup(driver.page_source)

        return soup

    def pegar_header(self, driver):
        '''Funcao que extrai o header do relatorio'''

        sopa = self.gerar_sopa(driver)
        parsed = []
        ancora = soup.find(text='Unidade')
        header = ancora.parent.parent.parent
        for div in header.find_all('div'):
            parsed.append(div.text)
        return parsed


