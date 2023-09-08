# Intégration des données STOM

## Correspondance des colonnes

- ZONE : La zone géographique en France (ici le PNE)
- ID ZONE : Le code de la zone géographique
- NOM SITE : Le nom du groupe de sites
- ID SITE : Le code du groupe de sites 
- NPOINT : Le numéro du point d'écoute
- IDUNIQUE : Le code du point d'écoute
- OBSERVATEUR 1, OBSERVATEUR 2 : Les observateurs effectuant la visite 
- DATE : La date de la visite
- HEURE : L'heure de la visite
- COUV NUAGE, PLUIE, VENT, VISI, DENEIGMT : Les conditions de la visite (couverture nuageuse, de pluie, de vent, de la visibilité, du déneigement)
- ESPECE : L'espèce observée
- NB05 : Observations dans les 5 premières minutes du protocole (nécessaire)
- NB510 : Observations après les 5 premières minutes du protocole (nécessaire)
- NB1015 : Observations après les 10 premières minutes du protocole
- NB100 : Observations hors protocole
- MAX10 : Nombre de juvéniles observés
- RQ : Remarques pour l'observation
- X, Y, ALT : Coordonnées géographiques
- RASTALT : Inconnu
- AGRI, IR, IIR1, IIR2 : Inconnus, supposés être des informations sur des éléments géographiques dans les sites
- % SOL NU, % ROCH : Description géologique quantitative du site
- % HERB, %ARBRISSEAU, %ARBRISSEAU_1m ,%ARBUSTE, %ARBRES : Données sur les espèces de plantes présentes sur le point d'écoute. Pour certains fichiers, il n'y a que quatre de ces cinq colonnes, dans ce cas, toutes les données figurent dans les plantes de moins de 1m de haut.
- %CROTTES : Une donnée inconnue sure les crottes (non fournie dans les données)
- INFOS SUP PATURAGE : Des informations supplémentaires sur le paturage sur le poitn d'écoute (fournie sur aucune ligne de fichier).

Nous avons essayé de fournir certaines données supplémentaires hors protocole dans les visites, mais sans réussite.

Les colonnes ZONE, ID ZONE, X, Y et ALT sont déterminés dans la base de données, aucun traitement n'est fait avec.

## Traitements des colonnes

### Traitement des sites

Tous les sites dans les fichiers sont des sites déjà définis dans GeoNature. Le choix du site se fait avec les colonnes "NOM SITE" et "NPOINT". "NOM SITE" contient le nom du groupe de points d'écoute, tandis que "NPOINT" contient le numéro du point d'écoute dans le groupe. Les "ID SITE" et "IDUNIQUE" pourraient être utilisés s'il étaient fournis pour toutes les lignes. Il a été considéré que tous les points d'écoute ont été visités dans un groupe. 

### Traitement des observateurs

Pour les observateurs, un maximun de travail à été fait afin qu'ils puissent tous être tirés de la base de données, peu importe la manière dont leur noms figurent dans un fichier. L'ordre de nom et prénom, s'il sont tous les deux définis. Si ceci n'est pas le cas, le traitement peut être fait seulement avec le nom. Si un nom ne figure pas du tout dans la base de données, la ligne est envoyée dans le fichier d'erreurs. Il y a un cas ou les données ont été modifiés, et un nom a été complété par le prénom de la personne qui a effectué la visite, car il y a plusieurs personnes dans la BDD avec ce nom, et la première lettre du prénom était fourni dans le document.

### Traitement des noms d'espèce

Le taxon de l'observation est déterminé à être celle ou le cd_nom dans la base de données est égal au cd_ref pour ce nom de taxon. Le code gère tous les problèmes de casse et d'accents, et complète les noms dans les cas ou le nom fourni dans le fichier est une partie d'un nom dans la base de données.



