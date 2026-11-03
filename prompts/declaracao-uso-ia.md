# Declaração de Uso de IA

**Nome:** Gabriel Victalino Mancebo
**Data:** 27/10/2026

## Ferramenta

Google Antigravity (agente de código na IDE), com o modelo Claude Opus 5.5. A skill `developing-with-streamlit` (instalada por `streamlit skills` em `.agents/skills/`) foi usada como referência de boas práticas do Streamlit.

## Prompt usado

1. "leia os PDFs anexados e use a skill/ask-matt para pesquisar skills da minha pasta e decidir quais as melhores que podem ser usadas nesse caso, não implemente nada ainda."
2. "implemente o que foi analisado"

Os PDFs eram os slides das Aulas 21 e 22 (Streamlit partes 1 e 2).

## O que a IA gerou

- `.streamlit/config.toml`: tema claro com a paleta Blaugrana/PSG inspirada nos clubes de Lionel Messi (azul `#004D98`, grená `#A50044`, azul-marinho `#0B1F3A`) e as fontes Inter/Outfit.
- `app.py`: abas "Dashboard 1" e "Dashboard 2"; tratamento dos casos 0, 1 e 2+ variáveis e de variáveis sem variação no recorte; os KPIs foram movidos para o Dashboard 2, com delta em relação à carreira; gráficos de barra em Altair com seleção cruzada por temporada.
- `src/metricas.py`: cálculo dos KPIs e das agregações em pandas puro (dá para reaproveitar no notebook).
- `src/data_loader.py`: correção das temporadas "11-Dec"/"Dec-13" (convertidas em data pelo Excel) e tradução do tipo de finalização.
- `entregas/justificativa-metricas.md`: rascunho da justificativa das 5 métricas.
- Testes automáticos com `streamlit.testing.v1.AppTest` cobrindo os cenários de 0/1/2+ variáveis (fora do repositório).

## O que foi aceito, modificado ou rejeitado e por quê

<!-- Preencha com a sua avaliação depois de revisar o código e o app rodando. -->

- **Aceito:** A estrutura e o visual geral, organização em abas, uso de filtros, tratamento de casos com poucas variáveis e KPIs com deltas em relação à carreira. Também foi mantida a lógica de usar dados agregados (fonte `src/metricas.py`) sempre que possível, e os testes automáticos para validação dos cenários de filtro.
- **Modificado:** `entregas/justificativa-metricas.md` foi modificado porque deve ser feito por mim. Foram alterados somente o planejamento de cada métrica (Variável, O que mede, etc).
- **Rejeitado:** Tabela com cada métrica proposta no arquivo 'planilha-metricas.md' porque deve ser feito por mim.
