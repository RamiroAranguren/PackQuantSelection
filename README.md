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


## v1.4 – Fix visual / contraste

Cambios:
- Gráficos Plotly forzados a tema claro (`plotly_white`) para evitar fondos negros.
- Inputs del sidebar con fondo blanco y texto oscuro.
- Cards de métricas con formato de USD compacto para evitar truncamientos.
- Mejor contraste general, bordes suaves y sombras más consistentes.
- Se mantiene toda la lógica de cálculo de v1.3.


## v1.4.1 – Hotfix Plotly Bar

Corrección:
- `style_plotly()` ahora aplica `line=dict(width=2.4)` solo a trazas `scatter`.
- Esto evita el error de Plotly cuando el gráfico es de barras: `Invalid property specified for object of type plotly.graph_objs.Bar: 'line'`.
- Se mantiene el fix visual de v1.4.


## v1.5 – Motor por retornos

Corrección metodológica:
- La calculadora ahora usa un motor basado en retornos diarios por ticker y "sleeves" de valor.
- Esto evita usar precios ajustados como si fueran precios transables para calcular acciones, lo que podía distorsionar mucho la cartera al rebalancear.
- Con precios crudos, el resultado es equivalente al método por cantidad de acciones.
- Con precios ajustados, el resultado es una aproximación más consistente de total return.
- La opción de precios ajustados queda desactivada por defecto para que el resultado sea comparable con Excel de precios de cierre.


## v1.6 – Pulido final de UI

Cambios:
- Rebalanceos cargados se movieron al final y se muestran como matriz por trimestre con ticker y ponderación.
- Las tablas principales se renderizan como HTML de fondo blanco para evitar modo oscuro.
- Métricas y Tenencia actual se muestran lado a lado.
- Se elimina la tabla debajo del gráfico de Atribución por acción.
- Se elimina el texto `undefined` de gráficos al forzar título vacío.
- Inputs de monto y tasa pasan a texto numérico para evitar botones +/-.
- Se mantiene el motor por retornos de v1.5.


## v1.7 – Rebalance table design

Cambio visual:
- La tabla de rebalanceos se rediseñó para integrarse con el resto de la app.
- Se reemplazó el estilo tipo Excel/celeste por un estilo institucional: headers navy/blue, fondo blanco, bordes suaves, hover sutil y tipografía coherente.
- Se agrega una breve nota metodológica sobre composición objetivo y cantidades fijas entre rebalanceos.
