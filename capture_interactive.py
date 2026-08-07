import os
import asyncio
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

NEXUS_USER = os.getenv("NEXUS_USER")
NEXUS_PASS = os.getenv("NEXUS_PASS")

async def capture_interactive():
    async with async_playwright() as p:
        # Abre el navegador visible
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Escucha en tiempo real cada petición a la API
        async def handle_response(response):
            url = response.url
            if "api.nexus-365.com" in url and response.status == 200:
                print(f"[{response.request.method}] -> {url}")

        page.on("response", handle_response)

        print("Iniciando sesión...")
        await page.goto("https://providers.nexus-365.com/login")
        await page.fill('input[placeholder="Usuario"], input[type="text"]', NEXUS_USER)
        await page.fill('input[placeholder="Contraseña"], input[type="password"]', NEXUS_PASS)
        await page.click('button:has-text("Iniciar sesión")')

        print("\n" + "="*50)
        print("¡SESIÓN INICIADA!")
        print("Haz clic en las pestañas/tablas que quieres replicar en la ventana del navegador.")
        print("Tienes 45 segundos para navegar...")
        print("="*50 + "\n")

        await page.wait_for_timeout(45000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_interactive())