import json
import asyncio
import httpx

API_BASE_URL = "https://api.nexus-365.com/api/v1"

def load_token():
    try:
        with open("session.json", "r") as f:
            data = json.load(f)
            return data.get("token")
    except Exception as e:
        print(f"Error al leer session.json: {e}")
        return None

async def test_auth():
    token = load_token()
    if not token:
        print("No se encontró ningún token en session.json.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        print("Probando petición al endpoint /users/me...")
        response = await client.get(f"{API_BASE_URL}/users/me", headers=headers)
        
        print(f"Código de respuesta HTTP: {response.status_code}")
        if response.status_code == 200:
            print("Conexión exitosa. Datos de la cuenta:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("Error en la petición:", response.text)

if __name__ == "__main__":
    asyncio.run(test_auth())