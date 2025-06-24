import bibtexparser
# from datetime import datetime
from pylatexenc.latex2text import LatexNodes2Text

# Configuración
bib_file = "publications.bib"
output_html = "layouts/partials/publications_list.html"

# Inicializar el convertidor de LaTeX a texto plano (Unicode)
latex_converter = LatexNodes2Text()

# Parsear el .bib
try:
    with open(bib_file, 'r', encoding='utf-8') as f: # Especificar encoding utf-8
        bib_db = bibtexparser.load(f)
except FileNotFoundError:
    print(f"Error: El archivo {bib_file} no fue encontrado.")
    exit()
except Exception as e:
    print(f"Error al parsear el archivo .bib: {e}")
    exit()

# Ordenar publicaciones por año (descendente)
sorted_entries = sorted(
    bib_db.entries,
    key=lambda x: int(x.get("year", 0)),
    reverse=True
)

# HTML base
html_content = """
<!-- Lista generada automáticamente desde .bib -->
<ul class="publications-list">
"""

for i, entry in enumerate(sorted_entries):
    authors = latex_converter.latex_to_text(entry.get("author", "").replace(" and ", ", "))
    doi = entry.get("doi", "")
    # doi_link = f'<a href="https://doi.org/{doi}" target="_blank">DOI: {doi}</a>' if doi else ""
    title = entry.get("title", "")
    year = entry.get("year", "")
    isbn = entry.get("isbn", "")
    abstract = entry.get("abstract", "")
    
    # Mapeo de tipo de entrada a su fuente principal
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

    # Buscar campo principal
    field = source_fields.get(entry_type)
    publication_source = entry.get(field, "") if field else ""

    # Fallback si está vacío
    if not publication_source:
        for fallback in ("journal", "booktitle", "publisher", "school", "institution", "howpublished", "note"):
            publication_source = entry.get(fallback, "")
            if publication_source:
                break
    
    if doi:
        identifier = f'<a href="https://doi.org/{doi}" target="_blank">DOI: {doi}</a>'
    elif isbn:
        identifier = f"ISBN: {isbn}"
    else:
        identifier = ""
    # Generar BibTeX limpio
    bibtex_str = f"@{entry.get('ENTRYTYPE', 'article')}{{{entry.get('ID')},\n"
    for key, value in entry.items():
        if key not in ["ENTRYTYPE", "ID"]:
            bibtex_str += f"  {key} = {{{value}}},\n"
    bibtex_str += "}"

    html_content += f"""
    <li class="publication">
        <div class="publication-container">
            <h3 class="publication-title">{title}</h3>
            <p class="authors">Authors: {authors}</p>
            <p class="publication-meta">
                {year} | <em>{publication_source}</em> {identifier}
            </p>
            <div class="publication-buttons">
                <button onclick="toggleVisibility('abstract{i}')">Abstract</button>
                <button onclick="toggleVisibility('bib{i}')">BibTeX</button>
            </div>
            <div id="abstract{i}" class="abstract-block" style="display:none;">{abstract}</div>
            <div id="bib{i}" class="bibtex-block" style="display:none;"><pre>{bibtex_str}</pre></div>
        </div>
    </li>
    """

html_content += "</ul>"

# Agregar JS para mostrar/ocultar contenido
html_content += """
<style>
.publication-container {
  background-color: #ffffff;
  color: #1e293b;
  padding: 1rem;
  border-radius: 0.75rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
  transition: background-color 0.3s ease, color 0.3s ease;
}

html.dark .publication-container {
  background-color: #1c1f23;
  color: #e6e9ef;
  box-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

.publication-buttons button {
  background-color: #1d4ed8;
  color: #ffffff;
  border: none;
  border-radius: 0.375rem;
  padding: 0.45rem 0.9rem;
  margin-right: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.publication-buttons button:hover {
  background-color: #2563eb;
}

html.dark .publication-buttons button {
  background-color: #3b5bdb;
  color: #f8fafc;
}

html.dark .publication-buttons button:hover {
  background-color: #4c6ef5;
}

.authors, .publication-meta {
  color: #64748b;
}

html.dark .authors, html.dark .publication-meta {
  color: #9ca3af;
}
</style>

<script>
function toggleVisibility(id) {
    const abstractId = id.startsWith('abstract') ? id : id.replace('bib', 'abstract');
    const bibId = id.startsWith('bib') ? id : id.replace('abstract', 'bib');

    const elToShow = document.getElementById(id);
    const elToHide = document.getElementById(id === abstractId ? bibId : abstractId);

    if (elToShow.style.display === "none" || !elToShow.style.display) {
        elToShow.style.display = "block";
        elToHide.style.display = "none";
    } else {
        elToShow.style.display = "none";
    }
}
</script>
"""

# Guardar archivo
with open(output_html, "w") as f:
    f.write(html_content)

print(f"HTML generado en {output_html}")
