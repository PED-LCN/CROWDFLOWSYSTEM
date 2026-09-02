# Nota acadêmica preliminar — MVP 0

## Questão motivadora

É possível representar observações discretas de uma multidão como um campo
espacial contínuo e, posteriormente, extrair desse campo indicadores de
formação de gargalos e instabilidade coletiva?

## Hipótese inicial

Uma representação que combine densidade local e direção média do movimento
pode descrever a evolução espacial de uma multidão de forma mais informativa
que a contagem global de pessoas. O MVP 0 não testa antecipação de risco; ele
verifica se a infraestrutura mínima de simulação, campo e visualização produz
fenômenos observáveis e reproduzíveis.

## Escopo deste protótipo

- movimentação bidimensional de agentes sintéticos;
- discretização espacial em grade regular;
- suavização gaussiana aproximada da ocupação;
- agregação da velocidade por célula;
- cenários controlados de corredor, gargalo e contrafluxo.

## O que não pode ser concluído

- que o comportamento simulado representa uma multidão real;
- que densidade elevada equivale, isoladamente, a perigo;
- que uma analogia com fluidos é superior a modelos baseados em agentes;
- que os indicadores funcionarão com oclusão e erro de câmeras;
- que o protótipo possui desempenho ou confiabilidade operacional.

## Perguntas para discussão com um orientador

1. Qual literatura deve fundamentar a relação entre densidade, velocidade,
   compressão e risco coletivo?
2. Qual modelo de movimento deve fornecer o *ground truth* sintético?
3. Quais cenários e métricas permitem falsificar a hipótese central?
4. Deve-se comparar campo de densidade, Social Force e modelos macroscópicos?
5. Quais conjuntos públicos de vídeos ou trajetórias podem ser usados depois?
6. Quais cuidados éticos e de LGPD devem orientar a futura aquisição de vídeo?

## Experimento seguinte sugerido

Instrumentar os cenários com métricas temporais, introduzir um indicador de
convergência/compressão e comparar seu tempo de alerta contra um baseline que
utilize apenas ocupação por célula. O protocolo deve registrar parâmetros,
semente, séries temporais e resultado esperado de cada cenário.

