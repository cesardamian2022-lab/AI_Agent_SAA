import numpy as np
import pandas as pd
import yfinance as yf

def ejecutar_motor_cuantitativo(pesos_dict: dict, horizonte_anos: int = 5):
    """
    Descarga datos históricos de ETFs proxy, calcula métricas de riesgo/retorno
    y simula escenarios futuros (Normal, Mejor, Peor).
    """
    # Mapeo de activos a tickers proxy estándar
    proxy_tickers = {
        "Renta Variable Global": "SPY",
        "Renta Fija Global": "AGG",
        "Real Estate / Infra": "VNQ",
        "Cash": "SHV",
        "Private Equity / Alternativos": "PSP"
    }
    
    # Normalizar tickers según los pesos ingresados
    tickers = [proxy_tickers.get(k, "SPY") for k in pesos_dict.keys()]
    pesos = np.array(list(pesos_dict.values())) / 100.0
    
    # Descargar últimos 3 años de datos históricos diarios
    data = yf.download(tickers, period="3y", progress=False)["Close"]
    if isinstance(data, pd.Series):
        data = data.to_frame()
        
    returns = data.pct_change().dropna()
    
    # Retornos esperados anualizados y matriz de covarianza
    mu = returns.mean() * 252
    cov = returns.cov() * 252
    
    # Retorno y volatilidad esperada de la cartera
    portfolio_return = np.dot(pesos, mu)
    portfolio_vol = np.sqrt(np.dot(pesos.T, np.dot(cov, pesos)))
    
    # Simulación de escenarios a futuro (Monte Carlo simplificado)
    np.random.seed(42)
    simulaciones = 1000
    resultados_finales = []
    
    val_inicial = 100000.0 # USD base
    for _ in range(simulaciones):
        # Movimiento Browniano geométrico simplificado por horizonte
        shocks = np.random.normal(portfolio_return, portfolio_vol, horizonte_anos)
        valor_final = val_inicial * np.prod(1 + shocks)
        resultados_finales.append(valor_final)
        
    percentiles = np.percentile(resultados_finales, [10, 50, 90])
    
    escenarios = {
        "Escenario Peor (P10 - Estrés de Mercado)": round(percentiles[0], 2),
        "Escenario Normal (P50 - Mediana Histórica)": round(percentiles[1], 2),
        "Escenario Mejor (P90 - Ciclo Expansivo)": round(percentiles[2], 2),
        "Retorno Anualizado Esperado": f"{round(portfolio_return * 100, 2)}%",
        "Volatilidad Anualizada": f"{round(portfolio_vol * 100, 2)}%",
        "Sharpe Ratio (Rf=4%)": round((portfolio_return - 0.04) / portfolio_vol, 2)
    }
    
    return escenarios
