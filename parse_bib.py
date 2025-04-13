import bibtexparser
from datetime import datetime

# Configuración
bib_file = "publications.bib"
output_html = "layouts/partials/publications_list.html"

# Parsear el .bib
with open(bib_file) as f:
    bib_db = bibtexparser.load(f)

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
    authors = entry.get("author", "").replace(" and ", ", ")
    doi = entry.get("doi", "")
    doi_link = f'<a href="https://doi.org/{doi}" target="_blank">DOI: {doi}</a>' if doi else ""
    title = entry.get("title", "")
    year = entry.get("year", "")
    journal = entry.get("journal", "")
    abstract = entry.get("abstract", "")
    
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
                {year} | <em>{journal}</em> {doi_link}
            </p>
            <div class="publication-buttons">
                <button onclick="toggleVisibility('abstract{i}')">Summary</button>
                <button onclick="toggleVisibility('bib{i}')">Abstract</button>
            </div>
            <div id="abstract{i}" class="abstract-block" style="display:none;">{abstract}</div>
            <div id="bib{i}" class="bibtex-block" style="display:none;"><pre>{bibtex_str}</pre></div>
        </div>
    </li>
    """

html_content += "</ul>"

# Agregar JS para mostrar/ocultar contenido
html_content += """
<script>
function toggleVisibility(id) {
    const el = document.getElementById(id);
    if (el.style.display === "none" || !el.style.display) {
        el.style.display = "block";
    } else {
        el.style.display = "none";
    }
}
</script>
"""

# Guardar archivo
with open(output_html, "w") as f:
    f.write(html_content)

print(f"HTML generado en {output_html}")
