
---

# Recipe Recommendation System

## Overview

This project is an recipe recommendation system designed to cater to individual dietary preferences and needs. The system leverages  data science techniques and transformer-based language models to analyse and suggest recipes that align with users requirements.

## Features

- **Personalised Recommendations**: The system tailors recipe suggestions based on user input, including preferred ingredients, cooking time, and difficulty level.
- **Dietary Filters**: Supports filtering recipes by dietary requirements, such as vegan, vegetarian, dairy-free, and gluten-free.
- **Exploratory Data Analysis (EDA)**: Includes tools for analyzing and visualizing the dataset to understand trends and distributions.
- **Data Cleaning and Preprocessing**: Automated cleaning and preprocessing of recipe data to ensure high-quality inputs for the recommendation engine.


## Installation

### Prerequisites

- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/installation/) (Python package manager)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MasanaKhanyi/Recipe-Recommender.git
   cd Recipe-Recommender
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the project**:
   ```bash
   python get_recipes.py
   ```

## Usage

### Data Preprocessing

Before using the recommendation system, ensure that the data is properly cleaned and preprocessed:

```bash
   python data_cleaning.py
   ```

### Web Scraping

The data used in this project was scraped from  [JamieOliver.com](https://www.jamieoliver.com/). To run the scraper run:

```bash
   python scaper.py
   ```





