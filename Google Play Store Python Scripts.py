# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 17:48:27 2022

@author: dharm
"""

#Analysis of Global Play Store
#Datasets downloaded from Kaggle.com

# 1. import pandas and matplotlib libraries, read the 'google play store' and 
# 'googleplaystore user reviews' file as a dataframe #and print the first few rows of the file

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_columns', None)


gps = pd.read_csv(r'C:\Users\dharm\OneDrive\Desktop\Training\Python Project - Google Play Store\googleplaystore\googleplaystore.csv')
print(gps.head())

gps_user = pd.read_csv(r'C:\Users\dharm\OneDrive\Desktop\Training\Python Project - Google Play Store\googleplaystore_user_reviews\googleplaystore_user_reviews.csv')
print(gps_user.head())

# 2. Clean the Installs and Price columns. Check the datatypes of all the columns
# and change if required

print(gps[['Installs']])
print(gps[gps['Type']=='Paid'])

chars_remove = ['+',',','$']
cols_clean = ['Installs','Price']

for col in cols_clean:
    for char in chars_remove:
        gps[col] = gps[col].apply(lambda x: x.replace(char,''))
        
print(gps.head(20))

gps['Installs'] = gps['Installs'].astype('float')
gps['Price'] = gps['Price'].astype('float')

print(gps.dtypes)

# 3. Print the total number of apps, top5 Genres by number of apps 
# and the percentage of total. Average ratings by Genre

print(gps.Genres.value_counts().sum())
print(gps.Genres.value_counts().head(5))
print(gps.Genres.value_counts(normalize=True).head(5))
print(gps.groupby('Genres').mean())

# 4. Repeat the above analysis by category. Plot a bar chart by category and
# number of apps

print(gps.Category.value_counts().head(5))
print(gps.Category.value_counts(normalize=True).head(5))
print(gps.groupby('Category').mean())

num_apps = gps.Category.value_counts()
a=num_apps.index
b=num_apps.values

num_apps.plot(x=a,y=b,kind='bar',title='Num Apps by Category')

# 5. What is the percentage of paid apps and the average price of the paid apps by category

print(pd.pivot_table(gps,index='Category',columns='Type',aggfunc='size',fill_value=0))

# 6. Does size of the app effect the ratings, do paid apps have higher ratings? What is the
# distribution of these variables. Make Joint Plots to answer these questions

# check for null values and number of apps in each category
print(gps.isnull().sum())
print(gps.Category.value_counts())

# rating column has null values. select apps with no null values
apps_no_nulls = gps[gps['Rating'].notnull()]

# select categories with more than 200 apps to limit the number of categories

large_apps = apps_no_nulls.groupby('Category').filter(lambda x: len(x)>=200)

plt1 = sns.jointplot(x=large_apps['Size'],y=large_apps['Rating'])

plt2 = sns.jointplot(x=large_apps['Price'],y=large_apps['Rating'])

# 7. Does pricing of an app related to category, do some categories of apps have
# more expensive apps. Make a strip plot to answer this question. 
# List the top 20 most expensive apps

fig, ax = plt.subplots()
fig.set_size_inches(15,10)

popular_categories = large_apps[large_apps.Category.isin(['FAMILY','FINANCE','LIFESTYLE','MEDICAL','TOOLS','PHOTOGRAPHY','BUSINESS'])]

ax = sns.stripplot(x=popular_categories['Price'],y=popular_categories['Category'])

large_apps = large_apps.sort_values(by = ['Price'],ascending=False)
large_apps_price = large_apps.loc[:,['Category','App','Price']]
print(large_apps_price.head(20))






