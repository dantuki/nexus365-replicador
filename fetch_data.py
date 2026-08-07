import json
import asyncio
import httpx

API_BASE_URL = "https://api.nexus-365.com/api/v1"

def load_token():
    try:
        with open("session.json", "r") as f:
            return json.load(f).get("token")
    except Exception as e:
        print(f"Error al leer session.json: {e}")
        return None

async def fetch_all_aux_services():
    token = load_token()
    if not token:
        print("No se encontró token de sesión.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Solicitamos los primeros 50 registros de Servicios Auxiliares
    url_services = f"{API_BASE_URL}/auxservices?limit=50&page=1&sort=currentStatus"
    
    # Solicitamos los primeros 50 registros de Hojas de Costos
    url_costs = f"{API_BASE_URL}/cost/auxServices?limit=50&page=1"

    async with httpx.AsyncClient(timeout=15.0) as client:
        print("Consultando Servicios Auxiliares...")
        resp_services = await client.get(url_services, headers=headers)
        
        print("Consultando Hojas de Costos...")
        resp_costs = await client.get(url_costs, headers=headers)

        if resp_services.status_code == 200:
            data_services = resp_services.json()
            print(f"Éxito Servicios Auxiliares. Registros obtenidos: {len(data_services.get('payload', {}).get('docs', []))}")
            
            # Guardar resultado en JSON local
            with open("servicios_auxiliares.json", "w", encoding="utf-8") as f:
                json.dump(data_services, f, indent=2, ensure_ascii=False)
        else:
            print(f"Error al obtener servicios: {resp_services.status_code}")

        if resp_costs.status_code == 200:
            data_costs = resp_costs.json()
            print(f"Éxito Hojas de Costos. Registros obtenidos: {len(data_costs.get('payload', {}).get('docs', []))}")
            
            # Guardar resultado en JSON local
            with open("hojas_de_costos.json", "w", encoding="utf-8") as f:
                json.dump(data_costs, f, indent=2, ensure_ascii=False)
        else:
            print(f"Error al obtener costos: {resp_costs.status_code}")

if __name__ == "__main__":
    asyncio.run(fetch_all_aux_services())