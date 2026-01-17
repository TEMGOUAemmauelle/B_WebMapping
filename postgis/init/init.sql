CREATE EXTENSION postgis;

-- Régions
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100)
);
SELECT AddGeometryColumn('regions', 'geom', 4326, 'MULTIPOLYGON', 2);

-- Départements
CREATE TABLE departements (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    region_id INTEGER REFERENCES regions(id)
);
SELECT AddGeometryColumn('departements', 'geom', 4326, 'MULTIPOLYGON', 2);

-- Bassins de production
CREATE TABLE bassins_production (
    id SERIAL PRIMARY KEY,
    filiere VARCHAR(50), -- agriculture, élevage, pêche
    produit VARCHAR(100),
    volume DOUBLE PRECISION,
    departement_id INTEGER REFERENCES departements(id)
);
SELECT AddGeometryColumn('bassins_production', 'geom', 4326, 'MULTIPOLYGON', 2);


