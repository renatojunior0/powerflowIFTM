from classeMetodoNewton import Newton

#Teste1 = Newton()
#Teste2 = Newton()

""" Teste1.setBarrasSistema(1, 1, 1.05, 0.00, 0 + 0 * 1j, 0 + 0 * 1j)
Teste1.setBarrasSistema(2, 2, 1.00, 0.00, 256.6e6 + 110.2e6 * 1j, 0 + 0 * 1j)
Teste1.setBarrasSistema(3, 2, 1.00, 0.00, 138.6e6 + 45.2e6 * 1j, 0 + 0 * 1j)

Teste1.mostrarBarras()
Teste1.setCalBarrasEspecf()

Teste1.ligacoesBarras(1, 2, impedancia=0.02 + 0.04j)
Teste1.ligacoesBarras(1, 3, impedancia=0.01 + 0.03j)
Teste1.ligacoesBarras(2, 3, impedancia=0.0125 + 0.025j)

Teste1.mostrarLigacoes()

Teste1.ResolucaoCircuito(erro=1e-9, listaBarrasTensoes=[2,3], listaBarrasAngulos=[2,3])
Teste1.FluxoPotenciaAparente(printTensoes=True, printCorrentes=True)
Teste1.graficoDados(tensao=True, angulo=True)
Teste1.mostrarBarras() """


# ##########################################################

# Teste2.setBarrasSistema(1, 1, 1.07, 0, 0 + 0 * 1j, 0 + 0 * 1j)
# Teste2.setBarrasSistema(2, 3, 1.05, 0, 0 + 0 * 1j, 50e6 + 0 * 1j)
# Teste2.setBarrasSistema(3, 3, 1.05, 0, 0 + 0 * 1j, 50e6 + 0 * 1j)
# Teste2.setBarrasSistema(4, 2, 1.00, 0, 100e6 + 15e6 * 1j, 0 + 0 * 1j)
# Teste2.setBarrasSistema(5, 2, 1.00, 0, 100e6 + 15e6 * 1j, 0 + 0 * 1j)
# Teste2.setBarrasSistema(6, 2, 1.00, 0, 100e6 + 15e6 * 1j, 0 + 0 * 1j)

# Teste2.mostrarBarras()
# Teste2.setCalBarrasEspecf()

# Teste2.ligacoesBarras(1, 2, impedancia=0.1 + 0.2j)
# Teste2.ligacoesBarras(1, 4, impedancia=0.05 + 0.2j)
# Teste2.ligacoesBarras(1, 5, impedancia=0.08 + 0.3j)
# Teste2.ligacoesBarras(2, 3, impedancia=0.05 + 0.25j)
# Teste2.ligacoesBarras(2, 4, impedancia=0.05 + 0.1j)
# Teste2.ligacoesBarras(2, 5, impedancia=0.1 + 0.3j)
# Teste2.ligacoesBarras(2, 6, impedancia=0.07 + 0.2j)
# Teste2.ligacoesBarras(3, 5, impedancia=0.12 + 0.26j)
# Teste2.ligacoesBarras(3, 6, impedancia=0.02 + 0.1j)
# Teste2.ligacoesBarras(4, 5, impedancia=0.2 + 0.4j)
# Teste2.ligacoesBarras(5, 6, impedancia=0.1 + 0.3j)

# Teste2.mostrarLigacoes()

# Teste2.ResolucaoCircuito(iteracoes=None, listaBarrasTensoes=[4, 5, 6], listaBarrasAngulos=[2, 3, 4, 5, 6], erro=1e-13)
# Teste2.FluxoPotenciaAparente(printTensoes=True, printCorrentes=True)
# Teste2.PerdasSistema()
# Teste2.graficoDados(tensao=True, angulo=True)
# Teste2.mostrarBarras()

SistemaIF = Newton()

SistemaIF.setBarrasSistema(1, 1, 1.00, 0, 0 + 0 * 1j, 0 + 0 * 1j)
SistemaIF.setBarrasSistema(2, 2, 1.00, 0, 0 + 0 * 1j, 0 + 0 * 1j)
SistemaIF.setBarrasSistema(3, 2, 1.00, 0, 0 + 0 * 1j, 0 + 0 * 1j)
SistemaIF.setBarrasSistema(4, 2, 1.00, 0, 84.72e3 + 36.098e3 * 1j, 0 + 0 * 1j)
SistemaIF.setBarrasSistema(5, 2, 1.00, 0, 6e3 + 2.55e3 * 1j, 0 + 0 * 1j)
SistemaIF.setBarrasSistema(6, 2, 1.00, 0, 5.5e3 + 0 * 1j, 0 + 0 * 1j)
SistemaIF.setBarrasSistema(7, 2, 1.00, 0, 56.59e3 + 24.11e3 * 1j, 0 + 0 * 1j)
SistemaIF.setBarrasSistema(8, 2, 1.00, 0, 2.02e3 + 0.87e3 * 1j, 0 + 0 * 1j)
SistemaIF.setBarrasSistema(9, 2, 1.00, 0, 9.56e3 + 4.07e3 * 1j, 0 + 0 * 1j)

SistemaIF.mostrarBarras()
SistemaIF.setCalBarrasEspecf()

SistemaIF.ligacoesBarras(1, 2, impedancia=0.01 + 0.1j)
SistemaIF.ligacoesBarras(2, 3, impedancia=0.001 + 0.01j)
SistemaIF.ligacoesBarras(3, 4, impedancia=0.001 + 0.01j)
SistemaIF.ligacoesBarras(3, 5, impedancia=0.001 + 0.01j)
SistemaIF.ligacoesBarras(3, 6, impedancia=0.001 + 0.01j)
SistemaIF.ligacoesBarras(3, 7, impedancia=0.001 + 0.01j)
SistemaIF.ligacoesBarras(3, 8, impedancia=0.001 + 0.01j)
SistemaIF.ligacoesBarras(3, 9, impedancia=0.001 + 0.01j)

SistemaIF.mostrarLigacoes()

SistemaIF.ResolucaoCircuito(erro=1e-05, listaBarrasTensoes=[2, 3, 4, 5, 6, 7, 8, 9], listaBarrasAngulos=[2, 3, 4, 5, 6, 7, 8, 9])
SistemaIF.FluxoPotenciaAparente(printTensoes=True, printCorrentes=True)
SistemaIF.PerdasSistema()
SistemaIF.mostrarBarras()


