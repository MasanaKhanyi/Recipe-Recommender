
import pandas as pd
import matplotlib.pyplot as plt 
import spacy
import ast
import numpy as np
from tqdm import tqdm
import re
from sentence_transformers import SentenceTransformer, util
import pandas as pd

nlp = spacy.load("en_core_web_sm")

normalization_dict = {
    'Vegetarian': 'vegetarian',
    'Dairy-free': 'dairy-free',
    'Vegan': 'vegan',
    'Gluten-free': 'gluten-free'
}

difficulty = {
    'Super easy': 'easy',
    'Not too tricky': 'medium',
    'Showing off': 'hard'
}

measurements = re.compile(r'(kg|organic|ml|litre|fresh|whole|bowl|bulb|cube|clove|cup|drop|ounce|oz|pinch|pound|teaspoon|tablespoon)s?')



# Function to remove measurements and then keep only nouns and adjectives
def preprocess_ingregients(ingredient):
    # Remove numbers and units of measurement (like litres, g, ml, etc.)
    #ingredient = ast.literal_eval(ingredient)
    ingredient = ast.literal_eval(ingredient)
    ingredients_list = []
    for ing in ingredient:
        cleaned_ingredient = re.sub(r'\b\d+\s*(litres|g|cloves|bunch|ml|kg|oz|tbsp|tsp|cup|cups|sprigs|pound|pounds|lb|lbs|inch|inches|cm|mm)\b', '', ing)
        
        # Process the cleaned ingredient text with spaCy
        doc = nlp(cleaned_ingredient)
        # Extract and join only the nouns and adjectives
        relevant_words = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]
        ing = " ".join(relevant_words)
        ingredients_list.append(ing)


    return ", ".join(ingredients_list)



def normalize_and_deduplicate(lst):
    # Remove duplicates by converting the list to a set and back to a list\

    remove_duplicates = set(ast.literal_eval(lst))
    
    # Normalize the values using the dictionary
    normalized_lst = []
    for item in remove_duplicates:
        for key in normalization_dict:
            if key in item:
                normalized_lst.append(normalization_dict[key])
                break  # Stop after the first match to avoid multiple additions

    return " ".join(normalized_lst)


def set_difficulty(value):
    return difficulty.get(str(value).strip()) if value != np.nan else np.nan

def clean_column(df, col_name, preprocess_func=None):
    if col_name in df.columns:
        df[col_name] = df[col_name].apply(preprocess_func)
    return df

def embbed_columns(recipe_df):
    
# Load the pre-trained model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Combine relevant columns into a single string
    recipe_df['combined'] = recipe_df.apply(
        lambda row: ' '.join([
            str(row['recipe_name']),
            str(row['subheading']),
            str(row['serves']),
            str(row['cooking_time']),
            str(row['difficulty']),
            str(row['ingredients']),
            str(row['diet']),
            str(row['tags']),
            str(row['description'])
        ]), axis=1
    )

    # Generate embeddings for each recipe
    recipe_df['embedding'] = tqdm(recipe_df['combined'].apply(lambda x: model.encode(x)))



def clean_data(recipe_df):
    # Drop no name recipes
    recipe_df.dropna(subset=['recipe_name'], inplace=True)

    # Define preprocessing functions for different columns
    preprocess_funcs = {
        'recipe_name': lambda x: x.strip(),
        'subheading': lambda x: x.strip() if pd.notna(x) else x,
        'description': lambda x: x.strip().strip('\"').strip("\'") if pd.notna(x) else x,
        'ingredients': lambda x: preprocess_ingregients(x),
        'diet': lambda x: normalize_and_deduplicate(x),
        'tags': lambda x: ", ".join(ast.literal_eval(x)),
        'difficulty': set_difficulty
    }

    # Apply cleaning and preprocessing
    for col, func in tqdm(preprocess_funcs.items()):
        recipe_df = clean_column(recipe_df, col, func)

    
if __name__ == "__main__":

    recipe_df = pd.read_csv("data/JamieOliver_full.csv")

    print("Preprocessing Data")
    clean_data(recipe_df)
    print("Creating Embeddings")
    embbed_columns(recipe_df)
    recipe_df.to_csv(r"data/clean_data.csv", index=False)
    print("Done")
