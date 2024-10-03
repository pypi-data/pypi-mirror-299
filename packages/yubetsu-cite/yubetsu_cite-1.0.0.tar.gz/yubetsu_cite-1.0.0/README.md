# Yubetsu Cite Documentation

## Overview

`Yubetsu Cite` is a Python implementation that helps in generating formatted citations for academic publications in different styles, including APA, MLA, AMA, Chicago, NLM, and IEEE. The Publication class encapsulates all the necessary information related to a publication and provides methods to format the citation based on specified styles.

## Classes

### CitationError

```python
class CitationError(ValueError):
    """Custom exception for citation generation errors."""
```

-   **Description:** Custom exception raised when there are issues related to citation generation, such as missing mandatory fields.

### UnsupportedFormatError

```python
class UnsupportedFormatError(ValueError):
    """Exception raised for unsupported citation formats."""
```

-   **Description:** Custom exception raised when an unsupported citation format is requested.

### Publication

```python
class Publication:
```

**Attributes**

-   **authors** (`List[str]`): A list of author names.
-   **year** (`Optional[int]`): Year of publication (required).
-   **month** (`Optional[int]`): Month of publication (1-12).
-   **title** (`str`): Title of the article or work (required).
-   **journal** (`str`): Journal or container name (required).
-   **volume** (`Optional[int]`): Volume of the journal.
-   **issue** (`Optional[int]`): Issue number of the journal.
-   **pages** (`Optional[str]`): Page range (e.g., '23-45').
-   **doi** (`Optional[str]`): DOI of the article or permalink.
-   **database** (`Optional[str]`): Database name (e.g., Project MUSE).
-   **access_date** (`Optional[str]`): Date of access (for online sources).
-   **citekey** (`Optional[str]`): Unique key for citation generation.

**Initialization**

```python
def __init__(self, authors: List[str], year: Optional[int], month: Optional[int], title: str, journal: str, volume: Optional[int] = None, issue: Optional[int] = None, pages: Optional[str] = None, doi: Optional[str] = None, database: Optional[str] = None, access_date: Optional[str] = None, citekey: Optional[str] = None):
```

-   **Parameters:**
    -   `authors`: List of author names (required).
    -   `year`: Year of publication (required).
    -   `month`: Month of publication (optional).
    -   `title`: Title of the article or work (required).
    -   `journal`: Journal or container name (required).
    -   `volume`: Volume of the journal (optional).
    -   `issue`: Issue number of the journal (optional).
    -   `pages`: Page range (optional).
    -   `doi`: DOI of the article or permalink (optional).
    -   `database`: Database name (optional).
    -   `access_date`: Date of access (optional).
    -   `citekey`: Unique citation key (optional). If not provided, it defaults to the author's last name followed by the publication year.
-   **Raises:**
    -   `CitationError`: If any of the mandatory fields (`authors`, `title`, `journal`, `year`) are missing.

**Methods**

1. **format_author_apa**

    ```python
    def format_author_apa(self, author: str) -> str:
    ```

    - **Description**: Formats a single author's name into APA style (Last, F. M.).
    - **Parameters**:
        - `author`: The name of the author.
    - **Returns**: Formatted author name in APA style.
    - **Raises**: `CitationError` if the author's format is invalid.

2. **format_authors_apa**

    ```python
    def format_authors_apa(self) -> str:
    ```

    - **Description**: Formats the list of authors according to APA style.
    - **Returns**: A string of formatted authors in APA style.

3. **format_author_mla**

    ```python
    def format_author_mla(self, author: str, index: int, total_authors: int) -> str:
    ```

    - **Description**: Formats a single author's name into MLA style.
    - **Parameters**:
        - `author`: The name of the author.
        - `index`: The index of the author in the list.
        - `total_authors`: Total number of authors.
    - **Returns**: Formatted author name in MLA style.

4. **format_authors_mla**

    ```python
    def format_authors_mla(self) -> str:
    ```

    - **Description**: Formats the list of authors according to MLA style.
    - **Returns**: A string of formatted authors in MLA style.

5. **format_author_ama**

    ```python
    def format_author_ama(self, author: str) -> str:
    ```

    - **Description**: Formats a single author's name into AMA style (Last FirstInitial MiddleInitial).
    - **Parameters**:
        - `author`: The name of the author.
    - **Returns**: Formatted author name in AMA style.

6. **format_authors_ama**

    ```python
    def format_authors_ama(self) -> str:
    ```

    - **Description**: Formats the list of authors according to AMA style rules.
    - **Returns**: A string of formatted authors in AMA style.

7. **format_author_nlm**

    ```python
    def format_author_nlm(self, author: str) -> str:
    ```

    - **Description**: Formats a single author's name into NLM style.
    - **Parameters**:
        - `author`: The name of the author.
    - **Returns**: Formatted author name in NLM style.

8. **format_authors_nlm**

    ```python
    def format_authors_nlm(self) -> str:
    ```

    - **Description**: Formats the list of authors according to NLM style rules.
    - **Returns**: A string of formatted authors in NLM style.

9. **format_authors_chicago**

    ```python
    def format_authors_chicago(self) -> str:
    ```

    - **Description**: Formats the list of authors according to Chicago style rules.
    - **Returns**: A string of formatted authors in Chicago style.

10. **format_authors_ieee**

    ```python
    def format_authors_ieee(self, in_text: bool = False) -> str:
    ```

    - **Description**: Formats the list of authors according to IEEE style rules.
    - **Parameters**:
        - `in_text`: Boolean flag to indicate if the citation is in-text (default is False).
    - **Returns**: A string of formatted authors in IEEE style.

11. **generate_citation**

    ```python
    def generate_citation(self, format_type: str = "APA", style: str = "raw") -> str:
    ```

    - **Description**: Generates a citation in the specified format and style.
    - **Parameters**:
        - `format_type`: The citation format ('APA', 'MLA', 'AMA', 'NLM', 'CHICAGO', 'IEEE', 'BIBTEX').
        - `style`: The style in which the citation should be formatted ('raw' or 'html').
    - **Returns**: Formatted citation string.
    - **Raises**:
        - `UnsupportedFormatError`: If an unsupported format or style is specified.

12. **generate_apa_citation**

    ```python
    def generate_apa_citation(self, style: str) -> str:
    ```

    - **Description**: Generates a citation in APA style.
    - **Parameters**:
        - `style`: The desired output style ('raw' or 'html').
    - **Returns**: Formatted APA citation string.

13. **generate_mla_citation**

    ```python
    def generate_mla_citation(self, style: str) -> str:
    ```

    - **Description**: Generates a citation in MLA style.
    - **Parameters**:
        - `style`: The desired output style ('raw' or 'html').
    - **Returns**: Formatted MLA citation string.

14. **generate_ama_citation**

    ```python
    def generate_ama_citation(self, style: str) -> str:
    ```

    - **Description**: Generates a citation in AMA style.
    - **Parameters**:
        - `style`: The desired output style ('raw' or 'html').
    - **Returns**: Formatted AMA citation string.

15. **generate_raw_nlm_citation**

    ```python
    def generate_raw_nlm_citation(self) -> str:
    ```

    - **Description**: Generates a raw text NLM citation for a journal article.
    - **Returns**: Formatted raw NLM citation string.

16. **generate_html_nlm_citation**

    ```python
    def generate_html_nlm_citation(self) -> str:
    ```

    - **Description**: Generates an HTML formatted NLM citation for a journal article.
    - **Returns**: Formatted HTML NLM citation string.

17. **generate_raw_chicago_citation**

    ```python
    def generate_raw_chicago_citation(self) -> str:
    ```

    - **Description**: Generates a raw text Chicago-style citation for a journal article.
    - **Returns**: Formatted raw Chicago-style citation string.

18. **generate_html_chicago_citation**

    ```python
    def generate_html_chicago_citation(self) -> str:
    ```

    - **Description**: Generates an HTML formatted Chicago-style citation for a journal article.
    - **Returns**: Formatted HTML Chicago-style citation string.

19. **generate_ieee_citation**

    ```python
    def generate_ieee_citation(self, in_text: bool = False) -> str:
    ```

    - **Description**: Generates a citation in IEEE style.
    - **Parameters**:
        - `in_text`: Boolean flag to indicate if the citation is in-text (default is False).
    - **Returns**: Formatted IEEE citation string.

20. **generate_bibtex_citation**

    ```python
    def generate_bibtex_citation(self) -> str:
    ```

    - **Description**: Generates a BibTeX citation for the publication.
    - **Returns**: Formatted BibTeX citation string.

21. **generate**

## Example Usage

```python
# Creating a Publication instance
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

# Generating an APA citation
apa_citation = publication.generate_citation(format_type="APA")
print(apa_citation)

# Generating a MLA citation
mla_citation = publication.generate_citation(format_type="MLA")
print(mla_citation)
```

## Error Handling

The code includes custom exceptions to handle errors related to citation generation:

-   **CitationError**: Raised when required fields are missing or incorrectly formatted.
-   **UnsupportedFormatError**: Raised when an unsupported citation format is requested.

## Dependencies

This code does not require any external libraries and runs in any standard Python environment (Python 3.6+).

## Testing

The class is designed for straightforward unit testing. You can create instances of the `Publication` class and verify the output of citation formats by checking the generated strings against known good values.

## 📚 Resources

Here you can find useful links and attributions related to our project. Make sure to review the license and citation styles below.

### 🏢 Company Website

Learn more about our company and other projects we’re working on:

-   **Company Website**: [https://www.yubetsu.com](https://www.yubetsu.com)

### ⚖️ License and Attribution

This project is licensed under the **Apache License 2.0**. Please make sure to review the full license before using or modifying the project:

-   **License Information**: [https://www.apache.org/licenses/](https://www.apache.org/licenses/LICENSE-2.0)

### 📝 Citation Style Attributions

Yubetsu Cite supports several citation styles. Below are the references and attributions for these standards:

-   **APA Style**: APA Style Guide, 7th Edition
-   **MLA Style**: MLA Handbook, 9th Edition
-   **AMA Style**: AMA Manual of Style, 11th Edition
-   **IEEE Style**: IEEE Citation Guidelines
-   **Chicago Style**: Chicago Manual of Style, 17th Edition
-   **NLM Style**: National Library of Medicine Style Guide

### 📖 Further Reading

For additional resources on citation formats and academic writing, explore the links below:

-   **APA Style**: [https://apastyle.apa.org](https://apastyle.apa.org)
-   **MLA Style**: [https://style.mla.org](https://style.mla.org)
-   **AMA Style**: [https://www.amamanualofstyle.com](https://www.amamanualofstyle.com)
-   **IEEE Citation Reference**: [https://ieee.org](https://ieee.org)
-   **Chicago Manual of Style**: [https://www.chicagomanualofstyle.org](https://www.chicagomanualofstyle.org)
