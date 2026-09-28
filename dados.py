import json
import os
import re
import sqlite3

from validacoes import (
    TAMANHO_MAXIMO_CATEGORIA,
    TAMANHO_MAXIMO_OBSERVACAO,
    TAMANHO_MAXIMO_PLATAFORMA,
    TAMANHO_MAXIMO_TITULO,
)

PASTA_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")
CAMINHO_BANCO = os.path.join(PASTA_DADOS, "pobrecritic_catalogo.db")
CAMINHO_JSON = os.path.join(PASTA_DADOS, "metacritic_games.json")

NOMES_TITULO = ("title", "name", "game", "game_name", "titulo", "nome")
NOMES_CATEGORIA = ("genre", "genres", "category", "categoria", "genero")
NOMES_PLATAFORMA = ("platform", "platforms", "console", "plataforma")
NOMES_NOTA = (
    "meta_score",
    "metascore",
    "metacritic_score",
    "critic_score",
    "score",
    "user_review",
    "user_score",
    "userscore",
    "rating",
    "nota",
)
NOMES_RESUMO = ("summary", "description", "desc", "resumo", "descricao", "observacao")
VALORES_VAZIOS = ("tbd", "n/a", "null", "none", "nan")


def extrair_lista(conteudo):
    if isinstance(conteudo, list):
        return [registro for registro in conteudo if isinstance(registro, dict)]

    if isinstance(conteudo, dict):
        for valor in conteudo.values():
            if isinstance(valor, list) and valor and isinstance(valor[0], dict):
                return [registro for registro in valor if isinstance(registro, dict)]

        registros = []
        for chave, valor in conteudo.items():
            if isinstance(valor, dict):
                registro = dict(valor)
                registro.setdefault("name", chave)
                registros.append(registro)
        return registros

    return []


def ler_registros_json(caminho):
    with open(caminho, encoding="utf-8-sig") as arquivo:
        texto = arquivo.read()

    try:
        conteudo = json.loads(texto)
    except json.JSONDecodeError:
        conteudo = [json.loads(linha) for linha in texto.splitlines() if linha.strip()]

    registros = extrair_lista(conteudo)

    if not registros:
        raise ValueError("O arquivo JSON não contém jogos reconhecíveis.")

    return registros


def dividir_categorias(texto):
    return [parte.strip() for parte in re.split(r"[,;|]", texto) if parte.strip()]


def obter_campo(registro, nomes, juntar_lista=False):
    chaves = {
        str(chave).strip().lower().replace(" ", "_"): valor
        for chave, valor in registro.items()
    }

    for nome in nomes:
        valor = chaves.get(nome)

        if isinstance(valor, (list, tuple)):
            if juntar_lista:
                valor = ", ".join(str(item).strip() for item in valor if str(item).strip())
            else:
                valor = valor[0] if valor else None

        if valor is None:
            continue

        texto = str(valor).strip()
        if texto and texto.lower() not in VALORES_VAZIOS:
            return texto

    return None


def converter_nota(texto):
    if texto is None:
        return None

    try:
        valor = float(texto.replace(",", "."))
    except ValueError:
        return None

    if valor != valor or valor < 0:
        return None

    if valor > 10:
        valor = valor / 10

    return round(min(valor, 10), 1)


def montar_jogo(registro):
    titulo = obter_campo(registro, NOMES_TITULO)

    if not titulo:
        return None

    categoria = obter_campo(registro, NOMES_CATEGORIA, juntar_lista=True) or "Outro"
    plataforma = obter_campo(registro, NOMES_PLATAFORMA) or "Não informada"
    nota = converter_nota(obter_campo(registro, NOMES_NOTA))
    resumo = obter_campo(registro, NOMES_RESUMO) or ""

    if len(resumo) > TAMANHO_MAXIMO_OBSERVACAO:
        resumo = resumo[: TAMANHO_MAXIMO_OBSERVACAO - 3].rstrip() + "..."

    return (
        titulo[:TAMANHO_MAXIMO_TITULO],
        categoria[:TAMANHO_MAXIMO_CATEGORIA],
        plataforma[:TAMANHO_MAXIMO_PLATAFORMA],
        nota,
        "-",
        resumo,
        0,
    )


class BancoDados:

    def __init__(self, caminho=CAMINHO_BANCO, caminho_json=CAMINHO_JSON):
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        self.conexao = sqlite3.connect(caminho)
        self.conexao.row_factory = sqlite3.Row
        self.criar_tabela(caminho_json)

    def criar_tabela(self, caminho_json):
        existia = self.conexao.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'jogos'"
        ).fetchone()

        versao = self.conexao.execute("PRAGMA user_version").fetchone()[0]

        jogos = []
        if not existia or versao < 2:
            try:
                jogos = self.carregar_jogos_json(caminho_json)
            except (OSError, ValueError):
                if not existia:
                    raise

        with self.conexao:
            self.conexao.execute(
                """
                CREATE TABLE IF NOT EXISTS jogos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL COLLATE NOCASE,
                    categoria TEXT NOT NULL,
                    plataforma TEXT NOT NULL COLLATE NOCASE,
                    nota REAL CHECK (nota IS NULL OR (nota >= 0 AND nota <= 10)),
                    status TEXT NOT NULL,
                    observacao TEXT NOT NULL DEFAULT '',
                    desejo INTEGER NOT NULL DEFAULT 0,
                    UNIQUE (titulo, plataforma)
                )
                """
            )

            if existia and versao < 1:
                self.conexao.execute(
                    "UPDATE jogos SET status = '-' WHERE status = 'Quero jogar'"
                )

            if existia and versao < 2 and jogos:
                self.completar_categorias(jogos)

            self.conexao.execute("PRAGMA user_version = 2")

            if not existia and jogos:
                self.conexao.executemany(
                    """
                    INSERT OR IGNORE INTO jogos
                        (titulo, categoria, plataforma, nota, status, observacao, desejo)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    jogos,
                )

    def carregar_jogos_json(self, caminho_json):
        registros = ler_registros_json(caminho_json)
        jogos = [montar_jogo(registro) for registro in registros]
        jogos = [jogo for jogo in jogos if jogo is not None]

        if not jogos:
            raise ValueError("Nenhum jogo com título foi encontrado no arquivo JSON.")

        return jogos

    def completar_categorias(self, jogos):
        atuais = {
            (linha["titulo"].casefold(), linha["plataforma"].casefold()): (
                linha["id"],
                linha["categoria"],
            )
            for linha in self.conexao.execute(
                "SELECT id, titulo, plataforma, categoria FROM jogos"
            )
        }

        atualizacoes = []
        for titulo, categoria, plataforma, *_ in jogos:
            atual = atuais.get((titulo.casefold(), plataforma.casefold()))

            if (
                atual
                and categoria != atual[1]
                and categoria.casefold().startswith(atual[1].casefold())
            ):
                atualizacoes.append((categoria, atual[0]))

        self.conexao.executemany(
            "UPDATE jogos SET categoria = ? WHERE id = ?", atualizacoes
        )

    def listar(
        self,
        busca="",
        categoria="Todas",
        plataforma="Todas",
        status="Todos",
        apenas_desejos=False,
    ):
        consulta = "SELECT * FROM jogos WHERE 1 = 1"
        parametros = []

        if plataforma != "Todas":
            consulta += " AND plataforma = ?"
            parametros.append(plataforma)

        if status != "Todos":
            consulta += " AND status = ?"
            parametros.append(status)

        if apenas_desejos:
            consulta += " AND desejo = 1"

        consulta += " ORDER BY titulo COLLATE NOCASE, plataforma COLLATE NOCASE"
        linhas = self.conexao.execute(consulta, parametros).fetchall()

        if categoria != "Todas":
            alvo = categoria.casefold()
            linhas = [
                linha
                for linha in linhas
                if alvo in [item.casefold() for item in dividir_categorias(linha["categoria"])]
            ]

        termo = busca.strip().casefold()
        if termo:
            linhas = [linha for linha in linhas if termo in linha["titulo"].casefold()]

        return linhas

    def categorias(self):
        linhas = self.conexao.execute("SELECT DISTINCT categoria FROM jogos").fetchall()
        unicas = {}
        for linha in linhas:
            for item in dividir_categorias(linha["categoria"]):
                unicas.setdefault(item.casefold(), item)
        return [unicas[chave] for chave in sorted(unicas)]

    def plataformas(self):
        linhas = self.conexao.execute(
            "SELECT DISTINCT plataforma FROM jogos ORDER BY plataforma COLLATE NOCASE"
        ).fetchall()
        return [linha["plataforma"] for linha in linhas]

    def obter(self, jogo_id):
        return self.conexao.execute(
            "SELECT * FROM jogos WHERE id = ?", (jogo_id,)
        ).fetchone()

    def existe_titulo(self, titulo, plataforma, ignorar_id=None):
        linha = self.conexao.execute(
            "SELECT id FROM jogos WHERE titulo = ? AND plataforma = ? AND id IS NOT ?",
            (titulo, plataforma, ignorar_id),
        ).fetchone()
        return linha is not None

    def inserir(self, dados):
        with self.conexao:
            cursor = self.conexao.execute(
                """
                INSERT INTO jogos (titulo, categoria, plataforma, nota, status, observacao, desejo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    dados["titulo"],
                    dados["categoria"],
                    dados["plataforma"],
                    dados["nota"],
                    dados["status"],
                    dados["observacao"],
                    dados["desejo"],
                ),
            )
        return cursor.lastrowid

    def atualizar(self, jogo_id, dados):
        with self.conexao:
            self.conexao.execute(
                """
                UPDATE jogos
                SET titulo = ?, categoria = ?, plataforma = ?, nota = ?,
                    status = ?, observacao = ?, desejo = ?
                WHERE id = ?
                """,
                (
                    dados["titulo"],
                    dados["categoria"],
                    dados["plataforma"],
                    dados["nota"],
                    dados["status"],
                    dados["observacao"],
                    dados["desejo"],
                    jogo_id,
                ),
            )

    def excluir(self, jogo_id):
        with self.conexao:
            self.conexao.execute("DELETE FROM jogos WHERE id = ?", (jogo_id,))

    def alternar_desejo(self, jogo_id):
        with self.conexao:
            self.conexao.execute(
                "UPDATE jogos SET desejo = 1 - desejo WHERE id = ?", (jogo_id,)
            )
        jogo = self.obter(jogo_id)
        return bool(jogo["desejo"]) if jogo else False

    def definir_status(self, jogo_id, status):
        with self.conexao:
            self.conexao.execute(
                "UPDATE jogos SET status = ? WHERE id = ?", (status, jogo_id)
            )

    def remover_desejo(self, jogo_id):
        with self.conexao:
            self.conexao.execute(
                "UPDATE jogos SET desejo = 0 WHERE id = ?", (jogo_id,)
            )

    def fechar(self):
        self.conexao.close()