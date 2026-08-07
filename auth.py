import asyncio
import httpx
import re

BASE_URL = "https://providers.nexus-365.com"

async def inspect_nexus():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0, follow_redirects=True) as client:
        print("--- PROBANDO ENDPOINTS HABITUALES ---")
        endpoints = ["/", "/login", "/Account/Login", "/api/auth/login", "/api/login"]
        
        for ep in endpoints:
            try:
                res = await client.get(ep)
                print(f"GET {ep} -> Status: {res.status_code} | URL Final: {res.url}")
            except Exception as e:
                print(f"GET {ep} -> Error: {e}")
                
        print("\n--- ANALIZANDO ARCHIVOS JS / SCRIPTS ---")
        res_main = await client.get("/")
        html = res_main.text
        
        scripts = re.findall(r'<script.*?>', html, re.IGNORECASE)
        print(f"Total de scripts encontrados: {len(scripts)}")
        for s in scripts:
            print(s)
            
        print("\n--- VISTA PREVIA DEL HTML ---")
        print(html[:600])

if __name__ == "__main__":
    asyncio.run(inspect_nexus())