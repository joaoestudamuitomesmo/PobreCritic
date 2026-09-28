import math
import re

CATEGORIAS = (
    "Ação",
    "Aventura",
    "RPG",
    "Estratégia",
    "Esporte",
    "Corrida",
    "Puzzle",
    "Terror",
    "Simulação",
    "Outro",
)

STATUS = ("-", "Quero jogar", "Jogando", "Jogado")

TAMANHO_MINIMO_TITULO = 2
TAMANHO_MAXIMO_TITULO = 80
TAMANHO_MAXIMO_CATEGORIA = 120
TAMANHO_MAXIMO_PLATAFORMA = 40
TAMANHO_MAXIMO_OBSERVACAO = 300
NOTA_MINIMA = 0
NOTA_MAXIMA = 10


def validar_titulo(titulo):
    titulo = titulo.strip()

    if not titulo:
        raise ValueError("Informe o título do jogo.")

    if len(titulo) < TAMANHO_MINIMO_TITULO:
        raise ValueError(
            f"O título deve ter no mínimo {TAMANHO_MINIMO_TITULO} caracteres."
        )

    if len(titulo) > TAMANHO_MAXIMO_TITULO:
        raise ValueError(
            f"O título deve ter no máximo {TAMANHO_MAXIMO_TITULO} caracteres."
        )

    return titulo


def validar_categoria(categoria):
    categoria = categoria.strip()

    if not categoria:
        raise ValueError("Informe a categoria do jogo.")

    if len(categoria) > TAMANHO_MAXIMO_CATEGORIA:
        raise ValueError(
            f"A categoria deve ter no máximo {TAMANHO_MAXIMO_CATEGORIA} caracteres."
        )

    return categoria


def validar_plataforma(plataforma):
    plataforma = plataforma.strip()

    if not plataforma:
        raise ValueError("Informe a plataforma do jogo.")

    if len(plataforma) > TAMANHO_MAXIMO_PLATAFORMA:
        raise ValueError(
            f"A plataforma deve ter no máximo {TAMANHO_MAXIMO_PLATAFORMA} caracteres."
        )

    return plataforma


def validar_status(status):
    if status not in STATUS:
        raise ValueError("Selecione o status do jogo.")

    return status


def validar_nota(nota):
    nota = nota.strip().replace(",", ".")

    if not nota:
        return None

    try:
        valor = float(nota)
    except ValueError:
        raise ValueError("A nota deve ser um número, como 8 ou 7,5.") from None

    if not math.isfinite(valor) or valor < NOTA_MINIMA or valor > NOTA_MAXIMA:
        raise ValueError(f"A nota deve estar entre {NOTA_MINIMA} e {NOTA_MAXIMA}.")

    return round(valor, 1)


def validar_observacao(observacao):
    observacao = observacao.strip()

    if len(observacao) > TAMANHO_MAXIMO_OBSERVACAO:
        raise ValueError(
            f"A observação deve ter no máximo {TAMANHO_MAXIMO_OBSERVACAO} caracteres."
        )

    return observacao


def validar_jogo(titulo, categoria, plataforma, nota, status, observacao, desejo):
    status = validar_status(status)

    return {
        "titulo": validar_titulo(titulo),
        "categoria": validar_categoria(categoria),
        "plataforma": validar_plataforma(plataforma),
        "nota": validar_nota(nota),
        "status": status,
        "observacao": validar_observacao(observacao),
        "desejo": 1 if desejo else 0,
    }


def nota_digitacao_valida(texto):
    return re.fullmatch(r"\d{0,2}([.,]\d?)?", texto) is not None