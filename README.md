# Dashboard da Aprovação

> **Ferramenta estratégica para simulação de notas do SISU e captação de leads.**

Esta aplicação é uma ferramenta desenvolvida para o mercado de educação. O sistema processa as notas do ENEM inseridas pelo usuário e aplica, em tempo real, os pesos específicos de cada universidade e curso cadastrados no banco de dados.

O objetivo é resolver a complexidade do cálculo manual de médias ponderadas, permitindo que o estudante descubra instantaneamente em quais instituições sua nota possui maior valor competitivo.

---

## O Problema

No **SISU (Sistema de Seleção Unificada)**, cada universidade tem autonomia para atribuir pesos diferentes às áreas do conhecimento (Redação, Matemática, etc.).

*Exemplo:* Um aluno com nota alta em Matemática terá uma média final muito superior em uma universidade que atribui **peso 3** para essa matéria, em comparação a outra que atribui **peso 1**.

Calcular isso manualmente para centenas de opções é inviável. Esta ferramenta automatiza esse processo, servindo também como um ponto de captação de potenciais alunos (**leads**) para instituições de ensino ou cursos preparatórios.

## Funcionalidades

* **Cálculo Ponderado em Tempo Real:** O sistema não faz apenas uma média simples. Ele cruza as 5 notas do usuário com os pesos específicos de milhares de ofertas de cursos.
* **Ranking Inteligente:** Os resultados são ordenados automaticamente da maior média para a menor, mostrando onde a nota do aluno "rende mais".
* **Gate de Conteúdo (Captura de Leads):** Para visualizar o resultado, o usuário deve fornecer Nome, E-mail e Telefone.
* **Validação de Dados:** O sistema impede entradas inválidas (notas acima de 1000, textos, etc) e valida o formulário de contato antes do envio.
* **Interface Responsiva:** Design focado em usabilidade (UX), adaptável para celulares e desktops.

## Arquitetura e Decisões Técnicas

O projeto foi desenhado focando em velocidade de resposta e simplicidade de manutenção.

### Backend (Python + Flask)
Optei por essa stack pela robustez matemática e facilidade de manipulação de dados.

### Banco de Dados Híbrido
Para otimizar a performance, utilizei uma abordagem híbrida:
1.  **Cursos e Pesos (Leitura Rápida):** Utilizei uma estrutura baseada em **JSON carregado em memória**.
    * *Decisão de Engenharia:* Como os pesos das universidades não mudam a cada segundo, não havia necessidade de querys pesadas em banco SQL para isso. Carregar o JSON na memória RAM garante que o cálculo de milhares de cursos ocorra em milissegundos.
    * *Origem dos Dados:* Script "scraper" desenvolvido para buscar dados na API pública do SISU.
2.  **Leads (Persistência Segura):** Para salvar os contatos dos alunos, utilizei um banco de dados **MySQL (via TiDB Cloud)**. Isso garante que os dados de negócio fiquem salvos de forma segura e estruturada na nuvem.

### Frontend
HTML5, CSS3 (interno para otimização de load na Vercel) e JavaScript puro para validações no lado do cliente, reduzindo a carga no servidor.

## Autor

**Claudio Monstans**

Desenvolvedor focado em criar soluções eficientes que aliam engenharia de software e geração de lucro para empresas.

Este é o meu primeiro projeto de portfólio. Estou utilizando-o para aplicar na prática as demandas reais do mercado, evitando ficar preso apenas à teoria. Em breve, novas funcionalidades serão adicionadas.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/cmonstans)

---
*Projeto sob licença MIT, entretanto, todos os dados sobre cursos são públicos e pertecem às suas respectivas organizações*
