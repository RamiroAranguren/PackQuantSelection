# Quant Selection – Calculadora por cliente

Primera versión de la calculadora del pack Quant Selection.

## Qué calcula

- Performance según fecha de entrada de cada cliente.
- Comparación contra SPY u otro benchmark.
- Rebalanceos discretos por trimestre.
- Cantidades fijas dentro de cada tramo.
- Entrada a mitad de trimestre comprando la canasta vigente ya drifted.
- Métricas: retorno acumulado, retorno anualizado, volatilidad, Sharpe, máximo drawdown, beta, alpha, tracking error, information ratio, correlación y hit-rate.
- Atribución por acción según P&L de holdings mantenidos.
- Tenencia actual estimada.

## Instalación

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Metodología

1. En cada rebalanceo se define una canasta modelo con pesos objetivo.
2. Esos pesos se convierten en cantidades de acciones al precio de cierre de la primera rueda disponible.
3. Dentro del trimestre no se reajustan pesos.
4. Si un cliente entra a mitad de trimestre, compra la canasta vigente escalada a su monto invertido, no los pesos originales del trimestre.
5. En el siguiente rebalanceo, se vende/compra para pasar a la nueva composición objetivo.

## Dividendos

Por defecto usa `auto_adjust=True` de yfinance, lo que permite trabajar con precios ajustados como aproximación a retorno total. Para una versión productiva se recomienda validar contra una fuente profesional o paga.


## v1.1

Corrección del selector de precios ajustados/no ajustados:

- Con `auto_adjust=True`, la columna `Close` de yfinance ya viene ajustada.
- Con `auto_adjust=False`, la calculadora ahora usa `Close` crudo.
- En la v1, al desactivar precios ajustados se estaba tomando `Adj Close`, por lo que el resultado no cambiaba.


## v1.2

Se agrega sección **Fun**.

### Pack equal weight

- Usa todas las empresas que alguna vez formaron parte del pack hasta cada rebalanceo.
- En cada rebalanceo real, suma los tickers nuevos al universo acumulado.
- Repondera todo el universo acumulado en partes iguales.
- Entre rebalanceos, las cantidades quedan fijas.
- Compara contra el Quant Selection real y contra el benchmark seleccionado.


## v1.3 – Estilo institucional + deploy-ready

Cambios:
- Se agrega un diseño visual institucional inspirado en estilo Balanz: header oscuro, cards, métricas y botones custom.
- Se agrega `.streamlit/config.toml`.
- Se agregan `render.yaml` y `Procfile` para deploy en Render.
- La app sigue funcionando igual que la v1.2.

## Deploy recomendado

### Opción A: Streamlit Community Cloud

1. Subir estos archivos a un repositorio de GitHub.
2. Ir a Streamlit Community Cloud.
3. Crear nueva app desde el repo.
4. Main file path: `app.py`.
5. Deploy.

### Opción B: Render

1. Subir estos archivos a un repositorio de GitHub.
2. Crear un nuevo Web Service en Render.
3. Conectar el repo.
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

Netlify no es la opción recomendada para esta versión porque Streamlit necesita un proceso Python persistente y conexión WebSocket.
