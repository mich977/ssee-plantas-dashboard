# -*- coding: utf-8 -*-
"""
Servidor Operacional SSEE - Plantas EGP ERNC
Permite compartir y ver el dashboard en celular (Android / iPhone) y otros dispositivos en la red.
"""

import http.server
import socket
import socketserver
import webbrowser
import os

PORT = 8080

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:{PORT}"

    print("=" * 65)
    print("   SSEE - PLANTAS EGP - ERNC | SERVIDOR PARA CELULAR / RED")
    print("=" * 65)
    print()
    print("  [>] SERVIDOR ACTIVO:")
    print(f"      En este equipo:   http://localhost:{PORT}")
    print(f"      En tu CELULAR:    {local_url}")
    print()
    print("  [>] PASOS PARA ABRIR EN ANDROID O IPHONE:")
    print("      1. Conecta tu celular a la misma red Wi-Fi")
    print("         (O activa 'Zona Wi-Fi / Compartir Internet' en tu celular).")
    print(f"      2. Abre el navegador (Chrome o Safari) e ingresa:")
    print(f"         {local_url}")
    print("      3. Para tenerlo como App:")
    print("         - iPhone: Compartir -> 'Agregar a pantalla de inicio'")
    print("         - Android: Menú 3 puntos -> 'Agregar a pantalla principal'")
    print()
    print("  Presiona Ctrl + C en esta ventana para detener el servidor.")
    print("=" * 65)

    Handler = http.server.SimpleHTTPRequestHandler
    # Permitir reutilizar la direccion si se reinicia rapido
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")

if __name__ == '__main__':
    main()
