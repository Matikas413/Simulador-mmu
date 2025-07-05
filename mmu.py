import sys
from collections import deque

class Pagina:
    def __init__(self):
        self.V = 0  # Bit de validez
        self.U = 0  # Bit de uso
        self.D = 0  # Bit de escritura
        self.frame = -1  # Frame asignado (-1 si no tiene)

def imprimir_tabla(tabla):
    print("\nP\u00e1gina | V | U | D | Frame")
    print("----------------------------")
    for i, p in enumerate(tabla):
        frame_str = p.frame if p.V == 1 else "-"
        print(f"{i:<7} | {p.V} | {p.U} | {p.D} | {frame_str}")

def simulador_mmu(paginas_virtuales, frames_fisicos, archivo_secuencia):
    tabla = [Pagina() for _ in range(paginas_virtuales)]
    frames_libres = deque(range(frames_fisicos))
    orden_fifo = deque()  # Páginas actualmente cargadas (FIFO)

    with open(archivo_secuencia, "r") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea or len(linea) < 2:
                continue

            tipo = linea[0]
            try:
                num = int(linea[1:])
            except ValueError:
                continue

            if num < 0 or num >= paginas_virtuales:
                continue

            pagina = tabla[num]

            if tipo in ('R', 'W'):
                if pagina.V == 0:
                    if frames_libres:
                        frame = frames_libres.popleft()
                    else:
                        victima = orden_fifo.popleft()
                        frame = tabla[victima].frame
                        tabla[victima] = Pagina()

                    pagina.V = 1
                    pagina.U = 0
                    pagina.D = 0
                    pagina.frame = frame
                    orden_fifo.append(num)

                pagina.U = 1
                if tipo == 'W':
                    pagina.D = 1

            elif tipo == 'F':
                if pagina.V == 1:
                    frame_liberado = pagina.frame
                    pagina.V = 0
                    pagina.U = 0
                    pagina.D = 0
                    pagina.frame = -1
                    if num in orden_fifo:
                        orden_fifo.remove(num)
                    frames_libres.append(frame_liberado)

    imprimir_tabla(tabla)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python mmu.py <paginas> <frames> <archivo_secuencia>")
        sys.exit(1)

    try:
        paginas = int(sys.argv[1])
        frames = int(sys.argv[2])
        archivo = sys.argv[3]
        simulador_mmu(paginas, frames, archivo)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)
