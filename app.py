from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

API_URL = os.getenv("API_URL")
ZONA_HORARIA = pytz.timezone("America/Merida")


# --- Utilidades ---
def fmt_to_api(date_str):
    if not date_str: return None
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%y%m%d")

def fmt_from_api(yymmdd):
    try:
        return datetime.strptime(yymmdd, "%y%m%d").strftime("%d-%m-%Y")
    except:
        return yymmdd

@app.route('/')
def index():
    hoy = datetime.now(ZONA_HORARIA).strftime("%Y-%m-%d")
    desde = request.args.get('desde', hoy)
    hasta = request.args.get('hasta', hoy)
    contribuyente = request.args.get('contribuyente', '')

    params = {"desde": fmt_to_api(desde), "hasta": fmt_to_api(hasta)}
    if contribuyente:
        params["contribuyente"] = contribuyente

    endpoint = "recibos/filtrar" if contribuyente else "recibos"
    try:
        r_res = requests.get(f"{API_URL}{endpoint}", params=params)
        r_res.encoding = 'utf-8'
        r_data = r_res.json() if r_res.status_code == 200 else []
    except Exception:
        r_data = []
    
    try:
        t_res = requests.get(f"{API_URL}recibos/totales", params=params)
        if t_res.status_code == 200:
            r_totales = t_res.json()
        else:
            r_totales = {"total_neto": 0, "total_descuento": 0, "cantidad_status_1": 0}
    except Exception:
        r_totales = {"total_neto": 0, "total_descuento": 0, "cantidad_status_1": 0}

    api_desde = fmt_to_api(desde)
    api_hasta = fmt_to_api(hasta)

    return render_template('recibos.html', 
                           recibos=r_data, 
                           totales=r_totales,
                           desde=desde, 
                           hasta=hasta,
                           api_desde=api_desde,
                           api_hasta=api_hasta, 
                           contribuyente=contribuyente,
                           fmt_fecha=fmt_from_api,
                           API_URL=API_URL)


@app.route('/obtener_resumen')
def obtener_resumen():
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')
    
    params = {
        "desde": fmt_to_api(desde),
        "hasta": fmt_to_api(hasta)
    }
    
    try:
        response = requests.get(f"{API_URL}recibos/totales/despliegue", params=params)
        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        return {"status": "error", "message": "No se encontraron datos"}, 404
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
    
@app.route('/cedulas')
def cedulas():
    hoy = datetime.now(ZONA_HORARIA).strftime("%Y-%m-%d")
    desde = request.args.get('desde', hoy)
    hasta = request.args.get('hasta', hoy)
    contribuyente = request.args.get('contribuyente', '')

    api_desde = fmt_to_api(desde)
    api_hasta = fmt_to_api(hasta)
    
    params = {"desde": api_desde, "hasta": api_hasta}
    if contribuyente:
        params["contribuyente"] = contribuyente

    endpoint = "cedulas/filtrar" if contribuyente else "cedulas"
    try:
        response = requests.get(f"{API_URL}{endpoint}", params=params)
        c_data = response.json() if response.status_code == 200 else []
    except:
        c_data = []

    return render_template('cedulas.html', 
                           cedulas=c_data, 
                           desde=desde, 
                           hasta=hasta,
                           api_desde=api_desde,
                           api_hasta=api_hasta,
                           contribuyente=contribuyente,
                           fmt_fecha=fmt_from_api,
                           API_URL=API_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)