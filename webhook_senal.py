from flask import Flask, request, jsonify
import requests

# --- TUS DATOS DE TELEGRAM ---
# TU TOKEN:
TOKEN = 7984885660:AAH1he9rHj_B1N2M8yLbppFR6AEFVuh1ASQ
# TU ID DE CHAT:
CHAT_ID =  '-1002161642865 
# -----------------------------

app = Flask(__name__)

# Función para enviar el mensaje a Telegram
def enviar_mensaje_telegram(mensaje_texto):
    """Usa la API de Telegram para enviar un mensaje."""
    # Codifica el texto para asegurar que caracteres especiales funcionen en la URL
    from urllib.parse import quote_plus
    texto_codificado = quote_plus(mensaje_texto)
    
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje_codificado}'
    try:
        requests.get(url) 
        print(f"Mensaje enviado con éxito: {mensaje_texto}")
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

# Ruta que recibirá la señal (Webhook)
@app.route('/recibir_senal', methods=['POST'])
def recibir_senal():
    """Esta función se activa cuando tu script de señales envía una orden."""
    try:
        # 1. Recibir la información enviada por tu plataforma de trading
        data = request.get_json()
        
        # 2. Extraer el mensaje. **¡Esto asume que tu plataforma envía un campo 'mensaje'!**
        mensaje_recibido = data.get('mensaje', 'Alerta sin formato (Revisar configuración de TradingView/Exnova)')
        
        # 3. Formatear y enviar el mensaje a Telegram
        mensaje_final = f"🚨 SEÑAL AUTOMÁTICA RECIBIDA 🚨\n\n{mensaje_recibido}"
        enviar_mensaje_telegram(mensaje_final)

        # 4. Devolver una respuesta para confirmar la recepción
        return jsonify({"status": "ok", "mensaje": "Señal procesada y enviada a Telegram"}), 200
    
    except Exception as e:
        error_msg = f"Error en la recepción del Webhook: {str(e)}"
        print(error_msg)
        enviar_mensaje_telegram(f"❌ ERROR: Fallo al procesar la señal. Detalle: {str(e)}")
        return jsonify({"status": "error", "detalle": error_msg}), 400

# Esta parte solo es para ejecutar en tu computadora local (no se usa en Render)
if __name__ == '__main__':
    app.run(debug=True, port=5000)
