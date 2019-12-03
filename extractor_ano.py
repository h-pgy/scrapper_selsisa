from collections import OrderedDict
from robot import BaseRobot

class ExtratorAno(BaseRobot):

    def __init__(self, driver, ano):

        self.driver = driver
        self.ano = ano
        self.periodos = self.gerar_periodos(self.ano)

    def pegar_fim_meses(self, ano):

        bissextos = ['1904',
                     '1908',
                     '1912',
                     '1916',
                     '1920',
                     '1924',
                     '1928',
                     '1932',
                     '1936',
                     '1940',
                     '1944',
                     '1948',
                     '1952',
                     '1956',
                     '1960',
                     '1964',
                     '1968',
                     '1972',
                     '1976',
                     '1980',
                     '1984',
                     '1988',
                     '1992',
                     '1996',
                     '2000',
                     '2004',
                     '2008',
                     '2012',
                     '2016',
                     '2020',
                     '2024']

        is_bissexto = ano in bissextos
        if is_bissexto:
            fev = '29'
        else:
            fev = '28'
        meses = OrderedDict({
            '01': '31',
            '02': fev,
            '03': '31',
            '04': '30',
            '05': '31',
            '06': '30',
            '07': '31',
            '08': '31',
            '09': '30',
            '10': '31',
            '11': '30',
            '12': '31'}
        )

        if is_bissexto:
            meses['02'] = '29'

        return meses

    def gerar_periodos(self, ano):

        fim_meses = self.pegar_fim_meses(ano)
        periodos = []
        for mes, fim in fim_meses.items():
            data_ini = f'01/{mes}/{ano}'
            data_fim = f'{fim}/{mes}/{ano}'
            period = (data_ini, data_fim)
            periodos.append(period)

        return periodos

    def extrair_ano(self, periodos = None):

        if periodos is None:
            periodos = self.periodos

        dados = []
        for dt_ini, dt_fim in periodos:
            print(dt_ini)
            df = robo.extrair_dados_periodo(driver, dt_ini, dt_fim)
            dados.append(df)

        return pd.concat(dados)