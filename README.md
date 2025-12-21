# Página web personal

En este repositorio se encuentra el contenido sobre mi página web. Este sitio web estático está generado mediante el framework [Hugo](https://gohugo.io). Todo el contenido está escrito en ficheros Markdown y se puede editar empleando cualquier editor de texto. Además, se tiene una configuración de Github Actions que reconstruye automáticamente el sitio una vez se realice un push en la rama `main`.

# Instalación

**Clonar el repositorio en local (mediante clave SSH)**

```bash
git clone git@github.com:kennyfh/kennyfh.github.io.git
```

**Se está usando un tema llamado [blowfish](https://github.com/nunocoracao/blowfish), que viene incluído com un submódulo de github, así que para incluír el tema ejecutar el siguiente comando**


```bash
git submodule update --init --recursive
```

**Para actualizar el tema puedes usar el siguiente comando**

```bash
git pull --recurse-submodules
```

## Dependencias

**Es importante tener una versión de hugo (>=0.137.0) para poder construir la web estática. Lo puedes encontrar en la [página oficial de hugo](https://gohugo.io/installation/linux/).**

**(Opcional) Si quieres construir las publicaciones a partir del fichero .bib, necesitarás el lenguaje python con sus dependencias, se da las opciones de instalarlo mediante un `requirements.txt` o  usar [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)**


## Desarrollo

**Para el desarrollo local y visualizar en tiempo real la web usa el siguiente comando

```bash
hugo serve
```

**Si quieres añadir publicaciones para la sección de `publications`de la web, añadir un artículo en el fichero `publications.bib`, y ejecutar el siguiente comando (si usas uv)

```bash
uv run generate_publications.py
```

## Agradecimientos

* [Blowfish](https://github.com/nunocoracao/blowfish)
