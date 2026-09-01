---
name: refinar-specs
description: Use only when the user explicitly invokes refine-specs to question and update an active specification set as decisions settle.
disable-model-invocation: true
---

<what-to-do>

Entreviste-me implacavelmente sobre cada aspecto deste plano (focado na pasta `Specs`) até chegarmos a um entendimento compartilhado. Percorra cada ramificação da árvore de design, resolvendo as dependências entre as decisões uma a uma. Para cada pergunta, forneça a sua recomendação de resposta.

Faça as perguntas uma de cada vez, aguardando o meu feedback sobre cada uma antes de continuar.

Se uma pergunta puder ser respondida explorando a base de código, explore a base de código em vez de perguntar.

</what-to-do>

<supporting-info>

## Consciência de Domínio

Durante a exploração da base de código, procure pela documentação existente focada na pipeline orientada a documentos (Document-Driven Pipeline):

### Estrutura de Arquivos

O projeto utiliza uma pasta `Specs` para o planejamento de features. A estrutura geralmente inclui:

```text
.omp/
├── Specs/
│   └── [nome-da-feature]/
│       ├── PRD.md
│       ├── ARCHITECTURE.md
│       ├── DESIGN.md
│       ├── INTEGRATION.md
│       ├── TASKS.md
│       └── POOP.md
├── agents/
├── rules/
└── skills/
main-tscript-tr-backoffice/src/
ms-bff-java-tr-backoffice/src/
```

Crie ou atualize os arquivos de forma sob demanda (lazy) — apenas quando houver algo concreto para escrever. Se o `PRD.md` não existir, crie-o quando o primeiro termo ou regra de negócio for resolvido.

## Durante a sessão

### Desafiar contra o PRD.md (Glossário)

Quando o usuário usar um termo que conflite com a linguagem existente no `PRD.md` ou nas especificações, aponte isso imediatamente. "O seu `PRD.md` define 'cancelamento' como X, mas você parece querer dizer Y — qual é o correto?"

### Refinar linguagem vaga

Quando o usuário usar termos vagos ou sobrecarregados, proponha um termo canônico e preciso. "Você está dizendo 'conta' — você se refere ao Cliente ou ao Usuário? São coisas diferentes."

### Discutir cenários concretos

Quando as relações de domínio estiverem sendo discutidas, teste-as com cenários específicos. Invente cenários que explorem casos extremos (edge cases) e force o usuário a ser preciso sobre as fronteiras entre os conceitos.

### Cruzamento com o código

Quando o usuário afirmar como algo funciona, verifique se o código concorda. Se encontrar uma contradição, traga isso à tona: "O seu código cancela Pedidos inteiros, mas você acabou de dizer que o cancelamento parcial é possível — qual está correto?"

### Atualizar a pasta Specs em tempo real (Inline)

Quando um termo for resolvido ou uma decisão arquitetural for tomada, atualize o arquivo relevante na pasta `Specs` (seja o `PRD.md` para conceitos de domínio, ou os arquivos de design técnico para decisões de arquitetura e trade-offs) imediatamente. Não acumule essas atualizações para o final — capture-as à medida que acontecem.

O `PRD.md` deve ser totalmente desprovido de detalhes de implementação. Não o trate como um rascunho ou repositório de decisões de código; ele é a fonte da verdade do negócio e linguagem ubíqua. As decisões técnicas e trade-offs (antigos ADRs) devem ser documentados nas especificações técnicas dentro da pasta da feature em `Specs/`.

</supporting-info>
