# Base sur Tomcat avec JDK
FROM tomcat:9.0-jdk17

# Variables d'environnement pour Tomcat
ENV CATALINA_HOME /usr/local/tomcat
ENV PATH $PATH:$CATALINA_HOME/bin

# Port exposé
EXPOSE 8080

# Télécharge et déploie GeoServer WAR
ARG GEOSERVER_VERSION=2.25.0
RUN wget -O /tmp/geoserver.zip https://sourceforge.net/projects/geoserver/files/GeoServer/${GEOSERVER_VERSION}/geoserver-${GEOSERVER_VERSION}-war.zip/download && \
    unzip /tmp/geoserver.zip geoserver.war -d /tmp && \
    mv /tmp/geoserver.war $CATALINA_HOME/webapps/geoserver.war && \
    rm -rf /tmp/geoserver*

# Ajoute un script pour patcher csp.xml au démarrage
RUN echo '#!/bin/bash\n\
# Attends que GeoServer démarre et crée csp.xml\n\
sleep 60  # Ajuste si besoin (temps pour démarrage)\n\
CSP_FILE="/opt/geoserver/data_dir/security/csp.xml"\n\
if [ -f "$CSP_FILE" ]; then\n\
  sed -i '\''s/form-action '\''self'\''/form-action '\''self'\'' https:\/\/b-webmapping.onrender.com/g'\'' $CSP_FILE\n\
  echo "CSP patched for form-action"\n\
fi\n\
# Relance Tomcat si besoin (mais pas nécessaire car patch post-démarrage)\n' > /patch_csp.sh && \
chmod +x /patch_csp.sh

# Autres env vars (pour proxy, etc.)
ENV PROXY_BASE_URL=https://b-webmapping.onrender.com/geoserver
ENV USE_X_FORWARDED_HEADERS=true

# Lance Tomcat, puis le script en background
CMD ["catalina.sh", "run"] & /patch_csp.sh
