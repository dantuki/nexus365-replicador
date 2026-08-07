import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

NEXUS_USER = os.getenv("NEXUS_USER")
NEXUS_PASS = os.getenv("NEXUS_PASS")
API_BASE_URL = "https://api.nexus-365.com/api/v1"

async def login():
    url = f"{API_BASE_URL}/authentication/ssignin"
    
    payload = {
        "username": NEXUS_USER,
        "password": NEXUS_PASS,
        "captchaToken": ""
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        print(f"Enviando solicitud de inicio de sesión para: {NEXUS_USER}...")
        
        try:
            response = await client.post(url, json=payload, headers=headers)
            print(f"Código de respuesta HTTP: {response.status_code}")
            
            data = response.json()
            print("Respuesta recibida del servidor:")
            print(data)

            if response.status_code == 200 and data.get("msg") == "Success":
                token = data.get("payload", {}).get("token")
                print("\nAutenticación exitosa.")
                print(f"Bearer Token obtenido: {token[:30]}...")
                return token
            else:
                print("\nError al iniciar sesión:", data.get("msg"))
                return None

        except Exception as e:
            print(f"Excepción durante la autenticación: {e}")
            return None

if __name__ == "__main__":
    asyncio.run(login())