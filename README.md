# Dashboard da Aprovação

Esta aplicação é uma ferramenta estratégica desenvolvida para o mercado de educação. O sistema processa as notas do ENEM inseridas pelo usuário e aplica, em tempo real, os pesos específicos de cada universidade e curso cadastrados no banco de dados.

O objetivo é resolver a complexidade do cálculo manual de médias ponderadas, permitindo que o estudante descubra instantaneamente em quais instituições sua nota possui maior valor competitivo.

## O Problema

No SISU (Sistema de Seleção Unificada), cada universidade tem autonomia para atribuir pesos diferentes às áreas do conhecimento (Redação, Matemática, etc.). Um aluno com nota alta em Matemática, por exemplo, terá uma média final muito superior em uma universidade que atribui peso 3 para essa matéria, em comparação a outra que atribui peso 1.

Calcular isso manualmente para centenas de opções é inviável. Esta ferramenta automatiza esse processo, servindo também como um ponto de captação de potenciais alunos (leads) para instituições de ensino ou cursos preparatórios.

## Funcionalidades

* **Cálculo Ponderado:** O sistema não faz apenas uma média simples. Ele cruza as 5 notas do usuário com os pesos específicos de cada oferta de curso disponível no banco de dados.
* **Ranking:** Os resultados são ordenados automaticamente da maior média para a menor. Isso mostra ao usuário onde sua nota "rende mais".
* **Módulo de Captura de Leads:** Implementação de um gate de conteúdo. Para visualizar o ranking completo, o usuário deve fornecer Nome, WhatsApp e E-mail. Inclui validação de formulário para garantir dados reais.
* **Validação de Dados:** O sistema impede entradas inválidas (textos, notas acima de 1000 ou negativas), garantindo a integridade do cálculo.
* **Interface Responsiva:** Design limpo e adaptável para dispositivos móveis, focado em usabilidade (UX).

## Arquitetura

O projeto foi desenhado focando em velocidade de resposta e simplicidade de manutenção.

* **Backend:** Python com framework Flask. Optei por essa stack pela robustez matemática e facilidade de manipulação de estruturas de dados.
* **Banco de Dados:** Utilizei uma estrutura baseada em JSON carregado em memória, estrutura essa, que foi obtida por meio de um script simples do tipo "scratcher" que busca na api do site do SISU todos os dados requisitados e, armazenou localmente afim de evitar demora, em vista que o site costuma apresentar muita lentidão nos dias que as inscrições estão abertas.
* *Decisão de Engenharia:* Como os pesos das universidades não mudam a cada segundo, não havia necessidade de um banco SQL pesado. Carregar o JSON na memória RAM do servidor garante que o cálculo de milhares de cursos ocorra em milissegundos, eliminando latência.
* **Frontend:** HTML5, CSS3 e JavaScript para validações no lado do cliente, reduzindo a carga no servidor.
 
## Estrutura de Arquivos

* `app.py`: Controlador principal. Contém a lógica de rotas, processamento do formulário e o algoritmo de cálculo de média ponderada.
* `templates/index.html`: Interface do usuário. Contém o formulário, o script do modal de captura e a lógica de exibição dos resultados (Jinja2).
* `banco_de_dados_completo.json`: Fonte da verdade contendo cursos, universidades e seus respectivos pesos por matéria.

## Autor

Desenvolvedor focado em criar soluções eficientes que aliam engenharia de software e geração de lucro para empresas 

Esse é o meu primeiro projeto, em breve irei adicionar novas funcionalidades, estou o utilizando para aprender na prática o que  o mercado busca, para não ficar preso apenas à teoria.
,Claudio Monstans
Linkedin: https://www.linkedin.com/in/cmonstans
