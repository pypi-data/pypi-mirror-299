from yubetsu_cite import Publication

# Create an instance of the Publication class
publication = Publication(
    authors=["John Doe", "Jane Smith", "Alice Johnson"],
    year=2024,
    month=9,
    title="A Comprehensive Study on Something Interesting",
    journal="Journal of Interesting Studies",
    volume=34,
    issue=2,
    pages="123-145",
    doi="10.1000/j.jis.2024.09.001"
)
# List of formats and styles to test
formats = ["APA", "MLA", "AMA", "NLM", "CHICAGO", "IEEE"]
styles = ["raw"] #, "html"]

# Run the tests
for fmt in formats:
    for style in styles:
        citation = publication.generate_citation(format_type=fmt, style=style)
        print(f"{fmt} ({style}):\n{citation}\n")

# BIBTEX
bibtex_citation = publication.generate_citation(format_type="BIBTEX")
print(f"BIBTEX:\n{bibtex_citation}")
