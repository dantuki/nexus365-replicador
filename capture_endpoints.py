import os
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

NEXUS_USER = os.getenv("NEXUS_USER")
NEXUS_PASS = os.getenv("NEXUS_PASS")

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        endpoints = set()

        # Intercepta las peticiones dirigidas a la API
        async def handle_request(request):
            if "api.nexus-365.com" in request.url:
                endpoints.add((request.method, request.url))

        page.on("request", handle_request)

        print("Iniciando sesión para registrar peticiones...")
        await page.goto("https://providers.nexus-365.com/login")
        await page.fill('input[placeholder="Usuario"], input[type="text"]', NEXUS_USER)
        await page.fill('input[placeholder="Contraseña"], input[type="password"]', NEXUS_PASS)
        await page.click('button:has-text("Iniciar sesión")')

        # Espera a que la SPA cargue la interfaz y realice las peticiones iniciales
        await page.wait_for_timeout(6000)
        await browser.close()

        print("\n--- ENDPOINTS DE API REALES CAPTURADOS ---")
        for method, url in sorted(endpoints):
            print(f"{method} -> {url}")

if __name__ == "__main__":
    asyncio.run(capture())