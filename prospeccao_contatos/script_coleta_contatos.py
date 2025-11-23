#!/usr/bin/env python3
"""
Script de Coleta de Contatos - Pet Shops, Salões de Beleza e Oficinas Mecânicas
Localização: São José, SC - Brasil

Descrição:
Este script extrai contatos de negócios locais de fontes públicas (Google Maps, Google My Business)
usando a API do Google Places e web scraping ético.

Requisitos:
- Python 3.8+
- Bibliotecas: requests, beautifulsoup4, pandas, googlemaps

Instalação de dependências:
pip install requests beautifulsoup4 pandas googlemaps selenium

Autor: Manus AI
Data: 2025-11-23
"""

import os
import csv
import json
import time
import re
from datetime import datetime
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

CONFIG = {
    "LOCATION": "São José, SC, Brasil",
    "LATITUDE": -27.6109,
    "LONGITUDE": -48.6362,
    "RADIUS": 15000,  # 15 km em metros
    "CATEGORIES": {
        "pet_shops": ["pet shop", "pet", "veterinário", "clínica veterinária"],
        "saloes_beleza": ["salão de beleza", "salão", "cabeleireiro", "barbershop", "estética"],
        "oficinas_mecanicas": ["oficina mecânica", "oficina", "mecânico", "auto elétrica", "funilaria"]
    },
    "TARGETS_PER_CATEGORY": 100,
    "OUTPUT_DIR": "./contatos_coletados",
    "OUTPUT_FORMAT": "csv"  # csv ou xlsx
}

# ============================================================================
# CLASSE PRINCIPAL: COLETOR DE CONTATOS
# ============================================================================

class ColetorContatos:
    """Classe responsável por coletar contatos de negócios locais."""

    def __init__(self, config: Dict):
        self.config = config
        self.contatos = {
            "pet_shops": [],
            "saloes_beleza": [],
            "oficinas_mecanicas": []
        }
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        self._criar_diretorio_saida()

    def _criar_diretorio_saida(self):
        """Cria o diretório de saída se não existir."""
        if not os.path.exists(self.config["OUTPUT_DIR"]):
            os.makedirs(self.config["OUTPUT_DIR"])
            print(f"✓ Diretório criado: {self.config['OUTPUT_DIR']}")

    # ========================================================================
    # MÉTODO 1: Busca via Google Maps (Web Scraping Ético)
    # ========================================================================

    def buscar_google_maps(self, categoria: str, palavras_chave: List[str]) -> List[Dict]:
        """
        Busca contatos no Google Maps usando web scraping ético.
        
        Nota: Este método usa a interface pública do Google Maps.
        Para produção, considere usar a API oficial do Google Places.
        """
        contatos = []
        
        print(f"\n🔍 Buscando {categoria} no Google Maps...")
        
        for palavra_chave in palavras_chave:
            try:
                # Construir URL de busca do Google Maps
                query = f"{palavra_chave} em {self.config['LOCATION']}"
                url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
                
                # Nota: Google Maps bloqueia web scraping agressivo
                # Este é um exemplo estrutural; em produção, use a API oficial
                print(f"  ℹ️  Para '{palavra_chave}': Acesse manualmente {url}")
                
                # Alternativa: Usar API do Google Places (requer API Key)
                # contatos_api = self._buscar_google_places_api(palavra_chave, categoria)
                # contatos.extend(contatos_api)
                
            except Exception as e:
                print(f"  ✗ Erro ao buscar '{palavra_chave}': {str(e)}")
        
        return contatos

    # ========================================================================
    # MÉTODO 2: Busca via API do Google Places (Recomendado)
    # ========================================================================

    def _buscar_google_places_api(self, palavra_chave: str, categoria: str, api_key: str) -> List[Dict]:
        """
        Busca contatos usando a API oficial do Google Places.
        
        Requer:
        - API Key do Google Cloud (Google Places API)
        - Ativar: Places API, Maps JavaScript API
        
        Documentação: https://developers.google.com/maps/documentation/places/web-service
        """
        contatos = []
        
        try:
            # Endpoint da API Google Places
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            
            params = {
                "query": f"{palavra_chave} {self.config['LOCATION']}",
                "key": api_key,
                "language": "pt-BR"
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "OK":
                for place in data.get("results", [])[:10]:  # Limitar a 10 resultados por palavra-chave
                    contato = self._extrair_dados_place(place, categoria)
                    if contato:
                        contatos.append(contato)
                        print(f"  ✓ {contato['nome']}")
            
            # Respeitar rate limit
            time.sleep(1)
            
        except Exception as e:
            print(f"  ✗ Erro na API Google Places: {str(e)}")
        
        return contatos

    def _extrair_dados_place(self, place: Dict, categoria: str) -> Optional[Dict]:
        """Extrai dados relevantes de um resultado do Google Places."""
        try:
            contato = {
                "categoria": categoria,
                "nome": place.get("name", "N/A"),
                "endereco": place.get("formatted_address", "N/A"),
                "telefone": place.get("formatted_phone_number", ""),
                "email": "",  # Google Places não fornece e-mail diretamente
                "website": place.get("website", ""),
                "latitude": place.get("geometry", {}).get("location", {}).get("lat", ""),
                "longitude": place.get("geometry", {}).get("location", {}).get("lng", ""),
                "rating": place.get("rating", ""),
                "fonte": "Google Places API"
            }
            
            # Tentar extrair e-mail do website
            if contato["website"]:
                contato["email"] = self._extrair_email_do_website(contato["website"])
            
            return contato if contato["telefone"] or contato["email"] else None
            
        except Exception as e:
            print(f"  ✗ Erro ao extrair dados: {str(e)}")
            return None

    def _extrair_email_do_website(self, website: str) -> str:
        """Tenta extrair e-mail do website de um negócio."""
        try:
            response = self.session.get(website, timeout=5)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Procurar por padrões de e-mail no HTML
            email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            emails = re.findall(email_pattern, str(soup))
            
            # Filtrar e-mails de contato (não técnicos)
            for email in emails:
                if not any(x in email.lower() for x in ["noreply", "no-reply", "admin", "root"]):
                    return email
            
            return ""
        except:
            return ""

    # ========================================================================
    # MÉTODO 3: Busca via Google My Business (Alternativa)
    # ========================================================================

    def buscar_google_my_business(self, categoria: str) -> List[Dict]:
        """
        Busca contatos via Google My Business (listagens públicas).
        
        Nota: Requer acesso à API Google My Business ou scraping manual.
        """
        print(f"\n🔍 Buscando {categoria} no Google My Business...")
        print("  ℹ️  Esta funcionalidade requer API Key do Google My Business")
        print("  ℹ️  Ou acesso manual via https://www.google.com/business/")
        
        return []

    # ========================================================================
    # MÉTODO 4: Busca via Páginas Amarelas Brasil
    # ========================================================================

    def buscar_paginas_amarelas(self, categoria: str, palavras_chave: List[str]) -> List[Dict]:
        """
        Busca contatos via Páginas Amarelas Brasil (fonte pública).
        
        Documentação: https://www.paginasamarelas.com.br/
        """
        contatos = []
        
        print(f"\n🔍 Buscando {categoria} nas Páginas Amarelas...")
        
        for palavra_chave in palavras_chave[:3]:  # Limitar a 3 palavras-chave
            try:
                # Construir URL de busca
                query = f"{palavra_chave} São José SC"
                url = f"https://www.paginasamarelas.com.br/search?q={query.replace(' ', '+')}"
                
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Procurar por listagens
                listagens = soup.find_all("div", class_="business-listing")
                
                for listagem in listagens[:10]:  # Limitar a 10 por palavra-chave
                    try:
                        contato = {
                            "categoria": categoria,
                            "nome": listagem.find("h3").text.strip() if listagem.find("h3") else "N/A",
                            "endereco": listagem.find("p", class_="address").text.strip() if listagem.find("p", class_="address") else "N/A",
                            "telefone": self._extrair_telefone(listagem),
                            "email": self._extrair_email(listagem),
                            "website": "",
                            "latitude": "",
                            "longitude": "",
                            "rating": "",
                            "fonte": "Páginas Amarelas Brasil"
                        }
                        
                        if contato["telefone"] or contato["email"]:
                            contatos.append(contato)
                            print(f"  ✓ {contato['nome']}")
                    
                    except Exception as e:
                        continue
                
                # Respeitar rate limit
                time.sleep(2)
                
            except Exception as e:
                print(f"  ✗ Erro ao buscar '{palavra_chave}': {str(e)}")
        
        return contatos

    def _extrair_telefone(self, elemento) -> str:
        """Extrai telefone de um elemento HTML."""
        try:
            # Procurar por padrões de telefone
            telefone_pattern = r"\(?(\d{2})\)?\s?9?\d{4}-?\d{4}"
            texto = elemento.get_text()
            match = re.search(telefone_pattern, texto)
            return match.group(0) if match else ""
        except:
            return ""

    def _extrair_email(self, elemento) -> str:
        """Extrai e-mail de um elemento HTML."""
        try:
            email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            texto = elemento.get_text()
            match = re.search(email_pattern, texto)
            return match.group(0) if match else ""
        except:
            return ""

    # ========================================================================
    # MÉTODO 5: Busca via Facebook (Alternativa)
    # ========================================================================

    def buscar_facebook(self, categoria: str) -> List[Dict]:
        """
        Busca contatos via Facebook Business Pages.
        
        Nota: Requer acesso à API Facebook Graph ou busca manual.
        """
        print(f"\n🔍 Buscando {categoria} no Facebook...")
        print("  ℹ️  Acesse https://www.facebook.com/search/pages/")
        print(f"  ℹ️  Busque por: '{categoria} São José SC'")
        
        return []

    # ========================================================================
    # MÉTODOS DE CONSOLIDAÇÃO E EXPORTAÇÃO
    # ========================================================================

    def consolidar_contatos(self):
        """Consolida todos os contatos coletados."""
        print("\n" + "="*70)
        print("RESUMO DE CONTATOS COLETADOS")
        print("="*70)
        
        total = 0
        for categoria, contatos in self.contatos.items():
            count = len(contatos)
            total += count
            print(f"  {categoria.replace('_', ' ').title()}: {count} contatos")
        
        print(f"\n  TOTAL: {total} contatos")
        print("="*70)

    def exportar_csv(self):
        """Exporta contatos para arquivo CSV."""
        print("\n📁 Exportando contatos para CSV...")
        
        # Consolidar todos os contatos
        todos_contatos = []
        for categoria, contatos in self.contatos.items():
            todos_contatos.extend(contatos)
        
        if not todos_contatos:
            print("  ✗ Nenhum contato para exportar")
            return
        
        # Criar DataFrame
        df = pd.DataFrame(todos_contatos)
        
        # Salvar CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_csv = os.path.join(self.config["OUTPUT_DIR"], f"contatos_{timestamp}.csv")
        
        df.to_csv(arquivo_csv, index=False, encoding="utf-8-sig")
        print(f"  ✓ Arquivo salvo: {arquivo_csv}")
        print(f"  ✓ Total de linhas: {len(df)}")

    def exportar_xlsx(self):
        """Exporta contatos para arquivo Excel."""
        print("\n📁 Exportando contatos para Excel...")
        
        # Consolidar todos os contatos
        todos_contatos = []
        for categoria, contatos in self.contatos.items():
            todos_contatos.extend(contatos)
        
        if not todos_contatos:
            print("  ✗ Nenhum contato para exportar")
            return
        
        # Criar DataFrame
        df = pd.DataFrame(todos_contatos)
        
        # Salvar Excel com múltiplas abas
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_xlsx = os.path.join(self.config["OUTPUT_DIR"], f"contatos_{timestamp}.xlsx")
        
        with pd.ExcelWriter(arquivo_xlsx, engine="openpyxl") as writer:
            # Aba geral
            df.to_excel(writer, sheet_name="Todos", index=False)
            
            # Abas por categoria
            for categoria, contatos in self.contatos.items():
                if contatos:
                    df_cat = pd.DataFrame(contatos)
                    df_cat.to_excel(writer, sheet_name=categoria.replace("_", " ").title(), index=False)
        
        print(f"  ✓ Arquivo salvo: {arquivo_xlsx}")
        print(f"  ✓ Total de linhas: {len(df)}")

    # ========================================================================
    # MÉTODO PRINCIPAL: EXECUTAR COLETA
    # ========================================================================

    def executar(self, usar_api_google: bool = False, google_api_key: str = ""):
        """Executa a coleta de contatos."""
        print("\n" + "="*70)
        print("INICIANDO COLETA DE CONTATOS")
        print("="*70)
        print(f"Localização: {self.config['LOCATION']}")
        print(f"Raio de busca: {self.config['RADIUS']/1000} km")
        print("="*70)
        
        # Coletar contatos por categoria
        for categoria, palavras_chave in self.config["CATEGORIES"].items():
            print(f"\n{'='*70}")
            print(f"CATEGORIA: {categoria.replace('_', ' ').upper()}")
            print(f"{'='*70}")
            
            contatos = []
            
            # Método 1: Google Places API (se disponível)
            if usar_api_google and google_api_key:
                contatos.extend(self._buscar_google_places_api(
                    " ou ".join(palavras_chave),
                    categoria,
                    google_api_key
                ))
            
            # Método 2: Páginas Amarelas
            contatos.extend(self.buscar_paginas_amarelas(categoria, palavras_chave))
            
            # Método 3: Google Maps (manual)
            if not contatos:
                self.buscar_google_maps(categoria, palavras_chave)
            
            # Armazenar contatos
            self.contatos[categoria] = contatos[:self.config["TARGETS_PER_CATEGORY"]]
            
            print(f"\n✓ {len(self.contatos[categoria])} contatos coletados para {categoria}")
        
        # Consolidar e exportar
        self.consolidar_contatos()
        
        if self.config["OUTPUT_FORMAT"] == "csv":
            self.exportar_csv()
        elif self.config["OUTPUT_FORMAT"] == "xlsx":
            self.exportar_xlsx()

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal."""
    print("\n🌟 Script de Coleta de Contatos - Negócios Locais")
    print("📍 Localização: São José, SC - Brasil")
    print("="*70)
    
    # Inicializar coletor
    coletor = ColetorContatos(CONFIG)
    
    # Opção 1: Usar API Google Places (recomendado)
    # Obter API Key em: https://cloud.google.com/docs/authentication/api-keys
    google_api_key = os.environ.get("GOOGLE_PLACES_API_KEY", "")
    
    if google_api_key:
        print("\n✓ Google Places API Key detectada")
        coletor.executar(usar_api_google=True, google_api_key=google_api_key)
    else:
        print("\n⚠️  Google Places API Key não encontrada")
        print("   Para usar a API Google Places:")
        print("   1. Acesse: https://cloud.google.com/docs/authentication/api-keys")
        print("   2. Crie uma API Key")
        print("   3. Ative: Places API, Maps JavaScript API")
        print("   4. Defina a variável de ambiente: GOOGLE_PLACES_API_KEY=sua_chave")
        print("\n   Usando método alternativo (Páginas Amarelas)...")
        coletor.executar(usar_api_google=False)
    
    print("\n✓ Coleta concluída!")
    print(f"📁 Arquivos salvos em: {CONFIG['OUTPUT_DIR']}")

if __name__ == "__main__":
    main()
