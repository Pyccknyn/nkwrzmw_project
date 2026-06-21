# El Niño — pas startowy w San Escobar

Minister transportu Republiki San Escobar musi przerobić **jeden odcinek** sieci
autostrad na pas startowy dla narodowych linii lotniczych El Niño. Trzeba wybrać
ten odcinek tak, aby po jego usunięciu **suma najkrótszych odległości ze stolicy
(Santo Subito) do wszystkich pozostałych miast** była jak najmniejsza.

---

## Uruchomienie

```
ElNino.exe --plik plik.txt
ElNino.exe --plik *ścieżka do pliku* --stolica 2
```

Plik musi być w formacie `wierzcholek1,wierzcholek2,waga` — jeden odcinek na linię:

```
1,2,4
1,3,2
2,3,1
```

Domyślnie program używa `dane.txt` znajdującego się obok pliku exe.

---

## 1. Model problemu

- Sieć autostrad to **graf nieskierowany ważony** `G = (V, E)`:
  - wierzchołki `V` = miasta,
  - krawędzie `E` = odcinki autostrad, waga = długość odcinka (≥ 0).
- Wyróżniony wierzchołek `s` = stolica **Santo Subito**.
- Definiujemy koszt grafu:

  ```
  cost(G) = Σ_{v ∈ V, v ≠ s} dist_G(s, v)
  ```

  gdzie `dist_G(s, v)` to długość najkrótszej ścieżki ze `s` do `v` w grafie `G`.
  Jeśli `v` jest nieosiągalne, traktujemy `dist = +∞`.

### Zadanie

Znajdź krawędź `e* ∈ E`, której usunięcie minimalizuje `cost(G − e*)`:

```
e* = argmin_{e ∈ E} cost(G − e)
```

Zwróć `e*` oraz uzyskaną sumę odległości.

### Założenia (warto potwierdzić w treści zadania)

- Usuwamy **dokładnie jedną** krawędź (nie zero, nie więcej).
- Graf po usunięciu musi pozostać **spójny** — inaczej któreś miasto byłoby
  odcięte od stolicy (koszt `+∞`). Takie krawędzie (mosty) odrzucamy.
- Wagi nieujemne → można używać Dijkstry.

---

## 2. Kluczowa obserwacja

Usunięcie krawędzi **nigdy nie zmniejsza** żadnej odległości — może je tylko
zwiększyć lub zostawić bez zmian. Mimo to usunięcie potrafi być korzystne tylko
w jednym sensie: _nie istnieje_ taka krawędź, której usunięcie obniża `cost`
poniżej kosztu pełnego grafu. **Najlepszym wyborem jest więc krawędź, której
usunięcie psuje sumę najmniej.**

To zmienia pytanie z „którą usunąć, żeby było lepiej” na **„którą poświęcić,
żeby stracić jak najmniej”** — i dokładnie tak należy czytać treść: jeden odcinek
_musi_ zniknąć (zostaje pasem startowym), minimalizujemy szkodę.

> Wniosek: jeśli treść dopuszcza „nie usuwać nic”, odpowiedzią byłby pełny graf.
> Skoro odcinek **trzeba** poświęcić, szukamy najmniej szkodliwego.

---

## 3. Algorytm — podejście bazowe (brute force)

Najprostsze poprawne rozwiązanie:

```
najlepszy_koszt = +∞
najlepsza_krawedz = brak
dla każdej krawędzi e ∈ E:
    G' = G − e
    d = Dijkstra(G', s)            # najkrótsze ścieżki ze stolicy
    c = suma d[v] dla v ≠ s
    jeśli c < najlepszy_koszt:
        najlepszy_koszt = c
        najlepsza_krawedz = e
zwróć (najlepsza_krawedz, najlepszy_koszt)
```

**Złożoność:** `|E|` przebiegów Dijkstry → `O(|E| · (|E| + |V|) log |V|)`.
Dla małych i średnich grafów (setki–tysiące krawędzi) to w zupełności wystarcza
i jest łatwe do udowodnienia poprawności.

---

## 4. Optymalizacja (opcjonalna, dla dużych grafów)

Większość krawędzi w ogóle nie zmienia odległości po usunięciu. Liczy się tylko
to, co dzieje się na **drzewie najkrótszych ścieżek** (SPT) ze stolicy:

- Krawędzie **spoza** SPT — ich usunięcie nie zmienia żadnej odległości
  (`cost` bez zmian). Można je pominąć.
- Krawędzie **należące do SPT** — ich usunięcie odcina poddrzewo i wymusza
  objazd. Tylko te warto przeliczać.

To redukuje liczbę kosztownych przeliczeń z `|E|` do co najwyżej `|V| − 1`.
Najpierw policz SPT raz, potem przeliczaj tylko krawędzie drzewa. Dla typowych
rozmiarów z zadania brute force jednak wystarcza — optymalizację zostaw na koniec.

---

## 5. Podział na zadania

Zadania ułożone tak, by dało się je rozdać i robić równolegle. Każde ma jasne
wejście/wyjście i własny test.

### Zadanie 1 — Wczytywanie i reprezentacja grafu

- Parser wejścia: liczba miast, krawędzie `(u, v, waga)`, indeks stolicy.
- Struktura: lista sąsiedztwa `adj[u] = [(v, waga), ...]`.
- **Wyjście:** obiekt grafu + `s`.
- **Test:** mały graf wczytany i wypisany zgadza się z wejściem.

### Zadanie 2 — Dijkstra (suma odległości)

- Funkcja `shortest_paths(graph, s)` → tablica odległości.
- Funkcja `total_cost(distances, s)` → suma (z obsługą `+∞`).
- **Wyjście:** `cost(G)` dla zadanego grafu.
- **Test:** ręcznie policzony mały graf.

### Zadanie 3 — Usuwanie krawędzi i ocena

- `remove_edge(graph, e)` → kopia grafu bez `e` (albo widok/maskowanie).
- Pętla po krawędziach + zliczanie najlepszego wyniku (rozdział 3).
- Wykrycie rozspójnienia → koszt `+∞`, krawędź odrzucona.
- **Wyjście:** `(najlepsza_krawedz, najlepszy_koszt)`.
- **Test:** graf z oczywistym mostem — most nie może zostać wybrany.

### Zadanie 4 — Wynik i interfejs

- Wypisanie której krawędzi (które miasta łączy) + uzyskana suma.
- Opcjonalnie porównanie z kosztem pełnego grafu (ile „kosztuje” poświęcenie).
- **Test:** end-to-end na przykładzie z rozdziału 6.

### Zadanie 5 (opcjonalne) — Optymalizacja SPT

- Ogranicz przeliczanie do krawędzi drzewa najkrótszych ścieżek (rozdział 4).
- **Test:** wynik identyczny jak brute force na losowych grafach (porównanie).

### Zadanie 6 — Testy i przypadki brzegowe

- Graf z jednym miastem (brak krawędzi → brak rozwiązania / komunikat).
- Graf, gdzie każda krawędź jest mostem (np. linia) — brak dopuszczalnego ruchu.
- Krawędzie wielokrotne między tymi samymi miastami.
- Duży graf losowy (sprawdzenie wydajności).

---

## 6. Przykład

```
Miasta: S, A, B, C, D     (S = Santo Subito)
Krawędzie:
  S-A : 1
  S-C : 4
  A-B : 1
  A-C : 1
  B-D : 1
  C-D : 1
```

Pełny graf: `dist = {A:1, B:2, C:2, D:3}`, `cost = 8`.

Usunięcie `A-C` zmusza `C` na trasę `S-A-B-D-C` lub przez `S-C(4)` → `C` rośnie
do 3 (przez most poddrzewa) i suma rośnie. Usunięcie `S-C` (waga 4, prawie
nieużywana) prawie nic nie psuje → kandydat na `e*`. Algorytm sprawdza wszystkie
i wybiera ten, który daje najmniejszą sumę.

---

## 7. Podział odpowiedzialności (4 osoby, wspólny projekt)

Projekt oddajemy **razem, jako całość** — poniżej jest tylko podział, kto za co
odpowiada w kodzie. Zależność modułów: **Eryk → Kacper → Filip → Sebastian**.
Żeby nie blokować się nawzajem, na starcie ustalamy wspólny kontrakt (sekcja
niżej) i każdy pracuje przeciwko stubom — np. Kacper testuje Dijkstrę na ręcznie
sklejonym grafie, zanim parser Eryka będzie gotowy.

### Eryk Wicher — graf i wczytywanie

- Odpowiada za klasę `Graph(n)`, metodę `add_edge(u, v, w)`, listę sąsiedztwa
  `adj[u] = [(v, waga, eid)]` i listę `self.edges` (każda krawędź raz).
- Parser wejścia: liczba miast, krawędzie `(u, v, waga)`, indeks stolicy `src`.
- **Pilnuje, by:** mały graf wczytany i wypisany = wejście; krawędzie wielokrotne działają.

### Kacper Łucki — Dijkstra i suma odległości

- Odpowiada za `dijkstra(graph, src, banned_edge=None)` → tablica odległości (z `inf`).
- `total_cost(dist, src)` → suma odległości do miast ≠ stolica; `inf` gdy coś odcięte.
- Parametr `banned_edge` jest potem używany przez moduł Filipa.
- **Pilnuje, by:** ręcznie policzony mały graf się zgadzał; nieosiągalne miasto → `inf`.

### Filip Bąk — usuwanie krawędzi i wybór e\*

- Odpowiada za `best_edge_to_remove(graph, src)` — pętla po wszystkich `eid`,
  wywołanie Dijkstry z `banned_edge=eid`, wybór minimalnego kosztu.
- Most (krawędź rozspajająca) daje `inf` → automatycznie odrzucony.
- (Opcjonalnie, jeśli starczy czasu) optymalizacja po drzewie najkrótszych ścieżek.
- **Pilnuje, by:** w grafie z oczywistym mostem most nie został wybrany.

### Sebastian Broda — wynik i integracja

- Odpowiada za `solve(graph, src)` → słownik: koszt bazowy, najlepsza krawędź,
  koszt po usunięciu, strata.
- Ładny wypis: które miasta łączy odcinek + uzyskana suma + porównanie z pełnym grafem.
- Spina moduły całego zespołu, odpala **end-to-end** i prowadzi zestaw testów
  brzegowych (jedno miasto, sama linia = same mosty, duży graf losowy, krawędzie wielokrotne).

### Kontrakt integracyjny (uzgadniamy raz, na początku)

- Graf: `adj[u] = [(v, waga, eid)]`, krawędzie w `self.edges` (każda raz).
- Stolica = indeks `src`. Odległość nieosiągalna = `inf`. Koszt rozspojenia = `inf`.
- Każdy commituje swój moduł wraz z testami do **wspólnego repozytorium**;
  na koniec oddajemy projekt jako jedną całość.

---

## 8. Struktura projektu (propozycja)

```
san-escobar/
├── README.md          # ten plik
├── solution.py        # referencyjna implementacja (brute force + opcja SPT)
└── tests/
    └── test_basic.py  # przykłady i przypadki brzegowe
```

Uruchomienie referencji:

```bash
python solution.py
```
