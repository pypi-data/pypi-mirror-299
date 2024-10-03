# Parseur de relevés BoursoBank

⚠ Cette bibliothèque a été développée indémendament de BoursoBank.


## Installation

    pip install boursobank


## Sécurité

### Mot de passe

Cette bibliothèque ne **se connecte pas à internet** (dans le doute,
lis le code) elle ne fait que lire des relevés au format PDF déjà
téléchargés, tous les traitements sont effectés en local.

Dans le doute il doit être possible de faire tourner l’application
dans [firejail](https://github.com/netblue30/firejail) ou similaire.

Il n’est donc pas nécessaire de s’inquiéter pour son mot de passe : il
n’est pas demandé (là, pas besoin de relire le code : si la lib ne
demande pas le mot de passe… elle ne l’a pas).


### Erreurs du parseur

Lire des PDF [n’est pas simple](https://pypdf.readthedocs.io/en/stable/user/extract-text.html#ocr-vs-text-extraction).

Pour s’assurer de ne pas introduire d’erreur dans vos analyses, cette
bibliothèque fournit une méthode `validate()` qui valide que le
montant initial + toutes les lignes donne bien le montant final, sans
quoi une `ValueError` est levée.

Cet exemple ne lévera donc une exception qu’en cas d’erreur d’analyse
(ou de la banque, comme au monopoly) :

```python
for file in args.files:
    statement = Statement.from_pdf(file)
    statement.pretty_print()
    statement.validate()
```


## Interface en ligne de commande

Cette lib est utilisable en ligne de commande :

    boursobank *.pdf

vous affichera vos relevés (CB ou compte), exemple :

    $ boursobank 2024-01.pdf
                2024-01.pdf
    ┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Date       ┃ RIB                        ┃
    ┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ 2024-01-01 │ 12345 12345 00000000000 99 │
    └────────────┴────────────────────────────┘
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃                                    Label ┃ Value    ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
    │                            VIR SEPA Truc │ 42.42    │
    │                     VIR SEPA Machin truc │ 99.00    │
    │    Relevé différé Carte 4810********0000 │ -123.45  │
    └──────────────────────────────────────────┴──────────┘


## API

Tout l’intérêt est de pouvoir consulter ses relevés en Python, par
exemple un export en CSV :

```python
import argparse
import csv
import sys
from pathlib import Path

from boursobank import Statement


def main():
    args = parse_args()
    statement = Statement.from_pdf(args.ifile)
    writer = csv.writer(sys.stdout)
    for line in statement.lines:
        writer.writerow((line.label, line.value))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("ifile", type=Path, help="PDF file")
    return parser.parse_args()


if __name__ == "__main__":
    main()
```

La bibliothèque ne fournit qu’un point d’entrée : la classe `Statement`

Depuis cette classe il est possible de parser des PDF :

    relevé_bancaire = Statement.from_pdf("test.pdf")

ou du texte :

    relevé_bancaire = Statement.from_text("blah blah")


Cette classe fournit principalement deux attributs, un dictionnaire `headers` contenant :

- `date` : le 1° jour du mois couvert par ce relevé.
- `emit_date` : la date à laquelle le relevé a été rédigé.
- `RIB` : le RIB/IBAN du relevé.
- `devise` : probablement `"EUR"`.
- `card_number` : le numéro de carte bleu si c’est un relevé de carte.
- `card_owner` : le nom du possesseur de la carte bleu si c’est un relevé de carte.

et un attribut lines contenant des instances de la classe `Line` dont
les attributs principaux sont :

- `label` : la description courte de la ligne.
- `description` : la suite de la description de la ligne si elle est sur plusieurs lignes.
- `value` : le montant de la ligne (positif pour un crédit, négatif pour un débit).
