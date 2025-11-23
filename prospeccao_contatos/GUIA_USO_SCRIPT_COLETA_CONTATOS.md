# Guia de Uso: Script de Coleta de Contatos

## Visão Geral

O script `script_coleta_contatos.py` coleta automaticamente contatos de negócios locais (pet shops, salões de beleza e oficinas mecânicas) em São José, SC, Brasil, de fontes públicas e legais.

**Categorias:**
- Pet Shops (100 contatos)
- Salões de Beleza (100 contatos)
- Oficinas Mecânicas (100 contatos)

**Total:** 300 contatos com telefone e/ou e-mail

---

## Requisitos

### Sistema Operacional
- Windows, macOS ou Linux
- Python 3.8 ou superior

### Dependências Python
```bash
pip install requests beautifulsoup4 pandas googlemaps openpyxl
```

### Configuração Opcional: Google Places API

Para melhor precisão e volume de dados, recomenda-se usar a **API oficial do Google Places**.

#### Passo 1: Criar Projeto no Google Cloud

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto (ex: "Coleta de Contatos")
3. Ative as seguintes APIs:
   - **Places API**
   - **Maps JavaScript API**
   - **Geocoding API**

#### Passo 2: Criar API Key

1. Vá para **Credenciais** no Google Cloud Console
2. Clique em **Criar Credenciais** → **Chave de API**
3. Copie a chave gerada

#### Passo 3: Configurar Variável de Ambiente

**Windows (PowerShell):**
```powershell
$env:GOOGLE_PLACES_API_KEY = "sua_chave_aqui"
```

**macOS/Linux (Terminal):**
```bash
export GOOGLE_PLACES_API_KEY="sua_chave_aqui"
```

**Permanente (macOS/Linux):**
Adicione ao arquivo `~/.bashrc` ou `~/.zshrc`:
```bash
export GOOGLE_PLACES_API_KEY="sua_chave_aqui"
```

---

## Como Usar

### Opção 1: Executar com Google Places API (Recomendado)

```bash
# 1. Configurar variável de ambiente (conforme acima)
export GOOGLE_PLACES_API_KEY="sua_chave_aqui"

# 2. Executar o script
python3 script_coleta_contatos.py
```

**Vantagens:**
- Dados mais precisos e completos
- Inclui avaliações (ratings)
- Coordenadas geográficas (latitude/longitude)
- Websites e telefones verificados

### Opção 2: Executar sem API (Método Alternativo)

```bash
python3 script_coleta_contatos.py
```

O script usará automaticamente o método de **Páginas Amarelas Brasil** como alternativa.

---

## Configuração Personalizada

Edite a seção `CONFIG` no script para personalizar a busca:

```python
CONFIG = {
    "LOCATION": "São José, SC, Brasil",  # Localização
    "LATITUDE": -27.6109,                # Latitude
    "LONGITUDE": -48.6362,               # Longitude
    "RADIUS": 15000,                     # Raio em metros (15 km)
    "CATEGORIES": {
        "pet_shops": ["pet shop", "pet", "veterinário"],
        "saloes_beleza": ["salão de beleza", "cabeleireiro"],
        "oficinas_mecanicas": ["oficina mecânica", "mecânico"]
    },
    "TARGETS_PER_CATEGORY": 100,         # Contatos por categoria
    "OUTPUT_DIR": "./contatos_coletados", # Diretório de saída
    "OUTPUT_FORMAT": "csv"               # csv ou xlsx
}
```

---

## Saída do Script

### Arquivos Gerados

O script cria arquivos na pasta `contatos_coletados/`:

**Formato CSV:**
- `contatos_20251123_143022.csv` - Todos os contatos em um arquivo

**Formato Excel:**
- `contatos_20251123_143022.xlsx` - Com abas por categoria

### Estrutura dos Dados

Cada contato contém:

| Campo | Descrição | Exemplo |
| :--- | :--- | :--- |
| **categoria** | Tipo de negócio | pet_shops |
| **nome** | Nome do estabelecimento | Pet Shop Amigos |
| **endereco** | Endereço completo | Rua A, 123, São José, SC |
| **telefone** | Telefone de contato | (48) 99999-9999 |
| **email** | E-mail de contato | contato@petshop.com.br |
| **website** | Site do negócio | https://petshop.com.br |
| **latitude** | Coordenada geográfica | -27.6109 |
| **longitude** | Coordenada geográfica | -48.6362 |
| **rating** | Avaliação (0-5) | 4.5 |
| **fonte** | Origem dos dados | Google Places API |

---

## Exemplo de Execução

```bash
$ python3 script_coleta_contatos.py

🌟 Script de Coleta de Contatos - Negócios Locais
📍 Localização: São José, SC - Brasil
======================================================================

✓ Google Places API Key detectada

======================================================================
INICIANDO COLETA DE CONTATOS
======================================================================
Localização: São José, SC, Brasil
Raio de busca: 15 km
======================================================================

======================================================================
CATEGORIA: PET SHOPS
======================================================================

🔍 Buscando pet_shops no Google Places...
  ✓ Pet Shop Amigos
  ✓ Clínica Veterinária São José
  ✓ Pet Care Centro
  ...

✓ 45 contatos coletados para pet_shops

======================================================================
CATEGORIA: SALÕES DE BELEZA
======================================================================

🔍 Buscando saloes_beleza no Google Places...
  ✓ Salão de Beleza Elegância
  ✓ Cabeleireiro Profissional
  ...

✓ 38 contatos coletados para saloes_beleza

======================================================================
CATEGORIA: OFICINAS MECÂNICAS
======================================================================

🔍 Buscando oficinas_mecanicas no Google Places...
  ✓ Oficina Mecânica Central
  ✓ Auto Elétrica São José
  ...

✓ 42 contatos coletados para oficinas_mecanicas

======================================================================
RESUMO DE CONTATOS COLETADOS
======================================================================
  Pet Shops: 45 contatos
  Salões De Beleza: 38 contatos
  Oficinas Mecânicas: 42 contatos

  TOTAL: 125 contatos
======================================================================

📁 Exportando contatos para CSV...
  ✓ Arquivo salvo: ./contatos_coletados/contatos_20251123_143022.csv
  ✓ Total de linhas: 125

✓ Coleta concluída!
📁 Arquivos salvos em: ./contatos_coletados
```

---

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'pandas'"

**Solução:**
```bash
pip install pandas
```

### Erro: "Google Places API Key não encontrada"

**Solução:**
1. Verifique se a variável de ambiente foi configurada corretamente
2. Reinicie o terminal/IDE
3. Execute: `echo $GOOGLE_PLACES_API_KEY` (macOS/Linux) ou `echo %GOOGLE_PLACES_API_KEY%` (Windows)

### Erro: "Invalid API Key"

**Solução:**
1. Verifique se a chave foi copiada corretamente
2. Verifique se as APIs estão ativadas no Google Cloud Console
3. Aguarde alguns minutos para a chave ser propagada

### Poucos contatos coletados

**Causas possíveis:**
1. Raio de busca muito pequeno (aumentar `RADIUS`)
2. Palavras-chave muito específicas (adicionar sinônimos)
3. Taxa de limite da API atingida (aguardar alguns minutos)

**Solução:**
Edite a seção `CONFIG` e ajuste os parâmetros.

---

## Boas Práticas

1. **Respeitar Rate Limits:** O script inclui delays entre requisições para não sobrecarregar os servidores.

2. **Verificar Dados:** Sempre revise os contatos coletados antes de usar em campanhas de marketing.

3. **Conformidade LGPD:** Os dados coletados são de fontes públicas, mas respeite as leis de proteção de dados ao usá-los.

4. **Atualizar Regularmente:** Recolha dados periodicamente para manter a lista atualizada.

5. **Usar Dados Responsavelmente:** Não use os contatos para spam ou atividades ilícitas.

---

## Limitações

- **Google Places API:** Limite de 25 requisições por segundo (plano gratuito)
- **Páginas Amarelas:** Pode ter dados desatualizados
- **Cobertura:** Nem todos os negócios estão listados em fontes públicas
- **Telefones/E-mails:** Nem todos os negócios têm essas informações disponíveis publicamente

---

## Suporte e Melhorias

Para sugestões de melhorias ou relatar problemas, entre em contato com a equipe de desenvolvimento.

---

**Versão:** 1.0  
**Última Atualização:** 23/11/2025  
**Autor:** Manus AI
