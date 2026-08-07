import os
import asyncio
import httpx
import re
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://providers.nexus-365.com"

async def inspect_login_page():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0, follow_redirects=True) as client:
        print("Obteniendo página principal de Nexus...")
        res = await client.get("/")
        print(f"URL final tras redirecciones: {res.url}\n")
        
        html = res.text
        
        print("--- FORMULARIOS ENCONTRADOS ---")
        forms = re.findall(r'<form.*?>', html, re.IGNORECASE)
        for f in forms:
            print(f)
            
        print("\n--- CAMPOS DE ENTRADA (<input>) ---")
        inputs = re.findall(r'<input.*?>', html, re.IGNORECASE)
        for i in inputs:
            print(i)

if __name__ == "__main__":
    asyncio.run(inspect_login_page())