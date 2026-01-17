# Webmapping Backend

Ce projet met en place une infrastructure de base pour un système de webmapping basé sur PostGIS et GeoServer via Docker Compose.

## Structure du projet

```
.
├── .env
├── docker-compose.yml
├── Readme
├── geoserver/
├── postgis/
│   └── init/
│       └── init.sql
```

- **postgis/** : Contient la configuration et l'initialisation de la base de données PostGIS.
- **geoserver/** : Répertoire réservé pour la configuration ou les extensions GeoServer.
- **.env** : Variables d'environnement pour la base de données PostgreSQL/PostGIS.
- **docker-compose.yml** : Orchestration des services Docker.

## Prérequis

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Configuration

1. **Variables d'environnement**

   Le fichier [.env](.env) définit les identifiants de la base de données :

   ```
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=gatesweb123
   POSTGRES_DB=bassins_cm
   ```

2. **Initialisation de la base PostGIS**

   Le script [postgis/init/init.sql](postgis/init/init.sql) crée les tables spatiales nécessaires : `regions`, `departements`, `bassins_production`.

## Lancement des services

1. **(Optionnel) Activer l'initialisation automatique de la base**

   Décommente la ligne suivante dans [docker-compose.yml](docker-compose.yml) pour exécuter le script d'initialisation lors du premier lancement :

   ```yml
   volumes:
     - pgdata:/var/lib/postgresql/data
     - ./postgis/init/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
   ```

2. **Démarrer les services**

   ```sh
   docker-compose up -d
   ```

   - **PostGIS** sera accessible sur le port `5433`.
   - **GeoServer** sera accessible sur le port `8080` (http://localhost:8080).

## Accès

- **GeoServer** : http://# Webmapping Backend

Ce projet met en place une infrastructure de base pour un système de webmapping basé sur PostGIS et GeoServer via Docker Compose.

## Structure du projet

```
.
├── .env
├── docker-compose.yml
├── Readme
├── geoserver/
├── postgis/
│   └── init/
│       └── init.sql
```

- **postgis/** : Contient la configuration et l'initialisation de la base de données PostGIS.
- **geoserver/** : Répertoire réservé pour la configuration ou les extensions GeoServer.
- **.env** : Variables d'environnement pour la base de données PostgreSQL/PostGIS.
- **docker-compose.yml** : Orchestration des services Docker.

## Prérequis

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Configuration

1. **Variables d'environnement**

   Le fichier [.env](.env) définit les identifiants de la base de données :

   ```
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=gatesweb123
   POSTGRES_DB=bassins_cm
   ```

2. **Initialisation de la base PostGIS**

   Le script [postgis/init/init.sql](postgis/init/init.sql) crée les tables spatiales nécessaires : `regions`, `departements`, `bassins_production`.

## Lancement des services

1. **(Optionnel) Activer l'initialisation automatique de la base**

   Décommente la ligne suivante dans [docker-compose.yml](docker-compose.yml) pour exécuter le script d'initialisation lors du premier lancement :

   ```yml
   volumes:
     - pgdata:/var/lib/postgresql/data
     - ./postgis/init/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
   ```

2. **Démarrer les services**

   ```sh
   docker-compose up -d
   ```

   - **PostGIS** sera accessible sur le port `5433`.
   - **GeoServer** sera accessible sur le port `8080` (http://localhost:8080).

## Accès
