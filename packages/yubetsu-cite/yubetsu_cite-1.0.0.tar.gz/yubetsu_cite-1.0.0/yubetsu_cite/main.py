import re
from typing import List, Optional


class CitationError(ValueError):
    """Custom exception for citation generation errors."""
    pass


class UnsupportedFormatError(ValueError):
    """Exception raised for unsupported citation formats."""
    pass


class Publication:
    def __init__(self,
                 authors: List[str],
                 year: Optional[int],
                 month: Optional[int],
                 title: str,
                 journal: str,
                 volume: Optional[int] = None,
                 issue: Optional[int] = None,
                 pages: Optional[str] = None,
                 doi: Optional[str] = None,
                 database: Optional[str] = None,
                 access_date: Optional[str] = None,
                 citekey: Optional[str] = None):
        """
        Initialize the Publication class.

        :param authors: List of author names (various formats are supported)
        :param year: Year of publication
        :param title: Title of the article or work
        :param journal: Journal or container name
        :param volume: Volume of the journal
        :param issue: Issue number of the journal
        :param pages: Page range (e.g., '23-45')
        :param doi: DOI of the article or permalink
        :param database: Database name (e.g., Project MUSE)
        :param access_date: Date of access (for online sources)
        :raises CitationError: If mandatory fields are missing
        """
        if not authors or not all(authors):
            raise CitationError("Authors are required and cannot be empty.")
        if not title:
            raise CitationError("Title is required and cannot be empty.")
        if not journal:
            raise CitationError("Journal or container name is required and cannot be empty.")
        if not year:
            raise CitationError("Year is required and cannot be empty.")

        self.authors = authors
        self.year = year
        self.month = month
        self.title = title
        self.journal = journal
        self.volume = volume
        self.issue = issue
        self.pages = pages
        self.doi = doi
        self.database = database
        self.access_date = access_date
        self.citekey = citekey if citekey else f"{authors[0].split()[-1].lower()}{year}"  # Default citekey
        self.MONTHS = [
        "",  # Placeholder for index 0
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    def format_author_apa(self, author: str) -> str:
        """Formats author names into APA style (Last, F. M.)."""
        name_parts = re.split(r'\s+', author.strip())
        if len(name_parts) < 2:
            raise CitationError(f"Invalid author format: {author}")

        last_name = name_parts[-1]
        initials = ' '.join([f"{part[0]}." for part in name_parts[:-1] if len(part) > 0])
        return f"{last_name}, {initials}"

    def format_authors_apa(self) -> str:
        """Formats the list of authors according to APA style."""
        formatted_authors = [self.format_author_apa(author) for author in self.authors]
        if len(formatted_authors) == 1:
            return formatted_authors[0]
        elif len(formatted_authors) == 2:
            return f"{formatted_authors[0]} & {formatted_authors[1]}"
        elif len(formatted_authors) <= 20:
            return ', '.join(formatted_authors[:-1]) + f", & {formatted_authors[-1]}"
        else:
            return ', '.join(formatted_authors[:19]) + ", ... " + formatted_authors[-1]

    def format_author_mla(self, author: str, index: int, total_authors: int) -> str:
        """
        Converts author names into MLA style (First Last) and applies MLA rules for multiple authors.
        :param author: Author name string in various formats
        :param index: Author index to determine whether to apply 'et al.' for 3+ authors
        :param total_authors: Total number of authors in the list
        :return: Formatted author string in MLA style
        """
        name_parts = re.split(r'\s+', author.strip())
        if len(name_parts) < 2:
            raise CitationError(f"Invalid author format: {author}")

        first_name = ' '.join(name_parts[:-1])
        last_name = name_parts[-1]

        # MLA rules for multiple authors
        if total_authors == 1:
            return f"{last_name}, {first_name}"
        elif total_authors == 2:
            if index == 0:
                return f"{last_name}, {first_name}"
            elif index == 1:
                return f"and {first_name} {last_name}"
        elif total_authors > 2 and index == 0:
            return f"{last_name}, {first_name} et al"

    def format_authors_mla(self) -> str:
        """
        Formats the list of authors according to MLA style and multiple author rules.
        :return: Formatted authors in MLA style
        """
        formatted_authors = []
        total_authors = len(self.authors)

        for index, author in enumerate(self.authors):
            formatted_author = self.format_author_mla(author, index, total_authors)
            if formatted_author:
                formatted_authors.append(formatted_author)

        return ' '.join(formatted_authors)

    def format_author_ama(self, author: str) -> str:
        """Formats author names into AMA style (Last FirstInitial MiddleInitial)."""
        name_parts = re.split(r'\s+', author.strip())
        if len(name_parts) < 2:
            raise CitationError(f"Invalid author format: {author}")

        last_name = name_parts[0]
        first_initial = name_parts[1][0] if len(name_parts) > 1 else ''
        middle_initial = name_parts[2][0] if len(name_parts) > 2 else ''
        
        formatted_name = f"{last_name} {first_initial}"
        if middle_initial:
            formatted_name += f"{middle_initial}"
        return formatted_name

    def format_authors_ama(self) -> str:
        """Formats the list of authors according to AMA style rules."""
        total_authors = len(self.authors)
        formatted_authors = [self.format_author_ama(author) for author in self.authors]

        if total_authors > 6:
            return ', '.join(formatted_authors[:3]) + ", et al."
        else:
            return ', '.join(formatted_authors)

    def format_author_nlm(self, author: str) -> str:
        """Formats author names into NLM style."""
        name_parts = re.split(r'\s+', author.strip())
        if len(name_parts) < 2:
            raise CitationError(f"Invalid author format: {author}")
        last_name = name_parts[0]
        first_initial = name_parts[1][0] if len(name_parts) > 1 else ''
        middle_initial = name_parts[2][0] if len(name_parts) > 2 else ''
        formatted_name = f"{last_name} {first_initial}"
        if middle_initial:
            formatted_name += f"{middle_initial}"
        return formatted_name

    def format_authors_nlm(self) -> str:
        """Formats the list of authors according to NLM style rules."""
        formatted_authors = [self.format_author_nlm(author) for author in self.authors]
        total_authors = len(formatted_authors)
        if total_authors > 3:
            return ', '.join(formatted_authors[:3]) + ", and others"
        else:
            return ', '.join(formatted_authors)

    def format_authors_chicago(self) -> str:
        """Formats the list of authors according to Chicago style rules."""
        if len(self.authors) == 0:
            raise CitationError("No authors provided.")
        elif len(self.authors) == 1:
            return self.authors[0]
        elif len(self.authors) == 2:
            return f"{self.authors[0]} and {self.authors[1]}"
        elif len(self.authors) == 3:
            return f"{', '.join(self.authors[:-1])}, and {self.authors[-1]}"
        else:
            return f"{self.authors[0]} et al."

    def format_authors_ieee(self, in_text: bool = False) -> str:
        """Formats the list of authors according to IEEE style rules."""
        formatted_authors = [f"{author.split()[0][0]}. {author.split()[-1]}" for author in self.authors]
        if in_text:
            return f"{formatted_authors[0]} et al." if len(formatted_authors) >= 3 else ", ".join(formatted_authors[:-1]) + " and " + formatted_authors[-1]
        return f"{formatted_authors[0]} et al." if len(formatted_authors) >= 6 else ", ".join(formatted_authors[:-1]) + " and " + formatted_authors[-1]
    
    def generate_citation(self, format_type: str = "APA", style: str = "raw") -> str:
        """
        Generates a citation in the specified format and style.
        :param format_type: The citation format ('APA', 'MLA', 'AMA')
        :param style: The style in which the citation should be formatted ('raw' or 'html')
        :return: Formatted citation string
        """
        format_type = format_type.upper()
        if format_type == "APA":
            return self.generate_apa_citation(style)
        elif format_type == "MLA":
            return self.generate_mla_citation(style)
        elif format_type == "AMA":
            return self.generate_ama_citation(style)
        elif format_type.upper() == "NLM":
            if style == 'raw':
                return self.generate_raw_nlm_citation()
            elif style == 'html':
                return self.generate_html_nlm_citation()
            else:
                raise UnsupportedFormatError(f"{style} style is not supported.")
        elif format_type.upper() == "CHICAGO":
            if style == 'raw':
                return self.generate_raw_chicago_citation()
            elif style == 'html':
                return self.generate_html_chicago_citation()
            else:
                raise UnsupportedFormatError(f"{style} style is not supported.")
        elif format_type.upper() == "IEEE":
            if style == 'raw':
                return self.generate_raw_ieee_citation()
            elif style == 'html':
                return self.generate_html_ieee_citation()
            else:
                raise UnsupportedFormatError(f"{style} style is not supported.")
        elif format_type.upper() == "BIBTEX":
            return self.generate_bibtex()
        else:
            raise UnsupportedFormatError(f"{format_type} format is not supported.")

    def generate_apa_citation(self, style: str) -> str:
        """Generates a citation in APA style."""
        if style == 'raw':
            citation = f"{self.format_authors_apa()} ({self.year}). {self.title}. {self.journal}"
            if self.volume:
                citation += f", {self.volume}"
            if self.issue:
                citation += f"({self.issue})"
            if self.pages:
                citation += f", {self.pages}"
            citation += f". https://doi.org/{self.doi}"
            return citation
        elif style == 'html':
            citation = f"{self.format_authors_apa()} ({self.year}). <i>{self.title}</i>. <i>{self.journal}</i>"
            if self.volume:
                citation += f", <b>{self.volume}</b>"
            if self.issue:
                citation += f"({self.issue})"
            if self.pages:
                citation += f", {self.pages}"
            citation += f". <a href='https://doi.org/{self.doi}'>https://doi.org/{self.doi}</a>"
            return citation
        else:
            raise CitationError("Invalid style type. Use 'raw' or 'html'.")

    def generate_mla_citation(self, style: str) -> str:
        """Generates a citation in MLA style."""
        if style == 'raw':
            authors = self.format_authors_mla()
            citation = f"{authors}. \"{self.title}.\" {self.journal}"
            if self.volume:
                citation += f", vol. {self.volume}"
            if self.issue:
                citation += f", no. {self.issue}"
            if self.pages:
                citation += f", pp. {self.pages}"
            citation += f", {self.year}."
            if self.database:
                citation += f" {self.database}."
            if self.doi:
                citation += f" doi:{self.doi}."
            return citation
        elif style == 'html':
            authors = self.format_authors_mla()
            citation = f"{authors}. \"<i>{self.title}</i>.\" <i>{self.journal}</i>"
            if self.volume:
                citation += f", vol. {self.volume}"
            if self.issue:
                citation += f", no. {self.issue}"
            if self.pages:
                citation += f", pp. {self.pages}"
            citation += f", {self.year}."
            if self.database:
                citation += f" <i>{self.database}</i>."
            if self.doi:
                citation += f" doi:<a href='https://doi.org/{self.doi}'>{self.doi}</a>."
            return citation
        else:
            raise CitationError("Invalid style type. Use 'raw' or 'html'.")

    def generate_ama_citation(self, style: str) -> str:
        """Generates a citation in AMA style."""
        if style == 'raw':
            authors = self.format_authors_ama()
            citation = f"{authors}. {self.title}. {self.journal}. {self.year};"
            if self.volume:
                citation += f"{self.volume}"
            if self.issue:
                citation += f"({self.issue})"
            if self.pages:
                citation += f":{self.pages}."
            if self.doi:
                citation += f" doi:{self.doi}."
            return citation
        elif style == 'html':
            authors = self.format_authors_ama()
            citation = f"{authors}. <i>{self.title}</i>. <i>{self.journal}</i>. {self.year};"
            if self.volume:
                citation += f" {self.volume}"
            if self.issue:
                citation += f"({self.issue})"
            if self.pages:
                citation += f":{self.pages}."
            if self.doi:
                citation += f" doi:<a href='https://doi.org/{self.doi}'>{self.doi}</a>."
            return citation
        else:
            raise CitationError("Invalid style type. Use 'raw' or 'html'.")

    def generate_raw_nlm_citation(self) -> str:
        """Generates a raw text NLM citation for a journal article."""
        authors = self.format_authors_nlm()
        citation = f"{authors}. {self.title}. {self.journal}."
        month_name = self.MONTHS[self.month] if self.month else ""
        citation += f" {self.year} {month_name};" if month_name else f" {self.year};"
        if self.volume:
            citation += f"{self.volume}"
        if self.issue:
            citation += f"({self.issue})"
        if self.pages:
            citation += f":{self.pages}"
        if self.doi:
            citation += f". doi:{self.doi}."
        return citation

    def generate_html_nlm_citation(self) -> str:
        """Generates an HTML formatted NLM citation for a journal article."""
        authors = self.format_authors_nlm()
        citation = f"{authors}. {self.title}. {self.journal}."
        month_name = self.MONTHS[self.month] if self.month else ""
        citation += f" {self.year} {month_name};" if month_name else f" {self.year};"
        if self.volume:
            citation += f"{self.volume}"
        if self.issue:
            citation += f"({self.issue})"
        if self.pages:
            citation += f":{self.pages}"
        if self.doi:
            citation += f". doi:<a href='https://doi.org/{self.doi}'>{self.doi}</a>."
        return citation

    def generate_raw_chicago_citation(self) -> str:
        """Generates a raw text Chicago-style citation for a journal article."""
        authors = self.format_authors_chicago()
        month_name = self.MONTHS[self.month] if self.month else ""
        month_part = f" ({month_name} {self.year})" if month_name else f" ({self.year})"
        citation = f"{authors}. \"{self.title}.\" {self.journal} {self.volume}, no. {self.issue}{month_part}: {self.pages}."
        if self.doi:
            citation += f" https://doi.org/{self.doi}."
        return citation

    def generate_html_chicago_citation(self) -> str:
        """Generates an HTML formatted Chicago-style citation for a journal article."""
        authors = self.format_authors_chicago()
        month_name = self.MONTHS[self.month] if self.month else ""
        month_part = f" ({month_name} {self.year})" if month_name else f" ({self.year})"
        citation = f"{authors}. \"<i>{self.title}</i>.\" <i>{self.journal}</i> {self.volume}, no. {self.issue}{month_part}: {self.pages}."
        if self.doi:
            citation += f" <a href='https://doi.org/{self.doi}'>https://doi.org/{self.doi}</a>."
        return citation

    def generate_raw_ieee_citation(self) -> str:
        """Generates a raw text IEEE-style citation for a journal article."""
        authors = self.format_authors_ieee()
        citation = f"{authors}, \"{self.title},\" {self.journal}, vol. {self.volume}, no. {self.issue}, pp. {self.pages}, {self.year}."
        if self.doi:
            citation += f" doi: {self.doi}."
        return citation

    def generate_html_ieee_citation(self) -> str:
        """Generates an HTML formatted IEEE-style citation for a journal article."""
        authors = self.format_authors_ieee()
        citation = f"{authors}, \"<i>{self.title}</i>,\" <i>{self.journal}</i>, vol. {self.volume}, no. {self.issue}, pp. {self.pages}, {self.year}."
        if self.doi:
            citation += f" doi: <a href='https://doi.org/{self.doi}'>{self.doi}</a>."
        return citation

    def generate_bibtex(self) -> str:
        """Generates a BibTeX entry for the publication."""
        entry_type = "article"
        authors_bibtex = " and ".join(self.authors)
        citation = f"@{entry_type}{{{self.citekey},\n"
        citation += f"  author = {{{authors_bibtex}}},\n"
        citation += f"  title = {{{self.title}}},\n"
        citation += f"  journal = {{{self.journal}}},\n"
        citation += f"  year = {{{self.year}}},\n"
        if self.volume:
            citation += f"  volume = {{{self.volume}}},\n"
        if self.issue:
            citation += f"  number = {{{self.issue}}},\n"
        if self.pages:
            pages = "--".join(self.pages.split("-"))
            citation += f"  pages = {{{pages}}},\n"
        if self.doi:
            citation += f"  doi = {{{self.doi}}},\n"
        citation += "}"
        return citation
