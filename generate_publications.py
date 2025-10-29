import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text
import os
import re
import shutil
import textwrap
from pathlib import Path

# --- CONFIGURACIÓN ---
BIB_FILE = "publications.bib"
CONTENT_DIR = Path("content/publications")
SOURCE_FILES_DIR = Path("source_files")

# --- LIMPIEZA INICIAL ---
# Limpiar el directorio de contenido antiguo para evitar archivos huérfanos
CONTENT_DIR.mkdir(parents=True, exist_ok=True)
# Asegurarse de que el directorio de archivos fuente exista
if not SOURCE_FILES_DIR.exists():
    SOURCE_FILES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Directorio '{SOURCE_FILES_DIR}' no encontrado. Lo he creado por ti. "
          f"Por favor, coloca tus archivos (ej: 'tu_id.pdf') aquí.")

# --- FUNCIONES AUXILIARES ---
def slugify(text):
    """Convierte un texto en un 'slug' amigable para URLs."""
    text = text.lower()
    text = re.sub(r'[\s\W_]+', '-', text)
    text = text.strip('-')
    return text

def get_publication_source(entry):
    """Obtiene la fuente principal de la publicación (journal, booktitle, etc.)."""
    entry_type = entry.get("ENTRYTYPE", "").lower()
    source_fields = {
        "article": "journal", "inproceedings": "booktitle", "conference": "booktitle",
        "book": "publisher", "inbook": "booktitle", "incollection": "booktitle",
        "techreport": "institution", "phdthesis": "school", "mastersthesis": "school",
        "misc": "howpublished",
    }
    field = source_fields.get(entry_type)
    source = entry.get(field, "") if field else ""
    if not source:
        for fallback in ("journal", "booktitle", "publisher", "school", "institution", "howpublished", "note"):
            source = entry.get(fallback, "")
            if source: break
    return source

# --- SCRIPT PRINCIPAL ---
print("Iniciando la generación de contenido de publicaciones...")
latex_converter = LatexNodes2Text()

try:
    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        bib_db = bibtexparser.load(f)
except FileNotFoundError:
    print(f"Error: El archivo {BIB_FILE} no fue encontrado.")
    exit()

# Ordenar publicaciones por año (descendente)
sorted_entries = sorted(
    bib_db.entries,
    key=lambda x: int(x.get("year", 0)),
    reverse=True
)

# Crear el archivo _index.md para la sección /publications
with open(os.path.join(CONTENT_DIR, "_index.md"), "w", encoding='utf-8') as f:
    f.write("---\n")
    f.write("title: 'Publications'\n")
    # f.write("layout: 'list'\n")  # Usará layouts/publications/list.html
    f.write("draft: false\n")
    f.write("showDate: false\n")
    # f.write("date: 2022-06-13T20:55:37+01:00\n")
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





# Procesar cada entrada del BibTeX
for entry in sorted_entries:
    # 1. OBTENER IDENTIFICADORES Y CREAR RUTAS
    entry_id = entry.get('ID')
    if not entry_id:
        print(f"Advertencia: Se omitió una entrada porque no tiene ID. Título: {entry.get('title', 'N/A')}")
        continue
        
    slug = slugify(entry_id)
    publication_path = os.path.join(CONTENT_DIR, slug)
    os.makedirs(publication_path, exist_ok=True)

    # 2. EXTRAER Y LIMPIAR METADATOS
    title = latex_converter.latex_to_text(entry.get("title", "")).replace("'", "''")
    authors_list = [latex_converter.latex_to_text(a.strip()) for a in entry.get("author", "").split(" and ")]
    # abstract_raw = latex_converter.latex_to_text(entry.get("abstract", "")).strip()
    abstract_from_bib = entry.get("abstract", "")
    safe_abstract = abstract_from_bib.replace('%', r'\%')
    # Ahora procesamos la cadena segura, que ya no tiene '%' problemáticos.
    abstract_raw = latex_converter.latex_to_text(safe_abstract).strip()
    indented_abstract = textwrap.indent(text=abstract_raw, prefix='  ')
    year = entry.get("year", "")
    publication_source = latex_converter.latex_to_text(get_publication_source(entry)).replace("'", "''")
    doi = entry.get("doi", "")
    website_url = entry.get("url", "") # Para el botón "Website"
    
    # Generar BibTeX limpio para esta entrada específica
    db = bibtexparser.bibdatabase.BibDatabase()
    db.entries = [entry]
    bibtex_str = bibtexparser.dumps(db)

    # 3. MANEJAR RECURSOS (PDF, SLIDES, ETC.) - Lógica de Page Bundles
    resources_front_matter = []

    # Buscar y copiar PDF
    pdf_source_path = os.path.join(SOURCE_FILES_DIR, f"{entry_id}.pdf")
    if os.path.exists(pdf_source_path):
        pdf_dest_filename = f"{slug}.pdf"
        shutil.copy(pdf_source_path, os.path.join(publication_path, pdf_dest_filename))
        resources_front_matter.append(f'pdf: "{pdf_dest_filename}"')

    # Buscar y copiar Slides
    slides_source_path = os.path.join(SOURCE_FILES_DIR, f"{entry_id}_slides.pdf")
    if os.path.exists(slides_source_path):
        slides_dest_filename = f"{slug}_slides.pdf"
        shutil.copy(slides_source_path, os.path.join(publication_path, slides_dest_filename))
        resources_front_matter.append(f'slides: "{slides_dest_filename}"')

    image_copied = False        
    image_extensions = ['.jpg', '.jpeg', '.png']
    for ext in image_extensions:
        image_source_path = SOURCE_FILES_DIR / f"{entry_id}{ext}"
        if image_source_path.exists():
            image_dest_filename = f"featured{ext}" # Esta es una cadena (str)
            destination_path = publication_path / Path(image_dest_filename)
            destination_path.write_bytes(image_source_path.read_bytes())
            resources_front_matter.append(f'image: "{image_dest_filename}"')  
            image_copied = True
            break


    # Añadir enlace al sitio web si existe
    if website_url:
        resources_front_matter.append(f'website: "{website_url}"')

    # 4. CONSTRUIR Y ESCRIBIR EL ARCHIVO index.md
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
    # Añadir los recursos encontrados al front matter
    if resources_front_matter:
        md_content += "\n".join(resources_front_matter) + "\n"

    md_content += f"""
bibtex: |-
{textwrap.indent(text=bibtex_str, prefix='  ')}
---
"""
    # El cuerpo del markdown puede estar vacío. Puedes añadir notas adicionales aquí si quieres.

    with open(os.path.join(publication_path, "index.md"), "w", encoding='utf-8') as f:
        f.write(md_content)

print(f"\n¡Proceso completado! Se generaron {len(sorted_entries)} archivos de publicación en '{CONTENT_DIR}'.")