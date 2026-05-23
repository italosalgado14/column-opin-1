FROM ghcr.io/getzola/zola:v0.19.2

WORKDIR /site

EXPOSE 1111

# Servidor de desarrollo con hot reload escuchando en todas las interfaces
ENTRYPOINT ["zola"]
CMD ["serve", "--interface", "0.0.0.0", "--port", "1111", "--base-url", "/"]
