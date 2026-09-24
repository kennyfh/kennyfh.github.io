"""Genera las páginas de `content/publications/` a partir de `publications.bib`.

Para cada entrada del .bib se crea `content/publications/<id>/index.md`. Si en
`source_files/` hay ficheros cuyo nombre coincide con el ID de la entrada, se
mueven al bundle (la carpeta es una bandeja de entrada y queda vacía):

- `<id>.pdf`             -> botón "PDF"
- `<id>_slides.pdf`      -> botón "Slides"
- `<id>.webp|png|jpg`   -> portada (`featured.webp`, con márgenes hasta ratio 1.5)

El `_index.md` de la sección solo se crea si no existe, para no perder el
contenido que se haya añadido a mano.
"""

import io
import json
import re
import shutil
import sys
import textwrap
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser
from PIL import Image
from pylatexenc.latex2text import LatexNodes2Text

BASE_DIR = Path(__file__).resolve().parent
BIB_FILE = BASE_DIR / "publications.bib"
CONTENT_DIR = BASE_DIR / "content" / "publications"
SOURCE_FILES_DIR = BASE_DIR / "source_files"

IMAGE_EXTENSIONS = (".webp", ".png", ".jpg", ".jpeg")
FEATURED_RATIO = 1.5
FEATURED_MAX_WIDTH = 1600  # Blowfish sirve como mucho 1280 px en las tarjetas
FEATURED_NAME = "featured.webp"

MONTHS = {
    name: i
    for i, names in enumerate(
        [
            ("jan", "january", "ene", "enero"),
            ("feb", "february", "febrero"),
            ("mar", "march", "marzo"),
            ("apr", "april", "abr", "abril"),
            ("may", "mayo"),
            ("jun", "june", "junio"),
            ("jul", "july", "julio"),
            ("aug", "august", "ago", "agosto"),
            ("sep", "sept", "september", "septiembre"),
            ("oct", "october", "octubre"),
            ("nov", "november", "noviembre"),
            ("dec", "december", "dic", "diciembre"),
        ],
        start=1,
    )
    for name in names
}

SECTION_INDEX = """\
---
title: 'Publications'
draft: false
showDate: false
showDateUpdated: false
showHeadingAnchors: false
showPagination: false
showReadingTime: false
showTableOfContents: true
showTaxonomies: false
showWordCount: false
showSummary: false
sharingLinks: false
---
"""

latex = LatexNodes2Text()


def slugify(text):
    """Convierte un texto en un 'slug' amigable para URLs."""
    return re.sub(r"[\s\W_]+", "-", text.lower()).strip("-")


def yaml_str(text):
    """Serializa un texto como escalar YAML (las cadenas JSON son YAML válido)."""
    return json.dumps(text, ensure_ascii=False)


def to_text(value):
    # Un `&` sin escapar es un separador de columnas en LaTeX y se perdería
    value = re.sub(r"(?<!\\)&", r"\\&", value)
    return latex.latex_to_text(value).strip()


def short_description(abstract, limit=160):
    """Primeras frases del resumen que quepan en `limit` caracteres (meta description)."""
    text = " ".join(abstract.split())
    description = ""
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        candidate = f"{description} {sentence}".strip()
        if len(candidate) > limit:
            break
        description = candidate
    return description or text[: limit - 1].rsplit(" ", 1)[0] + "…"


def get_publication_source(entry):
    """Obtiene la fuente principal de la publicación (journal, booktitle, etc.)."""
    source_fields = {
        "article": "journal",
        "inproceedings": "booktitle",
        "conference": "booktitle",
        "book": "publisher",
        "inbook": "booktitle",
        "incollection": "booktitle",
        "techreport": "institution",
        "phdthesis": "school",
        "mastersthesis": "school",
        "misc": "howpublished",
    }
    field = source_fields.get(entry.get("ENTRYTYPE", "").lower())
    candidates = [field] if field else []
    candidates += ["journal", "booktitle", "publisher", "school", "institution", "howpublished", "note"]
    return next((entry[f] for f in candidates if entry.get(f)), "")


def get_date(entry):
    """Fecha ISO (YYYY-MM-01) a partir de year/month; sirve para ordenar la lista."""
    year = int(entry.get("year", 0) or 0)
    month_raw = entry.get("month", "").strip().lower().rstrip(".")
    month = int(month_raw) if month_raw.isdigit() else MONTHS.get(month_raw, 1)
    return f"{year:04d}-{month:02d}-01" if year else None


def find_source(entry_id, suffix="", extensions=(".pdf",)):
    """Busca en source_files/ un fichero `<entry_id><suffix>.<ext>` sin distinguir mayúsculas."""
    wanted = f"{entry_id}{suffix}".lower()
    for path in sorted(SOURCE_FILES_DIR.iterdir()):
        if path.suffix.lower() in extensions and path.stem.lower() == wanted:
            return path
    return None


def make_featured_image(src, dest):
    """Añade márgenes transparentes para que todas las portadas tengan el mismo ratio."""
    with Image.open(src) as img:
        img = img.convert("RGBA")
        img.thumbnail((FEATURED_MAX_WIDTH, FEATURED_MAX_WIDTH), Image.LANCZOS)
        w, h = img.size
        if w / h > FEATURED_RATIO:
            new_w, new_h = w, int(w / FEATURED_RATIO)
        else:
            new_w, new_h = int(h * FEATURED_RATIO), h
        canvas = Image.new("RGBA", (new_w, new_h), (255, 255, 255, 0))
        canvas.paste(img, ((new_w - w) // 2, (new_h - h) // 2), img)
        buffer = io.BytesIO()
        canvas.save(buffer, "WEBP", quality=85, method=6)
    # El codificador es determinista: si los bytes coinciden no se reescribe (y git no ve cambios)
    if not dest.exists() or dest.read_bytes() != buffer.getvalue():
        dest.write_bytes(buffer.getvalue())


def build_publication(entry):
    entry_id = entry["ID"]
    slug = slugify(entry_id)
    bundle = CONTENT_DIR / slug
    bundle.mkdir(parents=True, exist_ok=True)

    front_matter = [
        f"title: {yaml_str(to_text(entry.get('title', '')))}",
        "showDate: false",
    ]
    date = get_date(entry)
    if date:
        front_matter.append(f"date: {date}")

    authors = [to_text(a) for a in entry.get("author", "").split(" and ") if a.strip()]
    front_matter.append("authors:")
    front_matter += [f"  - {yaml_str(a)}" for a in authors]
    front_matter.append(f"publication: {yaml_str(to_text(get_publication_source(entry)))}")
    # Tipo y datos bibliográficos: se usan en las etiquetas citation_* para Google Scholar
    front_matter.append(f"publication_type: {yaml_str(entry.get('ENTRYTYPE', '').lower())}")
    for field in ("volume", "number", "pages", "publisher"):
        if entry.get(field):
            front_matter.append(f"{field}: {yaml_str(to_text(entry[field]))}")

    # En BibTeX un `%` sin escapar abre un comentario; los ya escapados (`\%`) se dejan igual
    abstract = to_text(re.sub(r"(?<!\\)%", r"\\%", entry.get("abstract", "")))
    if abstract:
        front_matter.append(f"description: {yaml_str(short_description(abstract))}")
        front_matter.append("abstract: |-")
        front_matter.append(textwrap.indent(abstract, "  "))

    # Solo el identificador: algunos .bib traen la URL completa (https://doi.org/...)
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", entry.get("doi", "").strip(), flags=re.I)
    if doi:
        front_matter.append(f"doi: {yaml_str(doi)}")

    # Un fichero nuevo en source_files/ sustituye al del bundle; si no hay, se conserva el que ya estaba
    for suffix, key in (("", "pdf"), ("_slides", "slides")):
        dest = bundle / f"{slug}{suffix}.pdf"
        src = find_source(entry_id, suffix=suffix)
        if src:
            shutil.move(src, dest)
        if dest.exists():
            front_matter.append(f'{key}: "{dest.name}"')

    image = find_source(entry_id, extensions=IMAGE_EXTENSIONS)
    if image:
        make_featured_image(image, bundle / FEATURED_NAME)
        image.unlink()
        # Portadas de versiones anteriores del script: Blowfish usaría la primera que encuentre
        for old in bundle.glob("featured.*"):
            if old.name != FEATURED_NAME:
                old.unlink()

    if entry.get("url"):
        front_matter.append(f"website: {yaml_str(entry['url'])}")

    db = bibtexparser.bibdatabase.BibDatabase()
    db.entries = [entry]
    front_matter.append("bibtex: |-")
    front_matter.append(textwrap.indent(bibtexparser.dumps(db).strip(), "  "))

    (bundle / "index.md").write_text("---\n" + "\n".join(front_matter) + "\n---\n", encoding="utf-8")


def main():
    if not BIB_FILE.exists():
        sys.exit(f"Error: no se encontró {BIB_FILE}")

    parser = BibTexParser(common_strings=True)  # entiende macros como `month = dec`
    with BIB_FILE.open(encoding="utf-8") as f:
        entries = bibtexparser.load(f, parser=parser).entries

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_FILES_DIR.mkdir(exist_ok=True)
    section_index = CONTENT_DIR / "_index.md"
    if not section_index.exists():
        section_index.write_text(SECTION_INDEX, encoding="utf-8")

    generated = 0
    for entry in entries:
        if not entry.get("ID"):
            print(f"Aviso: entrada sin ID omitida ({entry.get('title', 'sin título')})")
            continue
        build_publication(entry)
        generated += 1

    print(f"Generadas {generated} publicaciones en {CONTENT_DIR.relative_to(BASE_DIR)}/")


if __name__ == "__main__":
    main()
