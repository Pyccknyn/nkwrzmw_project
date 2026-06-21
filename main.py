from __future__ import annotations

import argparse
import os
import sys

from dijkstra import (
    dijkstra,
    dijkstra_paths,
    find_best_runway,
    reconstruct_path,
    total_cost,
)
from graph_io import load_graph

LINE = "=" * 62
DASH = "-" * 62


def base_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def city_label(vertex: int, capital: int) -> str:
    if vertex == capital:
        return "Santo Subito"
    return f"Miasto {vertex}"


def run(filename: str, capital: int) -> None:
    if not os.path.isabs(filename):
        filename = os.path.join(base_dir(), filename)

    print(LINE)
    print("      EL NINO AIRLINES - PAS STARTOWY SAN ESCOBAR")
    print(LINE)

    try:
        graph = load_graph(filename)
    except FileNotFoundError:
        print(f"\nBlad: Nie znaleziono pliku '{filename}'")
        sys.exit(1)
    except ValueError as e:
        print(f"\nBlad: {e}")
        sys.exit(1)

    if capital < 1 or capital > graph.n:
        print(f"\nBlad: Stolica musi byc miedzy 1 a {graph.n}")
        sys.exit(1)

    n_cities = graph.n
    n_edges = len(graph.edges)
    print(f"\nMapa zaladowana: {n_cities} miast, {n_edges} odcinkow autostrad")
    print(f"Stolica: Santo Subito (wierzcholek {capital})\n")

    orig_distances = dijkstra(graph, capital)
    orig_cost = total_cost(orig_distances, capital)
    print(f"Suma odleglosci (oryginalny graf): {orig_cost:.1f}")

    print(f"\n{DASH}")
    print("  SZUKANIE OPTYMALNEGO ODCINKA POD PAS STARTOWY...")
    print(DASH)

    best_edge_id, best_cost = find_best_runway(graph, capital)

    if best_edge_id is None:
        print("\nBrak dostepnego odcinka!")
        print("Kazdy odcinek jest mostem - usuniecie dowolnego")
        print("odcieloby jakies miasto od stolicy.")
        sys.exit(1)

    u, v, w = graph.edges[best_edge_id]
    increase = best_cost - orig_cost

    print(f"\n  WYBRANY ODCINEK POD PAS STARTOWY:")
    print(f"    {city_label(u, capital)} <-> {city_label(v, capital)}"
          f"  (dlugosc: {w:.0f})")
    print(f"\n  Suma odleglosci po usunieciu : {best_cost:.1f}")
    if increase == 0:
        print("  Wzrost sumy odleglosci      : +0.0  (odcinek niekrytyczny!)")
    else:
        print(f"  Wzrost sumy odleglosci      : +{increase:.1f}")

    print(f"\n{DASH}")
    print("  NAJKROTSZE DROGI ZE STOLICY PO USUNIECIU ODCINKA")
    print(DASH)

    distances, parents = dijkstra_paths(graph, capital, banned_edge=best_edge_id)

    for dest in range(1, graph.n + 1):
        if dest == capital:
            continue
        d = distances[dest]
        label = city_label(dest, capital)
        if d == float("inf"):
            print(f"  {label:<22} NIEDOSTEPNE")
            continue
        path = reconstruct_path(parents, capital, dest)
        path_str = " -> ".join(str(node) for node in path)
        print(f"  {label:<22} dl.: {d:6.1f}   droga: {path_str}")

    print(f"\n{LINE}")
    print(f"  OPTYMALNA SUMA ODLEGLOSCI: {best_cost:.1f}")
    print(LINE)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="El Nino Airlines - optymalizacja pasa startowego San Escobar",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\nPrzyklad:  ElNino.exe --plik dane.txt --stolica 1",
    )
    parser.add_argument(
        "--plik", default="dane.txt",
        help="Plik z danymi grafu (domyslnie: dane.txt)"
    )
    parser.add_argument(
        "--stolica", type=int, default=1,
        help="Numer wierzcholka stolicy (domyslnie: 1)"
    )
    args = parser.parse_args()

    run(args.plik, args.stolica)

    if getattr(sys, "frozen", False) and len(sys.argv) == 1:
        try:
            input("\nNacisnij Enter aby zakonczyc...")
        except (EOFError, KeyboardInterrupt):
            pass


if __name__ == "__main__":
    main()
