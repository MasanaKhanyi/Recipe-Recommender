import requests
from bs4 import BeautifulSoup
import pandas as pd
import scraper_class
from tqdm import tqdm

# Jamie Oliver recipe website
url = "https://www.jamieoliver.com/recipes/category/course/mains/"
page = requests.get(url)

# Initializing DataFrame to store the scraped URLs
recipe_url_df = pd.DataFrame() 

# BeautifulSoup enables to find the elements/tags in a webpage
soup = BeautifulSoup(page.text, "html.parser")

# Selecting all the 'a' tags (URLs) present in the webpage and extracting 
# their 'href' attribute
recipe_urls = pd.Series([a.get("href") for a in soup.find_all("a")])

# All the recipes contain '-' and the '/recipes/' etc etc ...
recipe_urls = recipe_urls[(recipe_urls.str.count("-")>0) 
                         & (recipe_urls.str.contains("/recipes/")==True)
                         & (recipe_urls.str.contains("-recipes/")==True)
                         & (recipe_urls.str.contains("course")==False)
                         & (recipe_urls.str.contains("books")==False)
                         & (recipe_urls.str.endswith("recipes/")==False)
                         ].unique()

# DataFrame to store the scraped URLs
df = pd.DataFrame({"recipe_urls":recipe_urls})
df['recipe_urls'] = "https://www.jamieoliver.com" + df['recipe_urls'].astype('str')
# Appending 'df' to a main DataFrame 'init_urls_df'
recipe_df = pd.concat([recipe_url_df, df]).copy()


# The list of recipe attributes we want to scrape
attribs = ['recipe_name', 'subheading', 'serves', 'cooking_time', 'difficulty', 'ingredients', 'diet', 'tags','description', 'image_url']

# For each url (i) we add the attribute data to the i-th row
temp = pd.DataFrame(columns=attribs)
for i in tqdm(range(0,len(recipe_df['recipe_urls']))):
    url = recipe_df['recipe_urls'][i]
    recipe_scraper = scraper_class.JamieOliver(url)
    temp.loc[i] = [getattr(recipe_scraper, attrib)() for attrib in attribs]


# Put all the data into the same dataframe
temp['recipe_urls'] = recipe_df['recipe_urls']
columns = ['recipe_urls'] + attribs
JamieOliver_df = temp[columns]

#Output to csv file
JamieOliver_df.to_csv(r"data/JamieOliver_full.csv", index=False)