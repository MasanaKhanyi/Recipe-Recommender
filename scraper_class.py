import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
import re

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}

class JamieOliver():
    """ This class will output the recipe details. Recipes have the
    following properties:

    Attributes:
        url: The url of the recipe on Jamie Oliver site.
    """
    def __init__(self, url):
        self.url = url 
        self.soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    
    def recipe_name(self):
        """ Locates the recipe title """
        # Some of the urls are not recipe urls so to avoid errors we use try/except
        try:
            return self.soup.find('h1').text.strip()
        except Exception:
            return np.nan
        
    def serves(self):
        """ Locates the number of people the meal serves """
        try:
            return self.soup.find('div', {'class': 'recipe-detail serves'}).text.split(' ',1)[1]
        except Exception:
            return np.nan 

    def cooking_time(self):
        """ Locates the cooking time (in mins or hours and mins) """
        try:
            return self.soup.find('div', {'class': 'recipe-detail time'}).text.split('In')[1]
        except Exception:
            return np.nan


    def difficulty(self):
        """ Locates the cooking difficulty """
        try:
            return self.soup.find('div', {'class': 'col-md-12 recipe-details-col remove-left-col-padding-md'}).text.split('Difficulty')[1]
        except Exception:
            return np.nan

    def ingredients(self):
        """ Creating a vector containing the ingredients of the recipe """
        try:
            ingredients = []
            for li in self.soup.select('.ingred-list li'):
                ingred = ' '.join(li.text.split())
                ingredients.append(ingred)
            return ingredients
        except Exception:
            return np.nan
        
    
    def image_url(self):
        """ Creating a vector containing the ingredients of the recipe """
        try:
            return  self.soup.find('div', class_='hero-wrapper').find('img')['src']
        except Exception:
            return np.nan
        
    def diet(self):
        """ Creating a vector containing diet of recipe """
        try:
            diets= []
            for li in self.soup.select('.special-diets-list li'):
                    ingred = ' '.join(li.text.split())
                    diets.append(ingred)
            return diets
        except Exception:
            return np.nan
        
    def subheading(self):

        try:
            return self.soup.find('p', class_='subheading hidden-xs').text
        except Exception:
            return np.nan
            
    def tags(self):
        """ Creating a vector containing recipe tags """
        try:
            # Find all <a> tags within the .tags-list div
            links = self.soup.select('.tags-list a')
            # Extract and print the text of each <a> tag
            return [link.get_text(strip=True) for link in links]
        except Exception:
            return np.nan

    def description(self):
        try:
            return self.soup.find('div', class_='recipe-intro').text
        except Exception:
            return np.nan
            