import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text
import os
import re
import shutil
import textwrap
from pathlib import Path
from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parent  # ajusta según dónde esté el script
print("CWD:", os.getcwd())
print("Script dir:", Path(__file__).resolve().parent)
BIB_FILE = BASE_DIR / "publications.bib"
CONTENT_DIR = BASE_DIR / "content" / "publications"
SOURCE_FILES_DIR = BASE_DIR / "source_files"

CONTENT_DIR.mkdir(parents=True, exist_ok=True)
def slugify(text):
    """Convierte un texto en un 'slug' amigable para URLs."""
    text = text.lower()
    text = re.sub(r"[\s\W_]+", "-", text)
    text = text.strip("-")
    return text


def get_publication_source(entry):
    """Obtiene la fuente principal de la publicación (journal, booktitle, etc.)."""
    entry_type = entry.get("ENTRYTYPE", "").lower()
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
    field = source_fields.get(entry_type)
    source = entry.get(field, "") if field else ""
    if not source:
        for fallback in (
            "journal",
            "booktitle",
            "publisher",
            "school",
            "institution",
            "howpublished",
            "note",
        ):
            source = entry.get(fallback, "")
            if source:
                break
    return source


print("Iniciando la generación de contenido de publicaciones...")
latex_converter = LatexNodes2Text()

try:
    with open(BIB_FILE, "r", encoding="utf-8") as f:
        bib_db = bibtexparser.load(f)
except FileNotFoundError:
    print(f"Error: El archivo {BIB_FILE} no fue encontrado.")
    exit()

sorted_entries = sorted(
    bib_db.entries, key=lambda x: int(x.get("year", 0)), reverse=True
)

with open(os.path.join(CONTENT_DIR, "_index.md"), "w", encoding="utf-8") as f:
    f.write("---\n")
    f.write("title: 'Publications'\n")
    f.write("draft: false\n")
    f.write("showDate: false\n")
    f.write("showDateUpdated: false\n")
    f.write("showHeadingAnchors: false\n")
    f.write("showPagination: false\n")
    f.write("showReadingTime: false\n")
    f.write("showTableOfContents: true\n")
    f.write("showTaxonomies: false\n")
    f.write("showWordCount: false\n")
    f.write("showSummary: false\n")
    f.write("sharingLinks: false\n")
    f.write("---\n")

# TODO: esto podría optimizarse si las cosas se separan por carpetas
for entry in sorted_entries:
    entry_id = entry.get("ID")
    if not entry_id:
        print(
            f"Advertencia: Se omitió una entrada porque no tiene ID. Título: {entry.get('title', 'N/A')}"
        )
        continue

    slug = slugify(entry_id)
    publication_path = CONTENT_DIR / slug
    publication_path.mkdir(parents=True, exist_ok=True)

    title = latex_converter.latex_to_text(entry.get("title", "")).replace("'", "''")
    authors_list = [
        latex_converter.latex_to_text(a.strip())
        for a in entry.get("author", "").split(" and ")
    ]
    abstract_from_bib = entry.get("abstract", "")
    safe_abstract = abstract_from_bib.replace("%", r"\%")
    abstract_raw = latex_converter.latex_to_text(safe_abstract).strip()
    indented_abstract = textwrap.indent(text=abstract_raw, prefix="  ")
    year = entry.get("year", "")
    publication_source = latex_converter.latex_to_text(
        get_publication_source(entry)
    ).replace("'", "''")
    doi = entry.get("doi", "")
    website_url = entry.get("url", "")

    db = bibtexparser.bibdatabase.BibDatabase()
    db.entries = [entry]
    bibtex_str = bibtexparser.dumps(db)
    resources_front_matter = []

    pdf_source_path = None
    for pdf in SOURCE_FILES_DIR.glob("*.pdf"):
        if pdf.stem.lower() == entry_id.lower():
            pdf_source_path = pdf
            break
    
    if pdf_source_path:
        pdf_dest_filename = f"{slug}.pdf"
        shutil.copy(pdf_source_path, publication_path / pdf_dest_filename)
        resources_front_matter.append(f'pdf: "{pdf_dest_filename}"')

    slides_source_path = SOURCE_FILES_DIR / f"{entry_id}_slides.pdf"
    if slides_source_path.exists():
        slides_dest_filename = f"{slug}_slides.pdf"
        shutil.copy(
            slides_source_path,
            publication_path / slides_dest_filename,
        )
        resources_front_matter.append(f'slides: "{slides_dest_filename}"')

    for ext in [".jpg", ".jpeg", ".png"]:
        for img_path in SOURCE_FILES_DIR.glob(f"*{ext}"):
            if img_path.stem.lower() == entry_id.lower():
                image_dest_filename = f"featured.png" # Forzamos PNG para transparencia
                destination_path = publication_path / image_dest_filename
                
                with Image.open(img_path) as img:
                    img = img.convert("RGBA")
                    w, h = img.size
                    
                    # Definimos la proporción deseada (ejemplo 2:1 o 16:9)
                    target_ratio = 1.5 
                    current_ratio = w / h
                    
                    if current_ratio > target_ratio:
                        # Imagen muy ancha: añadimos margen arriba y abajo
                        new_w = w
                        new_h = int(w / target_ratio)
                    else:
                        # Imagen muy alta: añadimos margen a los lados
                        new_h = h
                        new_w = int(h * target_ratio)
                    
                    # Creamos fondo transparente (0,0,0,0) o blanco (255,255,255,255)
                    padding_img = Image.new("RGBA", (new_w, new_h), (255, 255, 255, 0))
                    
                    # Centramos la original
                    offset = ((new_w - w) // 2, (new_h - h) // 2)
                    padding_img.paste(img, offset, img)
                    
                    # Guardamos la imagen procesada
                    padding_img.save(destination_path, "PNG")                
                resources_front_matter.append(f'image: "{image_dest_filename}"')
                break
        else:
            continue
        break
    if website_url:
        resources_front_matter.append(f'website: "{website_url}"')

    md_content = f"""---
title: '{title}'
showDate: false
authors:
"""
    for author in authors_list:
        md_content += f'  - "{author}"\n'

    md_content += f"""publication: '{publication_source}'
publication_short: "" # Puedes usar esto para una versión corta del nombre de la conferencia
abstract: |-
{indented_abstract}
doi: "{doi}"
"""
    if resources_front_matter:
        md_content += "\n".join(resources_front_matter) + "\n"

    md_content += f"""
bibtex: |-
{textwrap.indent(text=bibtex_str, prefix="  ")}
---
"""

    with open(os.path.join(publication_path, "index.md"), "w", encoding="utf-8") as f:
        f.write(md_content)

print(
    f"\n¡Proceso completado! Se generaron {len(sorted_entries)} archivos de publicación en '{CONTENT_DIR}'."
)
