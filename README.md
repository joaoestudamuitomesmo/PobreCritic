<img width="225" height="225" alt="image" src="https://github.com/user-attachments/assets/ae618b17-2303-4d39-9ab1-1ff985dfd92d" />

## Interface em TKInter
Uma aplicação desenvolvida em Python que demonstra uma interface com tema escuro e componentes personalizados utilizando a biblioteca nativa tkinter e ttk.

## Objetivo
O objetivo principal deste projeto é criar um catálogo de jogos que permita analisar opções de jogos por suas plataformas e notas, adicionar novos jogos ao catálogo, adicionar jogos à lista de desejos.

## Requisitos
Para executar este projeto, necessita de ter instalado no seu sistema:

Python (>= 3.8).

Bibliotecas padrão do Python incluídas por defeito (o projeto utiliza tkinter, json, etc.).

## Instalação
Clone o repositório ou descarregue os ficheiros do projeto para a sua máquina local:

Bash
git clone https://github.com/joaoestudamuitomesmo/PobreCritic

cd PobreCritic

### Execução
Para iniciar a aplicação, execute o script principal a partir do seu terminal:

Bash
python main.py

## Utilização
Fazer login/cadastro

Ao ser redirecionado para a pagina de catalogo, você pode adicionar jogos a sua lista de desejos, adicionar jogos que não estão no catálogo, filtrar por gênero, plataforma, nome, etc.

## Limitações

Sistema de Login Simulado: A tela de login valida apenas a estrutura do e-mail e o tamanho mínimo da senha, permitindo acesso com qualquer credencial sem consultar um banco de dados de usuários.
Interface com Dimensões Fixas: A aplicação utiliza janelas e elementos com tamanhos fixos (1366x768), podendo apresentar problemas de exibição em telas de menor resolução ou ao redimensionar.
Armazenamento Mono-usuário: Os dados são salvos em um banco de dados SQLite local compartilhado, ou seja, as alterações, notas e lista de desejos afetam toda a aplicação e não ficam vinculadas a uma conta específica.
Dependência de Arquivo Estático: A inserção inicial do catálogo depende diretamente do arquivo `metacritic_games.json` estar presente na pasta `dados/`.
Sem Gestão de Permissões: Qualquer usuário que acessar a aplicação possui privilégios totais para adicionar, alterar ou excluir jogos do catálogo.
