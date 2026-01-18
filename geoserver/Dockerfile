# Base sur Tomcat avec JDK
FROM tomcat:9.0-jdk17

# Variables d'environnement pour Tomcat
ENV CATALINA_HOME /usr/local/tomcat
ENV PATH $PATH:$CATALINA_HOME/bin

# Port exposé
EXPOSE 8080

# Démarrer Tomcat au premier plan (OBLIGATOIRE)
CMD ["catalina.sh", "run"]

