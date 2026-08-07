import os
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

NEXUS_USER = os.getenv("NEXUS_USER")
NEXUS_PASS = os.getenv("NEXUS_PASS")

async def capture_dashboard():
    async with async_playwright() as p:
        # Abrimos con interfaz (headless=False) para que puedas ver el panel
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        api_calls = []

        # Captura las respuestas JSON de la API
        async def handle_response(response):
            url = response.url
            if "api.nexus-365.com" in url and response.status == 200:
                api_calls.append(f"{response.request.method} -> {url}")

        page.on("response", handle_response)

        print("Iniciando sesión y navegando al dashboard...")
        await page.goto("https://providers.nexus-365.com/login")
        await page.fill('input[placeholder="Usuario"], input[type="text"]', NEXUS_USER)
        await page.fill('input[placeholder="Contraseña"], input[type="password"]', NEXUS_PASS)
        await page.click('button:has-text("Iniciar sesión")')

        # Damos 12 segundos para que se cargue la tabla principal y interactúes si es necesario
        print("Esperando la carga del panel principal...")
        await page.wait_for_timeout(12000)
        await browser.close()

        print("\n--- ENDPOINTS DE DATOS CAPTURADOS ---")
        for call in sorted(set(api_calls)):
            print(call)

if __name__ == "__main__":
    asyncio.run(capture_dashboard())