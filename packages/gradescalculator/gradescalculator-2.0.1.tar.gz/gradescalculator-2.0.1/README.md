# GradesCalculator

`GradesCalculator` est un package Python qui permet de calculer une note globale à partir de notes pondérées. Il inclut un script exécutable en ligne de commande pour effectuer ce calcul facilement.

## Installation

Pour installer le package, vous pouvez utiliser `pip` après avoir construit le package localement. Suivez ces étapes :

1. Clonez le dépôt ou téléchargez les fichiers nécessaires.
```bash
git clone https://github.com/BERTHETquentin/GradesCalculator.git
```
2. Assurez-vous d'être dans le répertoire contenant `setup.py`.
3. Exécutez les commandes suivantes :

```bash
python setup.py sdist bdist_wheel
pip install dist/gradescalculator-0.2-py3-none-any.whl
pip install -e .
```

Vous pouvez aussi le télécharger directement via le gestionnaire de paquets [pip](https://pypi.org/project/pip/)

```bash
pip install gradescalculator
```

le lien du package PyPi se trouve [ici](https://pypi.org/project/gradescalculator/)

## Utilisation

Une fois installé, vous pouvez utiliser le script en ligne de commande pour calculer les notes. Voici comment l'utiliser :

### Calcul de la Moyenne Pondérée
Pour calculer une moyenne pondérée à partir de notes et de leurs poids, utilisez la commande suivante :
```bash
average note1 poids1 note2 poids2 note3 poids3 ...
```
#### Exemple
Supposons que vous avez les notes et poids suivants :

- Note 1 : 3.6 avec un poids de 10
- Note 2 : 4.6 avec un poids de 15
- Note 3 : 5.3 avec un poids de 25
- Note 4 : 4.0 avec un poids de 5
- Note 5 : 4.9 avec un poids de 45
  
Pour calculer la note globale, exécutez la commande suivante :
```bash
average 3.6 10 4.6 15 5.3 25 4.0 5 4.9 45
```
### Utilisation avec un Fichier CSV
Vous pouvez également importer les notes et leurs poids depuis un fichier CSV. Le fichier CSV doit contenir deux colonnes : la première pour les notes et la deuxième pour les poids.
```bash
average --csv chemin/vers/fichier.csv
```
### Choix de la Méthode de Calcul
Le script supporte plusieurs méthodes de calcul pour la moyenne :
- weighted : Moyenne pondérée (par défaut)
- arithmetic : Moyenne arithmétique simple
- geometric : Moyenne géométrique
Pour spécifier la méthode de calcul, utilisez l'option --method :
```bash
average --method [weighted|arithmetic|geometric] note1 poids1 note2 poids2 ...
```
### Résultat

Le script affichera la note globale précise arrondie à 0.01 près et arrondie à 0.5 près :

```bash
Precise Overall Grade (rounded to the nearest 0.01): X.X
Rounded Overall Grade (rounded to the nearest 0.5): Y.Y
```

### Structure du Répertoire

La structure du répertoire pour votre package gradescalculator doit ressembler à ceci :

```bash
gradescalculator/
│
├── gradescalculator/
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   └── test_calculations.py
│
├── dist/
│   └── gradescalculator-0.2-py3-none-any.whl
│
├── build/
├── gradescalculator.egg-info/
├── setup.py
└── README.md
```

## Moyennes Explicatives

### Moyenne Arithmétique
La moyenne arithmétique est la somme de toutes les valeurs divisée par le nombre de valeurs. C'est la méthode de calcul de la moyenne la plus couramment utilisée. 
#### Formule
Moyenne arithmétique = ![image](https://github.com/BERTHETquentin/GradesCalculator/assets/123391834/3e18a60c-a863-4f92-9475-bd1d2e690d67)
#### Exemple 
Si vous avez les valeurs 3, 5 et 7 :
Moyenne arithmétique = ![image](https://github.com/BERTHETquentin/GradesCalculator/assets/123391834/ae7bd953-52eb-434c-aac8-53b9b1d3487a)

### Moyenne Géométrique
La moyenne géométrique est la n-ième racine du produit des n valeurs. Elle est souvent utilisée pour des ensembles de nombres positifs où l'on souhaite prendre en compte les proportions ou les taux de croissance.
#### Formule
Moyenne géométrique = ![image](https://github.com/BERTHETquentin/GradesCalculator/assets/123391834/58bdee09-4538-4c99-b903-2883319346e0)
#### Exemple 
Si vous avez les valeurs 3, 5 et 7 :
Moyenne géométrique = ![image](https://github.com/BERTHETquentin/GradesCalculator/assets/123391834/1b9d1152-ef77-42bb-9b4a-d9f75bc63cbb)

### Moyenne pondérée
La moyenne pondérée est similaire à la moyenne arithmétique, mais chaque valeur est multipliée par un poids. La somme des produits des valeurs par leurs poids est ensuite divisée par la somme des poids.
#### Formule
Moyenne pondérée = ![image](https://github.com/BERTHETquentin/GradesCalculator/assets/123391834/2319272f-9c88-483f-97a8-37c11017cf99)

où ![image](https://github.com/BERTHETquentin/GradesCalculator/assets/123391834/8184090c-d7fa-48c9-967c-d9ff82bd8ce7) est le poids associé à la valeur ![image](https://github.com/BERTHETquentin/GradesCalculator/assets/123391834/5099621f-31bc-405b-8d79-5ce61d43c0fb)



#### Exemple 
Si vous avez les valeurs 3, 5 et 7 avec des poids 1, 2 et 3 respectivement :
Moyenne pondérée = ![image](https://github.com/BERTHETquentin/GradesCalculator/assets/123391834/8a0dae51-ed74-4382-9810-32ea1a63e0de)

## Auteur
- Quentin Berthet - [github](https://github.com/BERTHETquentin)
