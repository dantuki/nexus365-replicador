import os
import json
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

NEXUS_USER = os.getenv("NEXUS_USER")
NEXUS_PASS = os.getenv("NEXUS_PASS")

async def get_tokens():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        auth_data = {}

        async def handle_response(response):
            if "authentication/ssignin" in response.url and response.status == 200:
                try:
                    data = await response.json()
                    if data.get("msg") == "Success":
                        auth_data["token"] = data["payload"]["token"]
                        auth_data["refreshToken"] = data["payload"]["refreshToken"]
                except Exception as e:
                    print(f"Error al procesar la respuesta: {e}")

        page.on("response", handle_response)

        print("Navegando a la página de login...")
        await page.goto("https://providers.nexus-365.com/login")

        await page.fill('input[placeholder="Usuario"], input[type="text"]', NEXUS_USER)
        await page.fill('input[placeholder="Contraseña"], input[type="password"]', NEXUS_PASS)

        print("Enviando credenciales...")
        await page.click('button:has-text("Iniciar sesión")')

        await page.wait_for_timeout(4000)
        await browser.close()

        if "token" in auth_data:
            print("Token obtenido con éxito.")
            with open("session.json", "w") as f:
                json.dump(auth_data, f, indent=4)
            return auth_data["token"]
        else:
            print("No se pudo obtener el token. Verifica las credenciales.")
            return None

if __name__ == "__main__":
    asyncio.run(get_tokens())