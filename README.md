# CrowdFlowSystem — MVP 0

Prova de conceito em Python para visualizar ocupação e fluxo de uma multidão
simulada em um ambiente 2D. O objetivo desta versão não é prever acidentes nem
reproduzir fielmente a dinâmica humana: é criar um artefato experimental com o
qual seja possível discutir a hipótese do projeto com um orientador acadêmico.

## O que esta versão demonstra

- ambiente 2D dividido em células;
- agentes com origem, destino e movimento simples;
- paredes e passagem estreita;
- campo de densidade suavizado;
- vetor médio de movimento em cada célula;
- três cenários reproduzíveis;
- execução visual e execução sem interface para testes.

## Executar

Requer Python 3.10 ou superior. Não há dependências externas.

```powershell
python -m crowdflow
```

Para executar um experimento reproduzível sem abrir uma janela:

```powershell
python -m crowdflow --headless --scenario bottleneck --steps 600 --seed 7
```

Cenários disponíveis: `corridor`, `bottleneck` e `counterflow`.

## Controles da interface

- selecione um cenário na caixa superior;
- use **Pausar/Continuar** para inspecionar um instante;
- use **Reiniciar** para voltar à mesma configuração inicial;
- altere a semente para gerar outra execução reproduzível;
- marque **Agentes** e **Vetores** para alternar as camadas visuais.

## Interpretação

As cores representam densidade local suavizada: azul indica baixa ocupação e
vermelho indica maior concentração. As setas mostram a velocidade média dos
agentes dentro de cada célula. A medida `pico de densidade` é relativa ao
tamanho da célula e ao raio de suavização; ela ainda não corresponde a pessoas
por metro quadrado.

## Limites científicos

O movimento atual é uma heurística simples de destino + separação local. Ele
não implementa Social Force, Lattice Boltzmann ou Navier–Stokes. O campo de
densidade também não prova capacidade de antecipar riscos. Esses limites são
intencionais: o MVP 0 fornece um baseline que poderá ser medido e substituído
progressivamente.

Consulte [docs/NOTA_ACADEMICA.md](docs/NOTA_ACADEMICA.md) para a hipótese,
perguntas de pesquisa e próximos experimentos sugeridos.

## Testes

```powershell
python -m unittest discover -s tests -v
```

