<!--- Heading --->
<div align="center">
  <h1>ak_pdf2md</h1>
  <p>
    Convert PDFs to Markdown using llamaparse 
  </p>
</div>
<br />

<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Production](#production)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

<!-- About the Project -->
## About the Project


<!-- Getting Started -->
## Getting Started

<!-- Prerequisites -->
### Prerequisites

Python 3.11 or above

LLamaParse [API Key](https://cloud.llamaindex.ai/login) from Llamacloud

<!-- Installation -->
### Installation

#### Production

```bash
  pip install ak_pdf2md
```

<!-- Usage -->
## Usage

**Python**

```python
from ak_pdf2md import test_config, pdfparser

test_config() # Test if config.toml has been correctly set up

# Convert to markdown in same dir
pdfparser.convert(filepath="/path/to/pdf")

# Explicit Conversion
pdfparser.convert(filepath="/path/to/pdf", dest_dir="/dest", extension=".md")

#Can pass additional parser commands per #https://docs.cloud.llamaindex.ai/llamaparse/features/parsing_options
pdfparser.convert(
    filepath="/path/to/pdf", 
    parsing_instruction="You are parsing a receipt from a restaurant."
  )

```

**Terminal**

```bash
app --help    # Input Help

test          # Test if config is correctly setup
```

<!-- License -->
## License

See [LICENSE](/LICENSE) for more information.

<!-- Contact -->
## Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/ak_pdf2md](https://github.com/rpakishore/ak_pdf2md)
