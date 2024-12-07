# Text to SQL Generator

A Python application that converts natural language queries to SQL using Gemini Pro AI model. This tool helps users generate SQL queries without needing to know SQL syntax.

## Features

- Natural language to SQL conversion
- Support for common database operations
- Interactive query generation

## Prerequisites

- Python 3.8 or higher
- Google API key for Gemini Pro
- Required Python packages

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/text-to-sql.git
cd text-to-sql

**## Create and activate virtual environment**
# If anaconda installed in your system then directly use conda to create virtual env
1. conda create -p venv python=3.13 -y
2. conda activate venv/

OR
# Create virtual env by using python
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Installed required packages
pip install -r requirements.txt
 
# Setup google api key
# Link to create a google api key: https://makersuite.google.com/app/apikey

## run application
streamlit run app.py



