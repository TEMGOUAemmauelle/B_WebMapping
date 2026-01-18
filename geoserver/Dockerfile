# Base sur Tomcat avec JDK
FROM tomcat:9.0-jdk17

# Variables d'environnement pour Tomcat
ENV CATALINA_HOME /usr/local/tomcat
ENV PATH $PATH:$CATALINA_HOME/bin

# Port exposé
EXPOSE 8080

# Installe wget, unzip et sed (requis pour download, extraction et patch)
RUN apt-get update && \
    apt-get install -y wget unzip sed && \
    rm -rf /var/lib/apt/lists/*

# Télécharge et déploie GeoServer WAR
ARG GEOSERVER_VERSION=2.25.0
RUN wget -O /tmp/geoserver.zip https://sourceforge.net/projects/geoserver/files/GeoServer/${GEOSERVER_VERSION}/geoserver-${GEOSERVER_VERSION}-war.zip/download && \
    unzip /tmp/geoserver.zip geoserver.war -d /tmp && \
    mv /tmp/geoserver.war $CATALINA_HOME/webapps/geoserver.war && \
    rm -rf /tmp/geoserver*

# Force le data_dir et crée le dossier security
ENV GEOSERVER_DATA_DIR=/opt/geoserver/data_dir
RUN mkdir -p $GEOSERVER_DATA_DIR/security

# Ajoute un script pour patcher csp.xml au démarrage
RUN echo '#!/bin/bash\n\
CSP_FILE="$GEOSERVER_DATA_DIR/security/csp.xml"\n\
echo "Waiting for CSP file at $CSP_FILE..."\n\
while [ ! -f "$CSP_FILE" ]; do\n\
  sleep 1\n\
  ((counter++))\n\
  if (( counter % 30 == 0 )); then\n\
    echo "Still waiting after $counter seconds..."\n\
  fi\n\
done\n\
sed -i '\''s/form-action '\''self'\''/form-action '\''self'\'' https:\/\/b-webmapping.onrender.com/g'\'' $CSP_FILE\n\
echo "CSP patched for form-action at $(date)"\n' > /patch_csp.sh && \
chmod +x /patch_csp.sh

# Autres env vars (pour proxy, etc.)
ENV PROXY_BASE_URL=https://b-webmapping.onrender.com/geoserver
ENV USE_X_FORWARDED_HEADERS=true

# Lance Tomcat en foreground, et le script en background
CMD catalina.sh run & /patch_csp.sh
