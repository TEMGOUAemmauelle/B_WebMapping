# geoserver/Dockerfile

# Image officielle GeoServer
FROM docker.osgeo.org/geoserver:2.28.0

# Variables d'environnement pour l'admin
ENV GEOSERVER_ADMIN_USER=admin
ENV GEOSERVER_ADMIN_PASSWORD=camino

# Créer le data_dir si il n'existe pas
RUN mkdir -p /opt/geoserver/data_dir

# Copier un data_dir local (optionnel)
# COPY data_dir /opt/geoserver/data_dir

# Définir le data_dir par défaut
ENV GEOSERVER_DATA_DIR=/opt/geoserver/data_dir

# Exposer le port GeoServer
EXPOSE 8080

# Lancer GeoServer
CMD ["/opt/geoserver/bin/startup.sh"]
