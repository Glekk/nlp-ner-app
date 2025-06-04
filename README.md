# Ukrainian NER Model

A web application for Named Entity Recognition (NER) in Ukrainian text using a fine-tuned XLM-RoBERTa model.

## Features

- **Named Entity Recognition** for Ukrainian text
- **Web Interface**

## Project Structure

```
├── app.py                   # FastAPI web server
├── static/
│   └── ner_gui.html         # Web interface
├── src/
│   ├── add_model_bentoml.py # Model setup for BentoML
│   ├── bentoml_service.py   # BentoML service definition
│   └── utils.py             # NER result processing utilities
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. **Clone the repository** (or download the files):
   ```bash
   git clone <repository>
   cd ukrainian-ner
   ```

2. **Create or activate your python environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

### 1. Initialize the BentoML Model

First, you need to save the model to BentoML:

```bash
python src/add_model_bentoml.py
```

This will download and save the Ukrainian NER model (`glekk/xlm-roberta-base-ukrainian-ner-ukrner`) to BentoML.

### 2. Start the BentoML Service

In a separate terminal, start the model service:

```bash
bentoml serve src.bentoml_service:svc
```

The model service will be available at `http://localhost:3000`

### 3. Start the Web Application

In another terminal, start the FastAPI server:

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

The web application will be available at `http://localhost:8000`

Also, you can run the app using Docker:

```bash
docker-compose up --build
```

## Usage

1. **Open your browser** and go to `http://localhost:8000`

2. **Enter Ukrainian text** in the text area (there is a sample text provided for testing). 

3. **Click "Analyze Text"** to process the text

4. **View results** in the Detected Entities section, where named entities will be highlighted and categorized.
