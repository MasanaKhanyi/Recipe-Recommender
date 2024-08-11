

from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch
import ast
# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')


# Function to convert list to tensor
def row_to_tensor(row):
    return torch.tensor(ast.literal_eval(row), dtype=torch.float)

def search_recipe_nlp(prompt, df, model):
    # Generate the embedding for the user prompt
    prompt_embedding = model.encode(prompt)
    
    # Compute the cosine similarity between the prompt and the recipe embeddings
    df['similarity'] = df['embedding'].apply(lambda x: util.cos_sim(prompt_embedding, x).item())
    
    # Find the recipe with the highest similarity score
    best_match = df.loc[df['similarity'].idxmax()]
    
    # Return the recipe details if similarity is above a certain threshold
    if best_match['similarity'] > 0.5:  # Adjust threshold as needed
        return best_match[['recipe_name', 'subheading', 'serves', 'cooking_time', 'difficulty', 'ingredients', 'diet', 'tags', 'description']]
    else:
        return "No matching recipes found."

if __name__ == "__main__":
    model = SentenceTransformer('all-MiniLM-L6-v2')
    recipe_df = pd.read_csv("data/clean_data.csv")
    recipe_df['embedding'] = recipe_df['combined'].apply(lambda x: model.encode(x))

    print("Embedding Data...")

    # Example usage
    user_prompt = input("What kind of recipe are you in the mood for? : ")
    result = search_recipe_nlp(user_prompt, recipe_df, model)
    print(result)
