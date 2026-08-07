import json
import asyncio
import httpx
import pandas as pd

API_BASE_URL = "https://api.nexus-365.com/api/v1"

def load_token():
    try:
        with open("session.json", "r") as f:
            return json.load(f).get("token")
    except Exception as e:
        print(f"Error al leer session.json: {e}")
        return None

async def fetch_and_export_rates():
    token = load_token()
    if not token:
        print("No se encontró el token de sesión.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        print("Consultando el tarifario de la plataforma...")
        
        # Consultamos las capacidades y tipos de servicio/costos
        endpoints = [
            f"{API_BASE_URL}/capabilities/auxServicesTypes",
            f"{API_BASE_URL}/capabilities/providerAuxServiceTypes"
        ]

        all_items = []

        for url in endpoints:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                items = data.get("payload", [])
                if isinstance(items, list):
                    all_items.extend(items)
                elif isinstance(items, dict):
                    all_items.append(items)

        # Si el tarifario está en una ruta directa de tarifas
        resp_rates = await client.get(f"{API_BASE_URL}/common/executionTypes", headers=headers)
        
        print("\nGenerando archivo Excel...")
        
        # Procesamos los datos capturados para armar la tabla
        rows = []
        if isinstance(all_items, list) and len(all_items) > 0:
            for item in all_items:
                if isinstance(item, dict):
                    rows.append({
                        "ID / Código": item.get("_id") or item.get("code", ""),
                        "Tipo de Costo / Categoría": item.get("category") or item.get("type", "General"),
                        "Concepto / Descripción": item.get("name") or item.get("description", ""),
                        "Unidad": item.get("unit", "UND"),
                        "Importe / Tarifa ($)": item.get("price") or item.get("cost") or item.get("amount", 0)
                    })

        if rows:
            df = pd.DataFrame(rows)
            file_name = "Tarifario_Nexus_VMU.xlsx"
            df.to_excel(file_name, index=False)
            print(f"¡Éxito! Tarifario exportado a '{file_name}' con {len(rows)} registros.")
        else:
            print("No se encontraron registros estructurados en este endpoint. Se intentará por captura directa del modal.")

if __name__ == "__main__":
    asyncio.run(fetch_and_export_rates())