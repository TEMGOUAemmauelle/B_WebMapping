FROM tomcat:9.0-jdk17

# --- Variables Tomcat ---
ENV CATALINA_HOME /usr/local/tomcat
ENV PATH $PATH:$CATALINA_HOME/bin
EXPOSE 8080

# --- Installer wget/unzip/sed ---
RUN apt-get update && \
    apt-get install -y wget unzip sed && \
    rm -rf /var/lib/apt/lists/*

# --- Télécharger GeoServer WAR ---
ARG GEOSERVER_VERSION=2.25.0
RUN wget -O /tmp/geoserver.zip https://sourceforge.net/projects/geoserver/files/GeoServer/${GEOSERVER_VERSION}/geoserver-${GEOSERVER_VERSION}-war.zip/download && \
    unzip /tmp/geoserver.zip geoserver.war -d /tmp && \
    mv /tmp/geoserver.war $CATALINA_HOME/webapps/geoserver.war && \
    rm -rf /tmp/geoserver*

# --- Créer data_dir vide pour GeoServer ---
ENV GEOSERVER_DATA_DIR=/opt/geoserver/data_dir
RUN mkdir -p $GEOSERVER_DATA_DIR/security

# --- ADMIN GEO SERVER (OBLIGATOIRE) ---
ENV GEOSERVER_ADMIN_USER=admin
ENV GEOSERVER_ADMIN_PASSWORD=geoserver

# --- Patch CSP pour Render HTTPS ---
RUN echo '#!/bin/bash\n\
CSP_FILE="$GEOSERVER_DATA_DIR/security/csp.xml"\n\
echo "Waiting for CSP file at $CSP_FILE..."\n\
while [ ! -f "$CSP_FILE" ]; do\n\
  sleep 1\n\
done\n\
sed -i '\''s/form-action '\''self'\''/form-action '\''self'\'' https:\/\/b-webmapping.onrender.com/g'\'' $CSP_FILE\n\
echo "CSP patched"\n' > /patch_csp.sh && chmod +x /patch_csp.sh

# --- Variables proxy GeoServer ---
ENV PROXY_BASE_URL=https://b-webmapping.onrender.com/geoserver
ENV USE_X_FORWARDED_HEADERS=true

# --- CORRECTION CRUCIALE : RemoteIpValve pour HTTPS derrière proxy ---
RUN echo '<Context>\
<Valve className="org.apache.catalina.valves.RemoteIpValve" \
remoteIpHeader="x-forwarded-for" \
protocolHeader="x-forwarded-proto" \
protocolHeaderHttpsValue="https"/>\
</Context>' > $CATALINA_HOME/conf/context.xml

# --- Lancer le patch CSP et Tomcat en premier plan ---
CMD /patch_csp.sh & catalina.sh run
