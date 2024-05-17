
# NLP Arabic Dialect Identification and Next Word Prediction

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v0.84.0+-red.svg)

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)
- [MADAR Citation](#madar-citation)

## Project Overview

Welcome to the **NLP Arabic Dialect Identification and Next Word Prediction** project! This project leverages advanced natural language processing techniques to offer two main functionalities:
1. **Next Word Prediction (Knowledge-Based)**: Uses an n-gram model to predict the next word in a given sentence with the MADAR dataset.
2. **Arabic Dialect Identification (Machine Learning)**: Utilizes a BERT model with lexicon features to identify the Arabic dialect of a given text, leveraging the MADAR dataset.

✨ **Experience the project live on [Streamlit](https://uj-nlp-project-maan-sulaimani.streamlit.app/)!** ✨

## Features
- Next Word Prediction using n-gram model
- Arabic Dialect Identification using BERT
- Interactive UI with Streamlit
- Comprehensive text preprocessing for Arabic

## Installation

### Prerequisites
- Python 3.x
- pip
- Streamlit

### Instructions
1. Clone the repository:
    ```sh
    git clone https://github.com/your_username/Project-Name.git
    cd UJ-NLP-Project
    ```
2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## How to Run

### Windows
1. Open Command Prompt or PowerShell.
2. Navigate to the project directory and run:
    ```cmd
    run.bat
    ```

### macOS and Linux
1. Open Terminal.
2. Navigate to the project directory and make the script executable:
    ```sh
    chmod +x run.sh
    ./run.sh
    ```

## Usage

### Next Word Prediction (Knowledge-Based)
1. Select "برنامج خمن الكلمة التالية (Knowledge Based)" from the sidebar.
2. Enter a sentence in Arabic.
3. Click "خمن الكلمات الجاية" to predict the next words.

### Arabic Dialect Identification (Machine Learning)
1. Select "برنامج تحديد اللهجات (Machine Learning)" from the sidebar.
2. Enter an Arabic text.
3. Click "حدد اللهجة" to identify the dialect.

## Roadmap
- Add more dialects
- Improve the prediction model
- Enhance the UI/UX

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit your Changes (\`git commit -m 'Add some AmazingFeature'\`)
4. Push to the Branch (\`git push origin feature/AmazingFeature\`)
5. Open a Pull Request

## License
Distributed under the MIT License.

## Contact
For any inquiries or feedback, feel free to reach out!

## Acknowledgments
- [MADAR Project](http://madar.camel-lab.com/)
- [Streamlit](https://www.streamlit.io/)
- [BERT](https://github.com/google-research/bert)
