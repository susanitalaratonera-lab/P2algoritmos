"""Módulo principal: Intérprete de scripts de comandos para grafos.

Este script actúa como o motor de execución (REPL por lotes) da práctica:
1. Le un arquivo de texto secuencialmente liña por liña.
2. Limpa espazos en branco e ignora comentarios (liñas que inician con '#').
3. Tokeniza a instrución usando `shlex.split`, permitindo cadeas con espazos entre comiñas.
4. Despacha dinamicamente a función correspondente do paquete `commands` usando introspección/reflexión (`getattr`).
5. Pasa o grafo actual como primeiro argumento e actualiza a súa referencia co valor retornado polo comando,
   garantindo a persistencia do estado entre sucesivas instrucións.
6. Manexa con localización de liña calquera erro sintáctico, de chamada ou de acceso a ficheiros.

Uso dende a liña de comandos:
    python interpreter.py <ruta_ao_arquivo_de_comandos>

Exemplo de arquivo de comandos:
    # Cargar o grafo de satélites
    LOAD data.eval.json 200000
    # Imprimir a matriz de adxacencia
    PRINT
"""

from __future__ import annotations

# Módulos estándar de Python:
# argparse: Permite construír interfaces de liña de comandos robustas con validación de argumentos e flags de axuda (-h/--help).
import argparse
# Path: Representa rutas do sistema de ficheiros de forma orientada a obxectos e independente do SO (Windows/Linux/macOS).
from pathlib import Path
# shlex: Tokenizador léxico estilo shell POSIX, esencial para separar palabras pero conservando cadeas entre comiñas como un solo token.
import shlex
# sys: Proporciona acceso a variables e funcións do sistema, como sys.stderr (canal de erros) e sys.exit (código de saída do proceso).
import sys

# Paquetes propios do proxecto:
# commands: Paquete que contén as funcións executables asociadas a cada comando dispoñible.
import commands
# Graph: Clase que representa a estrutura de datos grafo sobre a cal operan os comandos.
from graphs import Graph


def main() -> None:
    """Punto de entrada principal para a execución do intérprete.

    Configura o analizador de argumentos de consola, abre e procesa o arquivo de script
    indicado e xestiona o ciclo de vida do grafo e as posibles excepcións.
    """
    # 1. Configuración do analizador de argumentos de liña de comandos (CLI)
    parser = argparse.ArgumentParser(
        description="Analiza e executa secuencialmente un arquivo de comandos de grafos."
    )
    # Engádese o argumento posicional obrigatorio 'file', especificando que debe converterse nun obxecto Path
    parser.add_argument(
        "file",
        type=Path,
        help="Ruta ao arquivo de texto cos comandos a executar.",
    )
    # Procesa os argumentos pasados ao invocar o script (ex: sys.argv[1:]); se falta o argumento ou se pasa -h, finaliza amosando axuda
    args = parser.parse_args()

    # 2. Inicialización do estado do grafo
    # Variable que manterá a referencia ao grafo en memoria ao longo de toda a execución do script.
    # Inicialmente é None ata que unha instrución (como CREATE ou LOAD) o instancie.
    graph: Graph | None = None

    # 3. Apertura e lectura segura do arquivo de comandos
    try:
        # Abre o arquivo en modo lectura de texto con codificación UTF-8 explícita
        with args.file.open("r", encoding="utf-8") as f:
            # enumerate(f, start=1) itera liña a liña proporcionando o número de liña (base 1) para diagnósticos de erro
            for line_number, line in enumerate(f, start=1):
                # Elimina espazos en branco iniciais e finais, así como saltos de liña (\r, \n)
                clean_line = line.strip()

                # Se a liña está baleira ou é un comentario (inicia con '#'), descártase e pásase á seguinte
                if not clean_line or clean_line.startswith("#"):
                    continue

                # Tokenización léxica: divide a liña en palabras, respectando frases entre comiñas como un único argumento.
                # Exemplo: 'LOAD "data.json" 200000' -> ['LOAD', 'data.json', '200000']
                tokens = shlex.split(clean_line)

                # Desempaquetado: o primeiro elemento é o nome do comando e o resto son os seus argumentos
                command, arguments = tokens[0], tokens[1:]

                # Inspección de comandos válidos:
                # Obtén a lista de nomes de comandos rexistrados no módulo commands (excluíndo atributos internos que inician con '_')
                available_cmds = [
                    cmd.upper() for cmd in vars(commands).keys() if not cmd.startswith("_")
                ]

                # 1. Búsqueda e resolución dinámica do comando
                try:
                    # Introspección dinámica: busca no paquete commands unha función co nome do comando en minúsculas (ex: 'PRINT' -> commands.print)
                    command_func = getattr(commands, command.lower())
                except AttributeError:
                    # Prodúcese se a función co nome do comando non existe no paquete commands
                    cmds_str = ", ".join(f"'{cmd}'" for cmd in available_cmds)
                    print(
                        f"[Línea {line_number}] Error: Comando '{command}' non recoñecido. "
                        f"Comandos dispoñibles: {cmds_str}",
                        file=sys.stderr,
                    )
                    # Detén a execución retornando código de erro 1 ao sistema operativo
                    sys.exit(1)

                # 2. Execución da función do comando
                try:
                    # Execución do comando:
                    # Invócase a función pasando o grafo actual como primeiro argumento e desempaquetando os argumentos restantes (*arguments).
                    # O valor retornado reempraza a referencia en 'graph', permitindo que os comandos modifiquen ou creen o grafo.
                    graph = command_func(graph, *arguments)
                except TypeError as exc:
                    # Prodúcese se o número de argumentos pasados non coincide coa signatura da función invocada
                    print(
                        f"[Línea {line_number}] Error: Chamada inválida ao comando '{command}' "
                        f"con argumentos {arguments}. Detalle: {exc}",
                        file=sys.stderr,
                    )
                    # Detén a execución retornando código de erro 1 ao sistema operativo
                    sys.exit(1)

    # 4. Manexo de excepcións de entrada/salída (I/O) ao acceder ao arquivo
    except FileNotFoundError:
        # Captúrase se a ruta pasada non corresponde a un arquivo existente no sistema
        print(f"Error: O arquivo '{args.file}' non existe.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        # Captúrase se o proceso actual non dispón de permisos do SO para ler o arquivo
        print(f"Error: Permiso denegado ao ler '{args.file}'.", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        # Captúrase se o arquivo contén bytes non válidos para a codificación UTF-8
        print(f"Error: Non se puido decodificar '{args.file}' como UTF-8.", file=sys.stderr)
        sys.exit(1)


# Garante que main() solo se execute cando o arquivo se invoca directamente dende a consola,
# evitando que se dispare se o módulo é importado dende outro script ou test.
if __name__ == "__main__":
    main()