# Justificativa das métricas: Dashboard 2

## 1. Gols no recorte

- **Variável:** contagem de linhas do dataset (cada linha é um gol)
- **O que mede:** o volume de gols no clube, competição e temporada selecionados
- **Por que foi escolhida:** dá a escala do recorte. Sem ela, as proporções dos outros cartões podem enganar (70% de 10 gols não é o mesmo que 70% de 400)
- **Público-alvo:** todos os públicos, pois é o número de entrada do dashboard
- **Qual decisão pode ser apoiada:** saber se o recorte tem gols suficientes para tirar conclusões ou se é melhor ampliar o filtro, além de comparar a produção entre temporadas e competições
- **O que comunica:** Messi marcou N gols, o equivalente a X% da carreira de clube

## 2. Com assistência

- **Variável:** `participacao_gols`
- **O que mede:** a proporção dos gols que tiveram passe de um companheiro
- **Por que foi escolhida:** é a variável-alvo da EDA. Mostra o quanto a produção depende do coletivo e o quanto vem de jogadas individuais e bola parada
- **Público-alvo:** analistas de desempenho e comissões técnicas
- **Qual decisão pode ser apoiada:** do lado do adversário, marcar o jogador (proporção baixa, ele resolve sozinho) ou cortar as linhas de passe até ele (proporção alta). Do lado do próprio clube, avaliar se o elenco está alimentando o atacante
- **O que comunica:** 7 em cada 10 gols tiveram assistência; o delta mostra se o recorte é mais coletivo ou mais individual que a média da carreira

## 3. Minuto médio do gol

- **Variável:** `minuto`
- **O que mede:** em que momento da partida os gols costumam sair
- **Por que foi escolhida:** é a principal variável quantitativa do Dashboard 1 e traduz a distribuição do minuto num número só
- **Público-alvo:** comissões técnicas e analistas de desempenho
- **Qual decisão pode ser apoiada:** planejar substituições e o ritmo de jogo. Quando a média tá acima de 45 minutos, indica que há concentração de gols no 2º tempo, período em que a defesa adversária costuma estar mais cansada
- **O que comunica:** em média, os gols saem por volta dos 52 minutos, ou seja, mais no segundo tempo

## 4. Chute de pé esquerdo

- **Variável:** `Type` (tipo de finalização)
- **O que mede:** a proporção dos gols marcados com chute de pé esquerdo
- **Por que foi escolhida:** é o tipo de finalização dominante e a característica mais conhecida do jogador. Quantificar isso transforma uma impressão em número
- **Público-alvo:** olheiros e analistas de clubes adversários
- **Qual decisão pode ser apoiada:** posicionamento defensivo, por exemplo forçar o jogador a finalizar com a direita. O delta mostra em quais recortes ele foi menos previsível
- **O que comunica:** 6 em cada 10 gols saíram do pé esquerdo

## 5. Gols em casa

- **Variável:** `Venue` (H, de Home = mandante, A, de Away = visitante)
- **O que mede:** a proporção dos gols marcados com o clube jogando em casa
- **Por que foi escolhida:** mostra se a produção depende do mando de campo, uma pergunta clássica de análise de desempenho
- **Público-alvo:** analistas de desempenho e jornalistas
- **Qual decisão pode ser apoiada:** expectativa de desempenho e preparação para jogos fora de casa. Por exemplo, uma proporção bem acima de 50% sugere um rendimento mais fraco como visitante
- **O que comunica:** cerca de 60% dos gols saíram em casa
