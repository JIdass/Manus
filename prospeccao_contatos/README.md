# Prospecção de Contatos - São José, SC

## Objetivo

Coletar automaticamente **300 contatos** (100 por categoria) de negócios locais em São José, Santa Catarina, Brasil:

- **Pet Shops** (100 contatos)
- **Salões de Beleza** (100 contatos)
- **Oficinas Mecânicas** (100 contatos)

Cada contato inclui **telefone celular** e/ou **e-mail** para facilitar campanhas de marketing e vendas.

---

## Arquivos do Projeto

| Arquivo | Descrição |
| :--- | :--- |
| `script_coleta_contatos.py` | Script Python principal para coleta de contatos |
| `GUIA_USO_SCRIPT_COLETA_CONTATOS.md` | Guia completo de instalação, configuração e uso |
| `README.md` | Este arquivo |

---

## Início Rápido

### 1. Clonar o Repositório

```bash
git clone https://github.com/JIdass/Manus.git
cd Manus/prospeccao_contatos
```

### 2. Instalar Dependências

```bash
pip install requests beautifulsoup4 pandas googlemaps openpyxl
```

### 3. Configurar API Google Places (Opcional mas Recomendado)

```bash
export GOOGLE_PLACES_API_KEY="sua_chave_aqui"
```

Consulte o **GUIA_USO_SCRIPT_COLETA_CONTATOS.md** para instruções detalhadas.

### 4. Executar o Script

```bash
python3 script_coleta_contatos.py
```

Os contatos serão salvos em `contatos_coletados/contatos_YYYYMMDD_HHMMSS.csv` ou `.xlsx`

---

## Características

✅ **Coleta Automática:** Busca contatos de múltiplas fontes públicas  
✅ **Dados Completos:** Telefone, e-mail, endereço, website, coordenadas geográficas  
✅ **Múltiplos Métodos:** Google Places API, Páginas Amarelas, Google Maps  
✅ **Exportação Flexível:** CSV ou Excel com abas por categoria  
✅ **Tratamento de Erros:** Robusto e confiável  
✅ **Respeito a Rate Limits:** Não sobrecarrega servidores  
✅ **Conformidade LGPD:** Usa apenas dados públicos  

---

## Estrutura de Dados

Cada contato contém:

```json
{
  "categoria": "pet_shops",
  "nome": "Pet Shop Amigos",
  "endereco": "Rua A, 123, São José, SC 88100-000",
  "telefone": "(48) 99999-9999",
  "email": "contato@petshop.com.br",
  "website": "https://petshop.com.br",
  "latitude": -27.6109,
  "longitude": -48.6362,
  "rating": 4.5,
  "fonte": "Google Places API"
}
```

---

## Métodos de Coleta

### 1. Google Places API (Recomendado)

**Vantagens:**
- Dados mais precisos e completos
- Inclui avaliações (ratings)
- Coordenadas geográficas verificadas
- Websites e telefones validados

**Requisitos:**
- API Key do Google Cloud
- Ativar: Places API, Maps JavaScript API

### 2. Páginas Amarelas Brasil

**Vantagens:**
- Sem necessidade de API Key
- Base de dados brasileira confiável
- Dados atualizados regularmente

**Limitações:**
- Pode ter dados desatualizados
- Cobertura menor que Google

### 3. Google Maps (Manual)

**Uso:**
- Busca manual em https://maps.google.com
- Filtre por categoria e localização
- Colete contatos manualmente

---

## Configuração Personalizada

Edite a seção `CONFIG` no script para personalizar:

```python
CONFIG = {
    "LOCATION": "São José, SC, Brasil",
    "LATITUDE": -27.6109,
    "LONGITUDE": -48.6362,
    "RADIUS": 15000,  # 15 km
    "TARGETS_PER_CATEGORY": 100,
    "OUTPUT_FORMAT": "csv"  # ou xlsx
}
```

---

## Exemplo de Saída

```
🌟 Script de Coleta de Contatos - Negócios Locais
📍 Localização: São José, SC - Brasil

======================================================================
INICIANDO COLETA DE CONTATOS
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
```

---

## Troubleshooting

### Erro: "ModuleNotFoundError"

```bash
pip install requests beautifulsoup4 pandas googlemaps openpyxl
```

### Erro: "Google Places API Key não encontrada"

Verifique se a variável de ambiente foi configurada:

```bash
echo $GOOGLE_PLACES_API_KEY  # macOS/Linux
echo %GOOGLE_PLACES_API_KEY%  # Windows
```

### Poucos contatos coletados

1. Aumentar `RADIUS` no `CONFIG`
2. Adicionar mais palavras-chave em `CATEGORIES`
3. Aguardar alguns minutos se atingiu rate limit

Consulte **GUIA_USO_SCRIPT_COLETA_CONTATOS.md** para mais detalhes.

---

## Boas Práticas

1. **Verificar Dados:** Sempre revise os contatos antes de usar
2. **Respeitar LGPD:** Use dados responsavelmente
3. **Atualizar Regularmente:** Recolha dados periodicamente
4. **Não Fazer Spam:** Respeite as preferências dos contatos
5. **Conformidade:** Siga as leis de proteção de dados

---

## Limitações

- **Rate Limits:** Google Places API tem limites de requisições
- **Cobertura:** Nem todos os negócios estão em fontes públicas
- **Dados Incompletos:** Nem todos têm telefone/e-mail disponíveis
- **Atualização:** Dados podem estar desatualizados

---

## Próximos Passos

1. ✅ Clonar repositório
2. ✅ Instalar dependências
3. ✅ Configurar API Google Places (opcional)
4. ✅ Executar script
5. ✅ Revisar e validar contatos
6. ✅ Usar contatos em campanhas de marketing

---

## Suporte

Para dúvidas, sugestões ou relatar problemas:

1. Abra uma **Issue** no repositório
2. Faça um **Pull Request** com melhorias
3. Entre em contato com a equipe de desenvolvimento

---

## Licença

Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

---

## Autor

**Manus AI** - Desenvolvimento de Scripts e Ferramentas de Automação

**Data:** 23 de Novembro de 2025  
**Versão:** 1.0

---

## Changelog

### v1.0 (23/11/2025)
- ✅ Script inicial com suporte a Google Places API
- ✅ Integração com Páginas Amarelas Brasil
- ✅ Exportação CSV e Excel
- ✅ Documentação completa
- ✅ Guia de uso detalhado
