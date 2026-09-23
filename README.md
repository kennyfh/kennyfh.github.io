# Página web personal

En este repositorio se encuentra el contenido de mi página web, [kennyfh.eu](https://kennyfh.eu). Es un sitio estático generado con [Hugo](https://gohugo.io) y el tema [Blowfish](https://github.com/nunocoracao/blowfish). Todo el contenido está escrito en Markdown y cada push a `main` reconstruye y publica la web automáticamente mediante GitHub Actions (en las pull requests solo se compila, para comprobar que no hay errores).

## Instalación

**Clonar el repositorio con el tema incluido (es un submódulo de git)**

```bash
git clone --recurse-submodules git@github.com:kennyfh/kennyfh.github.io.git
```

Si ya lo tenías clonado sin el tema:

```bash
git submodule update --init --recursive
```

**Actualizar el tema**

```bash
git submodule update --remote themes/blowfish
```

Antes de subir la nueva versión del tema, comprueba que la versión de Hugo de la CI (`.github/workflows/gh-pages.yml`) está dentro del rango que soporta Blowfish (`themes/blowfish/config.toml` y `themes/blowfish/release-versions/hugo-latest.txt`).

## Dependencias

- **Hugo extended >= 0.158.0** (la CI usa 0.160.1). En macOS: `brew install hugo`. Para otros sistemas, consulta la [guía de instalación](https://gohugo.io/installation/).
- **(Opcional) Python >= 3.12**, solo para generar las publicaciones a partir del `.bib`. Se recomienda [uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer); también puedes usar `pip install -r requirements.txt`.

## Desarrollo

Para ver la web en local con recarga en tiempo real:

```bash
hugo server
```

## Estructura

| Ruta | Contenido |
| --- | --- |
| `config/_default/` | Configuración del sitio, del tema, del menú y del perfil del autor |
| `content/` | Páginas: `about`, `resume`, `posts`, `projects` y `publications` |
| `layouts/publications/single.html` | Plantilla propia para la página de cada publicación |
| `assets/css/custom.css` | Estilos propios (Blowfish lo carga automáticamente) |
| `assets/icons/` | Iconos extra de [Font Awesome Free](https://fontawesome.com/license/free) que no trae el tema |
| `publications.bib` + `source_files/` | Fuente de las publicaciones (ver abajo) |

## Añadir publicaciones

1. Añade la entrada a `publications.bib`. Incluye al menos `author`, `title`, `year` y la revista o congreso; `month`, `doi`, `url` y `abstract` son opcionales.
2. (Opcional) Deja en `source_files/` los ficheros con el mismo nombre que el ID de la entrada (no distingue mayúsculas):
   - `<id>.pdf`: el artículo (botón "PDF").
   - `<id>_slides.pdf`: las diapositivas (botón "Slides").
   - `<id>.png`, `.jpg` o `.jpeg`: la portada. Se le añaden márgenes transparentes para que todas tengan la misma proporción.
3. Ejecuta el generador:

   ```bash
   uv run generate_publications.py
   ```

El script crea o actualiza `content/publications/<id>/index.md` y solo reescribe los PDFs y las portadas si han cambiado. El texto de `content/publications/_index.md` (la página de la lista) se edita a mano y el script no lo toca.

## Agradecimientos

- [Blowfish](https://github.com/nunocoracao/blowfish)
- Iconos de [Font Awesome Free](https://fontawesome.com) (CC BY 4.0)
