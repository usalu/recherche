## Semantische Zusammenfassung

Ein **Connector** ist ein möglicher Beziehungspunkt an einem Bauteil.
Ein **Port** gibt diesem Connector seine semantische Rolle.
Eine **Connection** ist gültig, wenn zwei Connectoren **kompatible Ports** haben.

Das System fragt also nicht nur:

```text
Liegen diese zwei Punkte passend zueinander?
```

Sondern vor allem:

```text
Passen diese zwei Verbindungsrollen semantisch zusammen?
```

## Semantische Lesart deiner Ports

Aus deinem Beispiel kann man die Ports so interpretieren:

```text
b-l    = seitliche Verbindungsrolle, Typ l
b-l-m  = seitliche Verbindungsrolle, Typ l-m
b-s    = seitliche Verbindungsrolle, Typ s
b-s-m  = seitliche Verbindungsrolle, Typ s-m

c-t    = vertikale obere Rolle
c-b    = vertikale untere Rolle
```

## Mögliche kompatible Ports

Eine sinnvolle Kompatibilitätslogik für dein Beispiel wäre:

```text
c-t ↔ c-b
```

Das bedeutet:

Ein **oberer vertikaler Anschluss** verbindet sich mit einem **unteren vertikalen Anschluss**.

Beispiel aus deinen Connectoren:

```text
c-p1-l-t verwendet Port c-t
c-p2-l-b verwendet Port c-b
```

Semantische Bedeutung:

```text
Die Oberseite von p1 kann mit der Unterseite von p2 verbunden werden.
Dadurch entsteht eine vertikale Stapel- oder Auflagerbeziehung.
```

Für seitliche Verbindungen wäre eine sinnvolle Paarung:

```text
b-l   ↔ b-s
b-l-m ↔ b-s-m
```

Das bedeutet:

Ein Connector mit der seitlichen Rolle `b-l` verbindet sich mit der komplementären seitlichen Rolle `b-s`.

Ein Connector mit der mittleren/modifizierten Rolle `b-l-m` verbindet sich mit der komplementären Rolle `b-s-m`.

Beispiel:

```text
b-p2-t-t1-c3-l verwendet Port b-l
b-p1-b-t1-c1-r verwendet Port b-s
```

Semantische Bedeutung:

```text
Ein seitlicher Connector vom Typ b-l kann mit einem komplementären seitlichen Connector vom Typ b-s verbunden werden.
Dadurch entsteht eine seitliche Bauteilbeziehung.
```

Weiteres Beispiel:

```text
b-p2-t-t1-c3-r verwendet Port b-l-m
b-p1-b-t1-c2-l verwendet Port b-s-m
```

Semantische Bedeutung:

```text
Ein mittlerer oder modifizierter seitlicher Connector vom Typ b-l-m kann mit einem komplementären mittleren oder modifizierten Connector vom Typ b-s-m verbunden werden.
```

## Übersicht

| Port A  | Kompatibler Port B | Semantische Beziehung                                       |
| ------- | ------------------ | ----------------------------------------------------------- |
| `c-t`   | `c-b`              | vertikale Oberseite-zu-Unterseite-Verbindung                |
| `b-l`   | `b-s`              | seitliche Bauteilverbindung                                 |
| `b-l-m` | `b-s-m`            | seitliche Bauteilverbindung, mittlere/modifizierte Variante |

Der wichtigste Punkt:

```text
Connectoren sind die möglichen Beziehungspunkte am Bauteil.
Ports sind die Bedeutung dieser Punkte.
Kompatible Ports definieren, welche Beziehungen erlaubt sind.
```


## Grundidee

Ein Connector ist eine Anschlussstelle am Bauteil.
Ein Port beschreibt die Rolle dieser Anschlussstelle.
Eine Verbindung ist erlaubt, wenn die Rollen zusammenpassen.

## Seitliche Anschlüsse

Ein oberer seitlicher Anschluss ist ein aufnehmender Anschluss.
Er kann mit einem seitlichen Gegenanschluss verbunden werden.

Ein mittiger oberer seitlicher Anschluss ist ebenfalls aufnehmend.
Er kann mit normalen oder mittigen Gegenanschlüssen verbunden werden.

Ein unterer seitlicher Anschluss ist ein Gegenanschluss.
Er kann mit einem aufnehmenden seitlichen Anschluss verbunden werden.

Ein diagonaler seitlicher Anschluss ist ebenfalls ein Gegenanschluss.
Er kann mit einem passenden aufnehmenden Anschluss verbunden werden.

## Vertikale Anschlüsse

Ein oberer vertikaler Anschluss dient zum Stapeln.
Er kann mit einem unteren vertikalen Anschluss verbunden werden.

Ein unterer vertikaler Anschluss dient ebenfalls zum Stapeln.
Er kann mit einem oberen vertikalen Anschluss verbunden werden.

## Kompatible Rollen

| Anschlussstelle                  | Eigene Rolle                          | Kompatible Rollen                                                   |
| -------------------------------- | ------------------------------------- | ------------------------------------------------------------------- |
| oberer seitlicher Anschluss      | aufnehmender Seitenanschluss          | seitlicher Gegenanschluss; mittiger seitlicher Gegenanschluss       |
| oberer mittiger Seitenanschluss  | aufnehmender mittiger Seitenanschluss | seitlicher Gegenanschluss; mittiger seitlicher Gegenanschluss       |
| unterer seitlicher Anschluss     | seitlicher Gegenanschluss             | aufnehmender Seitenanschluss; aufnehmender mittiger Seitenanschluss |
| unterer mittiger Seitenanschluss | mittiger seitlicher Gegenanschluss    | aufnehmender Seitenanschluss; aufnehmender mittiger Seitenanschluss |
| diagonaler seitlicher Anschluss  | seitlicher Gegenanschluss             | aufnehmender Seitenanschluss; aufnehmender mittiger Seitenanschluss |
| oberer vertikaler Anschluss      | oberer Stapelanschluss                | unterer Stapelanschluss                                             |
| unterer vertikaler Anschluss     | unterer Stapelanschluss               | oberer Stapelanschluss                                              |

## Kurzform

Seitliche Anschlüsse verbinden Bauteile nebeneinander.
Vertikale Anschlüsse verbinden Bauteile übereinander.
Ports beschreiben die Anschlussrolle.
Kompatible Ports beschreiben passende Gegenrollen.
