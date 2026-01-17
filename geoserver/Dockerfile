# Image officielle GeoServer
FROM docker.osgeo.org/geoserver:2.28.0

# Variables admin GeoServer
ENV GEOSERVER_ADMIN_USER=admin
ENV GEOSERVER_ADMIN_PASSWORD=camino

# Data directory
ENV GEOSERVER_DATA_DIR=/opt/geoserver/data_dir

# Créer le data_dir
RUN mkdir -p /opt/geoserver/data_dir

# Exposer le port
EXPOSE 8080

# Démarrer Tomcat au premier plan (OBLIGATOIRE)
CMD ["catalina.sh", "run"]
