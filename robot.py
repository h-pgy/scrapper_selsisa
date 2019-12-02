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
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, id_element)))

    def _wait_hierarquia(self, driver):

        self._wait_login(driver, 'ctl00_Principal_lblNmHierarquia')

    def _wait_usuario(self, driver):

        self._wait_login(driver, 'ctl00_Principal_lblNmUsuario')

    def login(self, driver, senha, usuario):
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
