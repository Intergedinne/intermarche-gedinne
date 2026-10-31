# Mise à jour hebdomadaire du folder

Chaque lundi, Florian partage les pages du folder de la semaine (images ou PDF).
Le site est le fichier `index.html` de ce dépôt (branche `main`, publié par GitHub Pages).

## Ce qu'on modifie

Uniquement le bloc JSON `<script id="folderData" type="application/json">` dans `index.html`.
Le reste de la page (ardoise, horaires, textes, formulaires) ne bouge pas.

## Format du bloc

```json
{
  "debut": "03/11",
  "fin": "08/11/2026",
  "fr": "https://www.intermarche.be/folders/decouvrez-notre-folder-du-03-11-26/",
  "nl": "https://www.intermarche.be/nl/folders/ontdek-onze-folder-van-03-11-26/",
  "temps": [
    {"t": "Titre FR", "p": "Texte FR", "tn": "Titel NL", "pn": "Tekst NL"}
  ],
  "offres": [
    {"r": "boucherie", "resa": 1, "carte": 1,
     "m": "1 kg + 1 kg gratis",
     "n": "Nom FR", "d": "Détails FR", "p": "4,19 €/kg", "x": "Ligne sous le prix FR",
     "nn": "Naam NL", "dn": "Details NL", "pn": "€ 4,19/kg", "xn": "Regel onder de prijs NL"}
  ]
}
```

- `debut` / `fin` : dates de validité imprimées sur le folder (du mardi au dimanche).
- `fr` / `nl` : liens vers le folder sur intermarche.be (même date que `debut`, format JJ-MM-AA).
- `temps` : 0 à 3 temps forts de la semaine (ouverture spéciale, cadeau, bonus carte…). Peut être vide.
- `offres` : une entrée par offre du folder.
  - `r` (rayon) : `boucherie`, `traiteur`, `fl`, `boulangerie`, `cremerie`, `epicerie`, `stnicolas` (saisonnier), `surgeles`, `boissons`, `maison`, `fleurs`.
  - `resa: 1` pour toutes les offres de la boucherie (affiche le bouton Réserver).
  - `carte: 1` pour les offres « avec ma carte ».
  - `m` : la mécanique telle qu'imprimée (« 1 + 1 gratis », « 2 + 2 gratis au choix », « -50 % », « Prix exceptionnel »…), en français. La traduction NL est automatique.
  - `p`/`pn` et `x`/`xn` sont facultatifs, mais toujours par paire FR/NL.
  - Prix au format belge : `4,19 €/kg` en FR, `€ 4,19/kg` en NL.
- Ne jamais inventer un prix ou une info : si un chiffre est illisible, on le laisse de côté.
- Pas de code-barres ni de bon de réduction reproduit sur le site.

## Vérifier avant de publier

1. Le bloc est du JSON valide (`python3 -c "import json,re; ..."`).
2. Chaque offre a `nn` et `dn`, et les paires `p`/`pn`, `x`/`xn` sont complètes.
3. Commit « Folder du JJ/MM », push sur `main`.

## Autres modifications du site

- `outils/source-artifact.html` : source de la copie de travail (artifact https://claude.ai/artifact/57WNNxdphnVhSF4sqfRdoj).
- `python3 outils/build_site.py` reconstruit `index.html` à partir de cette source (polices locales, balises de partage).
  Il conserve le bloc `folderData` déjà présent dans `index.html` : une modif de texte n'efface pas le folder de la semaine.
- Après une modif de la source, republier aussi l'artifact pour garder les deux copies identiques.
- Guide complet (routine, comptes, duplication pour un autre magasin) : https://claude.ai/artifact/6vP9CXWFhvqPwQL8XmxxLj
