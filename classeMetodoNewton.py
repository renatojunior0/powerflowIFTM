import cmath as cmt
import math as mt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class Newton:
    def __init__(self):
        self.__valorBaseS = 100e6 #Potência Aparente de 100MEGA
        self.count = 0
        self.__dadosBarras = dict()
        self.__ligacoesSistema = dict()
        self.__CalBarrasEspecf = dict()
        self.__PotenciasBarraS = dict()
        self.__SalvarTensoes = dict()
        self.__SalvarCorrentes = dict()
        self.__FluxoPotenciaAparente = dict()
        self.__PerdasSistema = 0
        self.__matrizYBus = []
        self.__MatrizJ1 = []
        self.__MatrizJ2 = []
        self.__MatrizJ3 = []
        self.__MatrizJ4 = []
        self.__MatrizJacobiana = []
        self.__plotagemTensao = dict()
        self.__plotagemAngulo = dict()
        self.__qtdBarrasPQ = int()
        self.__qtdBarrasPV = int()
        self.__resultadoEQ = []
        self.__listaBarrasTensoes = []
        self.__listaBarrasAngulos = []
        self.__CalculoPotenciasInjetadas = dict()
        self.__deltaPQ = []
        self.__ResiduosPotAtiva = []
        self.__ResiduosPotReativa = []

    
    def setBarrasSistema(self, barra, codigo, tensao, angulo, carga, geracao):
        """
        Código: 1 -> Tensão e Ângulo;
                2 -> P e Q;
                3 -> P e V.
        
        Ângulo -> Graus.
        Tensão -> pu
        Carga e Geração -> VA
        """
        self.__dadosBarras[barra] = {'codigo': codigo, 'tensao' : tensao, 'angulo' : mt.radians(angulo), 'carga' : (carga / self.__valorBaseS), 'geracao' : geracao / (self.__valorBaseS)}

        self.__plotagemTensao[barra] = [tensao]
        self.__plotagemAngulo[barra] = [angulo]

    def mostrarBarras(self):
        """
        Método para amostragem de informações na tela do software
        """
        print('\n\n####################### IMPLEMENTAÇÃO DO SOFTWARE: #######################')
        print('####################### REDE IFTM/CAUPT - UNIDADE 1: #####################')
        print('Valor Base S (Potência Aparente) = ', self.__valorBaseS, 'VA')
        
        for i in self.__dadosBarras:  
            print(self.__dadosBarras[i])
        print('\n\n########################################################################')

    def setCalBarrasEspecf(self):
        """ MÉTODO PARA CÁLCULO DE POTÊNCIA ESPECIFICADA NAS BARRAS
        Este método permite calcular a potência especificada em cada uma das barras. Os valores são calculados
        automaticamente.
        """
        for i in self.__dadosBarras:
            if self.__dadosBarras[i]['codigo'] == 2: #BARRAS PQ
                self.__CalBarrasEspecf[i] = {   'Potência Ativa' : np.real(self.__dadosBarras.get(i)['geracao'] - self.__dadosBarras.get(i)['carga']),
                                                'Potência Reativa' : float(
                                                    np.imag(self.__dadosBarras.get(i)['geracao'] - self.__dadosBarras.get(i)['carga'])
                                                    )}
            elif self.__dadosBarras[i]['codigo'] == 3: #BARRAS PV
                self.__CalBarrasEspecf[i] = {   'Potência Ativa' : np.real(self.__dadosBarras.get(i)['geracao'] - self.__dadosBarras.get(i)['carga']),
                                                'Potência Reativa' : float(
                                                    np.imag(self.__dadosBarras.get(i)['geracao'] - self.__dadosBarras.get(i)['carga'])
                                                    )} 
                                                    
        print('\n\n####################### POTÊNCIA APARENTE ESPECIFICADA:#######################')
        print(self.__CalBarrasEspecf, 'pu')
        print('\n\n##############################################################################')

    def ligacoesBarras(self, barra1, barra2, impedancia = None, admitancia = None):
        """ LIGAÇÕES DAS BARRAS DO SISTEMA
        AS INFORMAÇÕES DEVEM SEMPRE ESTAR EM PU.
        """
        if impedancia is None:
            impedancia = 1 / admitancia
        elif admitancia is None:
            admitancia = 1 / impedancia
        else:
            return 'ERRO: FAVOR INFORMAR A ADMITÂNCIA OU IMPEDÂNCIA DO SISTEMA!!!'
        
        self.__ligacoesSistema[(barra1, barra2)] = {    'Impedância' : impedancia,
                                                        'Admitância' : admitancia}

    def mostrarLigacoes(self):
        """
        MÉTODO PARA AMOSTRAGEM DE INFORMAÇÕES NA TELA DO SOFTWARE REFERENTE AS LIGAÇÕES DAS BARRAS
        """
        print('\n\n########################## LIGAÇÕES DAS BARRAS: ####################################')
        print('Valor Base S (Potência Aparente) = ', self.__valorBaseS, 'VA')
        
        for i in self.__ligacoesSistema:  
            print('Ligação ', i, '\t', self.__ligacoesSistema[i])
        print('####################################################################################')
    
    def __mostrarMatrizYBus(self):
        """
        MÉTODO PARA AMOSTRAGEM DE INFORMAÇÕES NA TELA DO SOFTWARE REFERENTE A MATRIZ DE ADMITÂNCIA YBUS
        """
        print('\n\n########################## MATRIZ DE ADMITÂNICIA YBUS: #############################')
        for i in self.__matrizYBus: 
            print(i) 
        print('####################################################################################')

    def matrizAdmitanciaYBus(self):
        """
        MÉTODO PARA REALIZAR O CÁLCULO DA MATRIZ DE ADMITÂNCIA YBUS
        """
        self.__matrizYBus = np.ones((len(self.__dadosBarras), len(self.__dadosBarras)), dtype=complex)

        for i in range(len(self.__matrizYBus)):
            listaCalculos = []
            for j in range(len(self.__matrizYBus)):
                if i == j:
                    listaCalculos.append(0)
                else:
                    if self.__ligacoesSistema.__contains__(tuple([i + 1, j + 1])):
                        listaCalculos.append(-self.__ligacoesSistema.get(tuple([i + 1, j + 1]))['Admitância'])
                    elif self.__ligacoesSistema.__contains__(tuple([j + 1, i + 1])):
                        listaCalculos.append(-self.__ligacoesSistema.get(tuple([j + 1, i + 1]))['Admitância'])
                    else:
                        listaCalculos.append(0)
            for j in range(len(self.__matrizYBus)):
                if i == j:
                    listaCalculos[j] = -1 * sum(listaCalculos)

            self.__matrizYBus[i] = listaCalculos    
        
        self.__mostrarMatrizYBus()

        for i in self.__dadosBarras:
            if self.__dadosBarras.get(i)['codigo'] == 2:
                self.__qtdBarrasPQ += 1
            elif self.__dadosBarras.get(i)['codigo'] == 3:
                self.__qtdBarrasPV += 1

    def CalculoPotenciasInjetadas(self):
        """ MÉTODO PARA CÁLCULO DE POTÊNCIAS INJETADAS NO SISTEMA
        Este método permite calcular a potência injetada no sistema.
        """
        self.__CalculoPotenciasInjetadas = dict()
        self.__deltaPQ = []
        self.__ResiduosPotAtiva = []
        self.__ResiduosPotReativa = []

        for i in self.__dadosBarras:
            somarPotenciasAtivas = []
            somarPotenciasReativas = []
            if self.__dadosBarras[i]['codigo'] != 1:
                for j in self.__dadosBarras:
                    somarPotenciasAtivas.append(
                            abs(self.__matrizYBus[i - 1][j - 1]) *
                            abs(self.__dadosBarras.get(i)['tensao']) * 
                            abs(self.__dadosBarras.get(j)['tensao']) *
                            mt.cos(np.angle(self.__matrizYBus[i - 1][j - 1]) 
                            - self.__dadosBarras.get(i)['angulo']
                            + self.__dadosBarras.get(j)['angulo'])
                    )
                    somarPotenciasReativas.append(
                            - abs(self.__matrizYBus[i - 1][j - 1]) *
                            abs(self.__dadosBarras.get(i)['tensao']) * 
                            abs(self.__dadosBarras.get(j)['tensao']) *
                            mt.sin(np.angle(self.__matrizYBus[i - 1][j - 1]) 
                            - self.__dadosBarras.get(i)['angulo']
                            + self.__dadosBarras.get(j)['angulo']) * 1j
                    )
                self.__ResiduosPotAtiva.append(
                    np.real(
                        self.__CalBarrasEspecf.get(i)['Potência Ativa'] - sum(somarPotenciasAtivas)
                    )
                )
                if self.__dadosBarras[i]['codigo'] == 2:
                    self.__ResiduosPotReativa.append(
                        np.imag(
                            self.__CalBarrasEspecf.get(i)['Potência Reativa'] * 1j - sum(somarPotenciasReativas)
                        )
                    )
        for i in range(len(self.__ResiduosPotAtiva)):
            self.__deltaPQ.append(self.__ResiduosPotAtiva[i])
        for i in range(len(self.__ResiduosPotReativa)):
            self.__deltaPQ.append(self.__ResiduosPotReativa[i])

        # for i in self.__deltaPQ:
        #     print('\n',i)
        print('\n ######################### DELTA P e DELTA Q ###########################')
        for i in range(len(self.__ResiduosPotAtiva)):
            print('DELTA P = ',self.__ResiduosPotAtiva[i])
        for i in range(len(self.__ResiduosPotReativa)):
            print('DELTA Q = ',self.__ResiduosPotReativa[i])
        print('\n #######################################################################')

    
    def __setSubMatrizJ1(self, listaAngulos, qtdBarrasPQ, qtdBarrasPV):
        """ MÉTODO PARA CÁLCULO DA SUBMATRIZ JACOBIANA J1
            listaAngulos   -> Lista de Ângulos calculados no circuito (Barras PQ e PV)
            qtdBarrasPQ    -> Quantidade de Barras PQ.
            qtdBarrasPV:   -> Quantidade de Barras PV. 
            Retorno Função -> SubMatriz Jacobiana J1.
        """

        self.__MatrizJ1 = np.ones((qtdBarrasPQ + qtdBarrasPV, qtdBarrasPQ + qtdBarrasPV))

        dentroDiagonalPrincipal = []
        foraDiagonalPrincipal = []

        for i in listaAngulos:
            somatorio = []
            for j in range(1, len(self.__dadosBarras) + 1, 1):
                if i != j:
                   somatorio.append(
                        abs(self.__matrizYBus[i - 1][j - 1]) * 
                        abs(self.__dadosBarras.get(i)['tensao']) *
                        abs(self.__dadosBarras.get(j)['tensao']) *
                        cmt.sin(cmt.phase(self.__matrizYBus[i - 1][j - 1]) -
                            self.__dadosBarras.get(i)['angulo'] + 
                            self.__dadosBarras.get(j)['angulo']
                       )
                   )
            dentroDiagonalPrincipal.append(sum(somatorio))

        for i in listaAngulos:
            for j in listaAngulos:
                if i != j:
                    foraDiagonalPrincipal.append(
                        -abs(self.__matrizYBus[i - 1][j - 1]) * 
                        abs(self.__dadosBarras.get(i)['tensao']) *
                        abs(self.__dadosBarras.get(j)['tensao']) *
                        cmt.sin(cmt.phase(self.__matrizYBus[i - 1][j - 1]) -
                            self.__dadosBarras.get(i)['angulo'] + 
                            self.__dadosBarras.get(j)['angulo']
                       )
                   ) 
        cont = 0
        
        for i in range(len(listaAngulos)):
            for j in range(len(listaAngulos)):
                if i == j:
                    self.__MatrizJ1[i][j] = np.real(dentroDiagonalPrincipal[j])
                else:
                    self.__MatrizJ1[i][j] = np.real(foraDiagonalPrincipal[cont])
                    cont += 1
        
        # print('\nMATRIZ J1 =  \n', self.__MatrizJ1)

        return self.__MatrizJ1

    def __setSubMatrizJ2(self, listaTensoes, listaAngulos, qtdBarrasPQ, qtdBarrasPV):
        """ MÉTODO PARA CÁLCULO DA SUBMATRIZ JACOBIANA J2
            listaTensoes   -> Lista de Tensões calculadas no circuito (Barras PQ e PV)
            listaAngulos   -> Lista de Ângulos calculados no circuito (Barras PQ e PV)
            qtdBarrasPQ    -> Quantidade de Barras PQ.
            qtdBarrasPV:   -> Quantidade de Barras PV. 
            Retorno Função -> SubMatriz Jacobiana J2.
        """

        self.__MatrizJ2 = np.ones((qtdBarrasPQ + qtdBarrasPV, qtdBarrasPQ))

        dentroDiagonalPrincipal = []
        foraDiagonalPrincipal = []

        for i in listaAngulos:
            somatorio = []
            aux = 0
            for j in range(1, len(self.__dadosBarras) + 1, 1):
                if i != j:
                   somatorio.append(
                        abs(self.__matrizYBus[i - 1][j - 1]) * 
                        abs(self.__dadosBarras.get(j)['tensao']) *
                        cmt.cos(cmt.phase(self.__matrizYBus[i - 1][j - 1]) -
                            self.__dadosBarras.get(i)['angulo'] + 
                            self.__dadosBarras.get(j)['angulo']
                       )
                   )
            aux = (2 * abs(self.__dadosBarras.get(i)['tensao']) * abs(self.__matrizYBus[i - 1][i - 1]) * 
                   cmt.cos(cmt.phase(self.__matrizYBus[i - 1][i - 1])))

            dentroDiagonalPrincipal.append(aux + sum(somatorio))

        for i in listaAngulos:
            for j in listaTensoes:
                if i != j:
                    foraDiagonalPrincipal.append(
                        abs(self.__matrizYBus[i - 1][j - 1]) * 
                        abs(self.__dadosBarras.get(i)['tensao']) *
                        cmt.cos(cmt.phase(self.__matrizYBus[i - 1][j - 1]) -
                            self.__dadosBarras.get(i)['angulo'] + 
                            self.__dadosBarras.get(j)['angulo']
                       )
                   ) 
        cont = 0
        
        for i in range(qtdBarrasPQ + qtdBarrasPV):
            auxPV = qtdBarrasPV
            for j in range(qtdBarrasPQ):
                if i < qtdBarrasPV:
                    self.__MatrizJ2[i][j] = np.real(foraDiagonalPrincipal[cont])
                    cont += 1
                elif i >= qtdBarrasPV:
                    if i - qtdBarrasPV == j:
                        self.__MatrizJ2[i][j] = np.real(dentroDiagonalPrincipal[j + qtdBarrasPV])
                        auxPV += 1
                    else:
                        self.__MatrizJ2[i][j] = np.real(foraDiagonalPrincipal[cont])
                        cont += 1
        print('\nauxPV = ', auxPV, '\n')
        # print('\nMatriz J2 = \n', self.__MatrizJ2)

        return self.__MatrizJ2

    def __setSubMatrizJ3(self, listaTensoes, listaAngulos, qtdBarrasPQ, qtdBarrasPV):
        """ MÉTODO PARA CÁLCULO DA SUBMATRIZ JACOBIANA J3
            listaTensoes   -> Lista de Tensões calculadas no circuito (Barras PQ e PV)
            listaAngulos   -> Lista de Ângulos calculados no circuito (Barras PQ e PV)
            qtdBarrasPQ    -> Quantidade de Barras PQ.
            qtdBarrasPV:   -> Quantidade de Barras PV. 
            Retorno Função -> SubMatriz Jacobiana J3.
        """

        self.__MatrizJ3 = np.ones((qtdBarrasPQ, qtdBarrasPQ + qtdBarrasPV))
 
        dentroDiagonalPrincipal = []
        foraDiagonalPrincipal = []

        for i in listaAngulos:
            somatorio = []
            for j in range(1, len(self.__dadosBarras) + 1, 1):
                if i != j:
                   somatorio.append(
                        abs(self.__matrizYBus[i - 1][j - 1]) * 
                        abs(self.__dadosBarras.get(i)['tensao']) *
                        abs(self.__dadosBarras.get(j)['tensao']) *
                        cmt.cos(cmt.phase(self.__matrizYBus[i - 1][j - 1]) -
                            self.__dadosBarras.get(i)['angulo'] + 
                            self.__dadosBarras.get(j)['angulo']
                       )
                   )

            dentroDiagonalPrincipal.append(sum(somatorio))

        for i in listaAngulos:
            for j in listaTensoes:
                if i != j:
                    foraDiagonalPrincipal.append(
                        -abs(self.__matrizYBus[i - 1][j - 1]) * 
                        abs(self.__dadosBarras.get(i)['tensao']) *
                        abs(self.__dadosBarras.get(j)['tensao']) *
                        cmt.cos(cmt.phase(self.__matrizYBus[i - 1][j - 1]) -
                            self.__dadosBarras.get(i)['angulo'] + 
                            self.__dadosBarras.get(j)['angulo']
                       )
                   ) 

        cont = 0
        for i in range(qtdBarrasPQ):
            #auxPV = qtdBarrasPV
            for j in range(qtdBarrasPQ + qtdBarrasPV):
                if j < qtdBarrasPV:
                    self.__MatrizJ3[i][j] = np.real(foraDiagonalPrincipal[cont])
                    cont += 1
                elif j >= qtdBarrasPV:
                    if j - qtdBarrasPV == i:
                        self.__MatrizJ3[i][j] = np.real(dentroDiagonalPrincipal[i + qtdBarrasPV])
                        #auxPV += 1
                    else:
                        self.__MatrizJ3[i][j] = np.real(foraDiagonalPrincipal[cont])
                        cont += 1
        #print('\nauxPV = ', auxPV, '\n')
        # print('\nMatriz J3 = \n', self.__MatrizJ3)

        return self.__MatrizJ3

    def __setSubMatrizJ4(self, listaTensoes, listaAngulos, qtdBarrasPQ, qtdBarrasPV):
        """ MÉTODO PARA CÁLCULO DA SUBMATRIZ JACOBIANA J4
            listaTensoes   -> Lista de Tensões calculadas no circuito (Barras PQ e PV)
            listaAngulos   -> Lista de Ângulos calculados no circuito (Barras PQ e PV)
            qtdBarrasPQ    -> Quantidade de Barras PQ.
            qtdBarrasPV:   -> Quantidade de Barras PV. 
            Retorno Função -> SubMatriz Jacobiana J4.
        """

        self.__MatrizJ4 = np.ones((qtdBarrasPQ, qtdBarrasPQ))

        dentroDiagonalPrincipal = []
        foraDiagonalPrincipal = []

        for i in listaAngulos:
            somatorio = []
            aux = 0
            for j in range(1, len(self.__dadosBarras) + 1, 1):
                if i != j:
                   somatorio.append(
                        abs(self.__matrizYBus[i - 1][j - 1]) * 
                        abs(self.__dadosBarras.get(j)['tensao']) *
                        cmt.sin(cmt.phase(self.__matrizYBus[i - 1][j - 1]) -
                            self.__dadosBarras.get(i)['angulo'] + 
                            self.__dadosBarras.get(j)['angulo']
                       )
                   )
            aux = (2 * abs(self.__dadosBarras.get(i)['tensao']) * abs(self.__matrizYBus[i - 1][i - 1]) * 
                   cmt.sin(cmt.phase(self.__matrizYBus[i - 1][i - 1])))

            dentroDiagonalPrincipal.append(-aux - sum(somatorio))

        for i in listaAngulos:
            for j in listaTensoes:
                if i != j:
                    foraDiagonalPrincipal.append(
                        -abs(self.__matrizYBus[i - 1][j - 1]) * 
                        abs(self.__dadosBarras.get(i)['tensao']) *
                        cmt.sin(cmt.phase(self.__matrizYBus[i - 1][j - 1]) -
                            self.__dadosBarras.get(i)['angulo'] + 
                            self.__dadosBarras.get(j)['angulo']
                       )
                   )

        cont = 0
        for i in range(qtdBarrasPQ):
            for j in range(qtdBarrasPQ):
                if i == j:
                    self.__MatrizJ4[i][j] = np.real(dentroDiagonalPrincipal[j + qtdBarrasPV])
                    #cont += 1
                else:
                    self.__MatrizJ4[i][j] = np.real(foraDiagonalPrincipal[cont])
                    cont += 1
        #print('\nauxPV = ', auxPV, '\n')
        # print('\nMatriz J4 = \n', self.__MatrizJ4)

        return self.__MatrizJ4

    def setMatrizJacobiana(self, listaBarrasTensoes, listaBarrasAngulos):
        """ MÉTODO PARA CÁLCULO DA MATRIZ JACOBIANA
            listaTensoes   -> Lista de Tensões calculadas no circuito (Barras PQ e PV)
            listaAngulos   -> Lista de Ângulos calculados no circuito (Barras PQ e PV)
            qtdBarrasPQ    -> Quantidade de Barras PQ.
            qtdBarrasPV:   -> Quantidade de Barras PV. 
            Retorno Função -> Matriz Jacobiana.
        """
        self.__MatrizJacobiana = []
        self.__listaBarrasTensoes = listaBarrasTensoes
        self.__listaBarrasAngulos = listaBarrasAngulos
        matrizNxN = len(listaBarrasTensoes) + len(listaBarrasAngulos)

        matrizJ1 = self.__setSubMatrizJ1(listaBarrasAngulos,self.__qtdBarrasPQ, self.__qtdBarrasPV)
        matrizJ2 = self.__setSubMatrizJ2(listaBarrasTensoes,listaBarrasAngulos, self.__qtdBarrasPQ, self.__qtdBarrasPV)
        matrizJ3 = self.__setSubMatrizJ3(listaBarrasTensoes,listaBarrasAngulos, self.__qtdBarrasPQ, self.__qtdBarrasPV)
        matrizJ4 = self.__setSubMatrizJ4(listaBarrasTensoes,listaBarrasAngulos, self.__qtdBarrasPQ, self.__qtdBarrasPV)

        self.__MatrizJacobiana = np.zeros((matrizNxN, matrizNxN))

        for i in range(matrizNxN):
            auxMatrizesJ1J2 = []
            auxMatrizesJ3J4 = []
            if i < len(matrizJ1):
                for j in range(len(matrizJ1[i])): auxMatrizesJ1J2.append(matrizJ1[i][j])
                for j in range(len(matrizJ2[i])): auxMatrizesJ1J2.append(matrizJ2[i][j])
                self.__MatrizJacobiana[i] = np.hstack(auxMatrizesJ1J2)
            elif i  >= len(matrizJ1):
                aux = i - len(matrizJ1)
                for j in range(len(matrizJ3[aux])): auxMatrizesJ3J4.append(matrizJ3[aux][j])
                for j in range(len(matrizJ4[aux])): auxMatrizesJ3J4.append(matrizJ4[aux][j])
                self.__MatrizJacobiana[i] = np.hstack(auxMatrizesJ3J4)

        print('\n\n########################## MATRIZ JACOBIANA: #####################################')
        print('\n Matriz J1 = ')
        for i in matrizJ1:
            print(i)
        print('\n Matriz J2 = ')
        for i in matrizJ2: 
            print(i) 
        print('\n Matriz J3 = ')
        for i in matrizJ3: 
            print(i) 
        print('\n Matriz J4 = ')
        for i in matrizJ4: 
            print(i)
        print('\n Matriz JACOBIANA = ')
        for i in self.__MatrizJacobiana: 
            print(i)    
        print('\n##################################################################################')

    def SistemaLinear(self):
        """ 
        MÉTODO PARA CÁLCULO DOS RESULTADOS DO SISTEMA LINEAR
        [DELTA P DELTA Q] = [JACOBIANA] . [RESULTADOEQ]
        """
        self.__resultadoEQ = []
        self.__resultadoEQ = np.linalg.solve(self.__MatrizJacobiana, self.__deltaPQ)
        resultadoDeuCerto = np.allclose(np.dot(self.__MatrizJacobiana, self.__resultadoEQ), self.__deltaPQ)
        print('\n\tO SISTEMA LINEAR FOI CALCULADO CORRETAMENTE?', resultadoDeuCerto)

        angulo = []
        tensao = []
        for i in range(len(self.__resultadoEQ)):
            if i < (self.__qtdBarrasPQ + self.__qtdBarrasPV):
                angulo.append(self.__resultadoEQ[i])
            else:
                tensao.append(self.__resultadoEQ[i])
        cont = 0
        for i in range(len(self.__dadosBarras)):
            if self.__dadosBarras.get(i + 1)['codigo'] != 1:
                self.__dadosBarras[i + 1]['angulo'] += float(np.real(angulo[cont]))
                self.__plotagemAngulo[i + 1].append(self.__dadosBarras[i + 1]['angulo'])
                cont += 1
        cont = 0
        for i in range(len(self.__dadosBarras)):
            if self.__dadosBarras.get(i + 1)['codigo'] == 2:
                self.__dadosBarras[i + 1]['tensao'] += float(np.real(tensao[cont]))
                self.__plotagemTensao[i + 1].append(self.__dadosBarras[i + 1]['tensao'])
                cont += 1
    
    def NovaInjecaoPotencia(self):
        """ 
            MÉTODO PARA CÁLCULO DOS RESULTADOS DE NOVOS VALORES DE 
            INJEÇÃO DE POTÊNCIA APARENTE NAS BARRAS DE FOLGA (SLACKBUS) E PV.
            [P e Q NAS BARRAS DE FOLGA e Q NAS PV]
        """
        self.__PotenciasBarraS = dict()

        for i in self.__dadosBarras:
            somarPotenciasAtivas = []
            somarPotenciasReativas = []
            if self.__dadosBarras[i]['codigo'] != 2:
                for j in self.__dadosBarras:
                    somarPotenciasAtivas.append(
                            abs(self.__matrizYBus[i - 1][j - 1]) *
                            abs(self.__dadosBarras.get(i)['tensao']) * 
                            abs(self.__dadosBarras.get(j)['tensao']) *
                            mt.cos(np.angle(self.__matrizYBus[i - 1][j - 1]) 
                            - self.__dadosBarras.get(i)['angulo']
                            + self.__dadosBarras.get(j)['angulo'])
                    )
                    somarPotenciasReativas.append(
                            - abs(self.__matrizYBus[i - 1][j - 1]) *
                            abs(self.__dadosBarras.get(i)['tensao']) * 
                            abs(self.__dadosBarras.get(j)['tensao']) *
                            mt.sin(np.angle(self.__matrizYBus[i - 1][j - 1]) 
                            - self.__dadosBarras.get(i)['angulo']
                            + self.__dadosBarras.get(j)['angulo']) * 1j
                    )
            if self.__dadosBarras[i]['codigo'] == 1:
                self.__PotenciasBarraS[i] = {'P' : np.real(sum(somarPotenciasAtivas)), 'Q' : np.imag(sum(somarPotenciasReativas))}
            elif self.__dadosBarras[i]['codigo'] == 3:
                self.__PotenciasBarraS[i] = {'P' : 0, 'Q' : np.imag(sum(somarPotenciasReativas))}
            
        for i in self.__dadosBarras:
            if self.__dadosBarras[i]['codigo'] == 1:
                self.__dadosBarras[i]['geracao'] = self.__PotenciasBarraS.get(i)['P'] + self.__PotenciasBarraS.get(i)['Q'] * 1j
            elif self.__dadosBarras[i]['codigo'] == 3:  
                #self.__dadosBarras[i]['geracao'] = self.__PotenciasBarraS.get(i)['P'] + self.__PotenciasBarraS.get(i)['Q'] * 1j
                self.__dadosBarras[i]['geracao'] = np.real(self.__dadosBarras.get(i)['geracao']) + self.__PotenciasBarraS.get(i)['Q'] * 1j

    def ResolucaoCircuito(self, erro=None, iteracoes=None, listaBarrasTensoes=None, listaBarrasAngulos=None):
        """ 
            MÉTODO PARA RESOLUÇÃO GENÉRICA DO CIRCUITO DE FLUXO DE POTÊNCIA 
            PARÂMETROS UTILIZADOS
            ERRO               -> VALOR DO ERRO UTILIZADO PARA O FIM DAS ITERAÇÕES.
            ITERAÇÕES          -> QUANTIDADE DE VEZES QUE IRÁ REPETIR O CÁLCULO DO FLUXO.
                OBSERVAÇÃO     -> DEVE SER PASSADO COMO PARÂMETRO O ERRO OU O NÚMERO DE ITERAÇÕES.
            LISTABARRASTENSOES -> LISTA DE TENSÕES A SEREM CALCULADAS NO CIRCUITO (BARRAS PQ).
            LISTABARRASANGULOS -> LISTA DE ÂNGULOS A SEREM CALCULADOS NO CIRCUITO (BARRAS PQ e PV).
        """
        self.__listaBarrasTensoes = listaBarrasTensoes
        self.__listaBarrasAngulos = listaBarrasAngulos
        self.count = 1
        self.matrizAdmitanciaYBus()
        self.CalculoPotenciasInjetadas()
        self.setMatrizJacobiana(listaBarrasTensoes=self.__listaBarrasTensoes, listaBarrasAngulos=self.__listaBarrasAngulos)
        self.SistemaLinear()
        if iteracoes is None and erro is not None:
            valorPeQ = list(map(abs, self.__deltaPQ))
            testeComparacao = list(map(lambda compara: True if (compara < erro) else False, valorPeQ))
            paradaSistema = testeComparacao.count(False)
            while True:
                self.CalculoPotenciasInjetadas()
                self.setMatrizJacobiana(listaBarrasTensoes=self.__listaBarrasTensoes, listaBarrasAngulos=self.__listaBarrasAngulos)
                self.SistemaLinear()
                self.count += 1
                valorPeQ = list(map(abs, self.__deltaPQ))
                testeComparacao = list(map(lambda compara: True if (compara < erro) else False, valorPeQ))
                paradaSistema = testeComparacao.count(False)
                if paradaSistema == 0:
                    break
        elif iteracoes is not None and erro is None:
            while self.count < iteracoes:
                self.CalculoPotenciasInjetadas()
                self.setMatrizJacobiana(listaBarrasTensoes=self.__listaBarrasTensoes, listaBarrasAngulos=self.__listaBarrasAngulos)
                self.SistemaLinear()
                self.count += 1
                # valorPeQ = list(map(abs, self.__deltaPQ))
                # testeComparacao = list(map(lambda compara: True if (compara < erro) else False, valorPeQ))
                # paradaSistema = testeComparacao.count(False)
        
        self.NovaInjecaoPotencia()
        if iteracoes is not None:
            print('\n ################### NÚMERO DE ITERAÇÕES = ', self.count)
        elif erro is not None:
            print('\n ################### CONVERGÊNCIA PARA O ERRO = ', erro, ' . ')
            print('\n ################### CONVERGÊNCIA EM ', self.count, ' ITERAÇÕES. ')


    def __mostrarTensao(self):
            print('\n\n########################## TENSÕES: #####################################')
            for i in self.__SalvarTensoes:
                print('BARRA: \t', i, '\tTENSÃO = \t', self.__SalvarTensoes.get(i), '\t[pu]')
            print('#########################################################################')

    def CalculoTensoes(self, print=None):
        """ 
            MÉTODO PARA CÁLCULO DE TENSÕES EM CADA BARRA DO SISTEMA
            O CÁLCULOO DAS TENSÕES É REALIZADO A PARTIR DOS VALORES EM PU E DOS ÂNGULOS DAS MESMAS,
            ÂNGULOS UTILIZADOS DAS ITERAÇÕES DO MÉTODO RESOLUCAOCIRCUITO().
            PARÂMETROS UTILIZADOS
            printTensao  -> PARA MOSTRAR OS VALORES DE TENSÕES EM CADA BARRA DEVE-SE PASSAR TRUE PARA A VARIÁVEL 
        """
        self.__SalvarTensoes = dict()
        for i in self.__dadosBarras:
            self.__SalvarTensoes[i] = cmt.rect( self.__dadosBarras.get(i)['tensao'],
                                                self.__dadosBarras.get(i)['angulo'])
        if print:
            self.__mostrarTensao()

    def __mostrarCorrente(self):
            print('\n\n########################## CORRENTES: #####################################')
            for i in self.__SalvarCorrentes:
                print('LIGAÇÃO: \t', i, '\tCORRENTE = \t', self.__SalvarCorrentes.get(i), '\t[pu]')
            print('#########################################################################')

            
    def CalculoCorrentes(self, print=None):
        """ 
            MÉTODO PARA CÁLCULO DE CORRENTES EM CADA LINHA DO SISTEMA
            O CÁLCULOO DAS CORRENTES É REALIZADO PARA TODAS AS BARRAS DO SISTEMA. PORTANTO, NAS BARRAS EM QUE 
            NÃO HÁ LIGAÇÕES, O RESULTADO DA CORRENTE DEVE SER 0. JÁ AS CORRENTES QUE REPRESENTAM LIGAÇÕES
            COM AS MESMAS BARRAS DO SISTEMA, SEUS VALORES SÃO CALCULADOS COMO O SOMATÓRIO DE TODAS AS CORRENTES
            DA BARRA SOB ANÁLISE.
            AS CORRENTES FORAM CALCULADAS CONSIDERANDO OS ÂNGULOS DAS TENSÕES!!!
            PARÂMETROS UTILIZADOS
            printCorrente  -> PARA MOSTRAR OS VALORES DE CORRENTE EM CADA BARRA DEVE-SE PASSAR TRUE PARA A VARIÁVEL 
        """
        self.__SalvarCorrentes = dict()
        self.CalculoTensoes(print=None)
        for i in self.__dadosBarras:
            somatorio = []
            for j in  self.__dadosBarras:
                if i == j:
                    continue
                else:
                    self.__SalvarCorrentes[(i,j)] = ((self.__SalvarTensoes.get(i) - self.__SalvarTensoes.get(j)) * self.__matrizYBus[i - 1][j - 1])
                somatorio.append(((self.__SalvarTensoes.get(i) - self.__SalvarTensoes.get(j)) * self.__matrizYBus[i - 1][j - 1]))
            self.__SalvarCorrentes[(i,i)] = sum(somatorio)
        if print:
            self.__mostrarCorrente()
    
    def FluxoPotenciaAparente(self, printTensoes=None, printCorrentes=None):
        """ 
            MÉTODO PARA CÁLCULO DO FLUXO DE POTÊNCIA APARENTE EM TODAS AS LIGAÇÕES DO SISTEMA.
            AS CORRENTES FORAM CALCULADAS CONSIDERANDO OS ÂNGULOS DAS TENSÕES!!!
            PARÂMETROS UTILIZADOS
            printTensoes    -> PARA MOSTRAR OS VALORES DE TENSÃO EM CADA BARRA DEVE-SE PASSAR TRUE PARA A VARIÁVEL 
            printCorrentes  -> PARA MOSTRAR OS VALORES DE CORRENTE EM CADA LINHA DEVE-SE PASSAR TRUE PARA A VARIÁVEL 
        """
        self.__FluxoPotenciaAparente = dict()
        self.CalculoTensoes(print=printTensoes)
        self.CalculoCorrentes(print=printCorrentes)

        for i in self.__SalvarCorrentes:
            a = i[0]
            # SINAL NEGATIVO COLOCADO NO CÁLCULO PARA OS RESULTADOS DE POTÊNCIA FICAREM NO "SENTIDO CORRETO".
            self.__FluxoPotenciaAparente[i] = -self.__SalvarTensoes.get(a) * np.conjugate(self.__SalvarCorrentes.get(i))
        
        print('\n######################## FLUXO DE POTÊNCIA: #######################################')
        for i in self.__FluxoPotenciaAparente:
            print('LIGAÇÃO: \t', i, '\tFLUXO DE POTÊNCIA = \t', self.__FluxoPotenciaAparente.get(i), '\t[pu]')
        print('####################################################################################')

        for i in self.__dadosBarras:
             if self.__dadosBarras.get(i)['codigo'] != 2:
                 self.__dadosBarras[i]['geracao'] = self.__FluxoPotenciaAparente.get((i,i))

    def PerdasSistema(self):
        """ 
            MÉTODO PARA CÁLCULO DAS PERDAS DO SISTEMA.
            OS CÁLCULOS SÃO REALIZADOS COM BASE NA SOMA DE TODAS AS POTÊNCIAS DO SISTEMA!!!
        """
        self.__PerdasSistema = 0
        listaPerdas = []
        for i in self.__FluxoPotenciaAparente:
            listaPerdas.append(self.__FluxoPotenciaAparente.get(i))
        self.__PerdasSistema = sum(listaPerdas)
        print('\n######################## PERDAS DO SISTEMA: ##############################')
        print(self.__PerdasSistema, '\t[pu]')

    def __graficoTensao(self):
        """ 
            MÉTODO PARA PLOTAR A CONVERGÊNCIA DA TENSÃO.
        """
        eixoX = self.count
        barras = []
        eixoY = []
        for i in self.__dadosBarras:
            if self.__dadosBarras.get(i)['codigo'] == 2:
                barras.append(i)
        for i in barras:
            eixoY.append(self.__plotagemTensao.get(i))
        for i in range(len(barras)):
            plt.subplot(len(barras), 1, i + 1)
            plt.plot(range(eixoX + 1), eixoY[i])
            #plt.ylim(0, 1)
            #plt.xlim(0, 25)
            plt.title('VARIAÇÃO DA TENSÃO NA BARRA ' + str(barras[i]) + ' X NÚMERO DE ITERAÇÕES')
            plt.xlabel('NÚMERO DE ITERAÇÕES ')
            plt.ylabel('TENSÃO NA BARRA ' + str(barras[i]) + ' [pu]')
            plt.grid(True)
        #plt.subplots(tight_layout=True)
        plt.tight_layout()
        plt.show()

    def __graficoAngulo(self):
        """ 
            MÉTODO PARA PLOTAR A CONVERGÊNCIA DOS ÂNGULOS.
        """
        eixoX = self.count
        barras = []
        eixoY = []
        for i in self.__dadosBarras:
            if self.__dadosBarras.get(i)['codigo'] != 1:
                barras.append(i)
        for i in barras:
            eixoY.append(self.__plotagemAngulo.get(i))
        for i in range(len(barras)):
            plt.subplot(len(barras), 1, i + 1)
            plt.plot(range(eixoX + 1), eixoY[i])
            plt.title('VARIAÇÃO DO ÂNGULO NA BARRA ' + str(barras[i]) + ' X NÚMERO DE ITERAÇÕES')
            plt.xlabel('NÚMERO DE ITERAÇÕES')
            plt.ylabel('ÂNGULO NA BARRA ' + str(barras[i]) + ' [rad]')
            plt.grid(True)
        #plt.subplots(constrained_layout=True)
        plt.tight_layout()
        plt.show()

    def graficoDados(self, tensao=None, angulo=None):
        """ 
            MÉTODO PARA PLOTAR A CONVERGÊNCIA DAS TENSÕES E DOS ÂNGULOS CALCULADOS PELO SISTEMA.
            PARÂMETROS UTILIZADOS
            tensao -> PARA PLOTAR OS VALORES DE TENSÃO, DEVE-SE PASSAR TRUE PARA A VARIÁVEL 
            angulo -> PARA MOSTRAR OS VALORES DO ÂNGULO, DEVE-SE PASSAR TRUE PARA A VARIÁVEL 
        """
        if tensao:
            self.__graficoTensao()
        if angulo:
            self.__graficoAngulo()
