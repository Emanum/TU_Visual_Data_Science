import pandas as pd
import itertools
import re
import math
import numpy as np

def get_unique(series):
    """Get unique values from a Pandas series containing semi-colon delimited strings."""
    return set(list(itertools.chain(*series.apply(lambda x: [c for c in x.split(';')]))))

def process_cat_gen_tag(df):
    """Process categories, genres, steamspy_tags and platform columns."""
    # get all unique plattform names
    plat_cols = get_unique(df['platforms'])
    
    # create a new column for each platform, with 1s indicating membership and 0s for non-members
    for col in sorted(plat_cols):
        plat_name = re.sub(r'[\s\-\/]', '_', col.lower())
        plat_name = re.sub(r'[()]', '', plat_name)
        
        df[plat_name] = df['platforms'].apply(lambda x: 1 if col in x.split(';') else 0)
    
    # get all unique category names
    cat_cols = get_unique(df['categories'])
    
    # create a new column for each category, with 1s indicating membership and 0s for non-members
    for col in sorted(cat_cols):
        col_name = re.sub(r'[\s\-\/]', '_', col.lower())
        col_name = re.sub(r'[()]', '', col_name)
        
        df[col_name] = df['categories'].apply(lambda x: 1 if col in x.split(';') else 0)
        
    # repeat for genre column names (get_unique used to find unique genre names, 
    # not necessary but useful if keeping all of them)
    gen_cols = get_unique(df['genres'])  
    gen_col_names = []
    
    # create new columns for each genre with 1s for games of that genre
    for col in sorted(gen_cols):
        col_name = col.lower().replace('&', 'and').replace(' ', '_')
        gen_col_names.append(col_name)
        
        df[col_name] = df['genres'].apply(lambda x: 1 if col in x.split(';') else 0)
        # alternate method using np.where:
        # df[col_name] = np.where(df['genres'].str.contains(col), 1, 0)
    
    # not using steamspy tags for now, as mostly overlap with genres
    # here's one way we could deal with them:
    tag_cols = get_unique(df['steamspy_tags'])
    df['top_tag'] = df['steamspy_tags'].apply(lambda x: x.split(';')[0])
    
    # remove redundant columns and return dataframe (keeping genres column for reference)
    df = df.drop(['categories', 'steamspy_tags','platforms'], axis=1)
    
    return df

def calc_rating(row):
    """Calculate rating score based on SteamDB method."""
    import math

    pos = row['positive_ratings']
    neg = row['negative_ratings']

    total_reviews = pos + neg
    average = pos / total_reviews
    
    # pulls score towards 50, pulls more strongly for games with few reviews
    score = average - (average*0.5) * 2**(-math.log10(total_reviews + 1))

    return score * 100

def handleMultipleItemColumn(df,column,sep):
    df[column] = df[column].apply(lambda x: x.split(sep))


def pre_process(df):
    """Preprocess Steam dataset for exploratory analysis."""
    #df = pd.read_csv(filepath_or_buffer = 'datasets/steam/steam.csv',sep=',', decimal = ".")
    
    # keep lower and higher bound of owners column, as integer
    df['owners_low_bound'] = df['owners'].str.split('-').apply(lambda x: x[0]).astype(int)
    df['owners_high_bound'] = df['owners'].str.split('-').apply(lambda x: x[1]).astype(int)
    del df['owners']
    
    # calculate rating, as well as simple ratio for comparison
    df['total_ratings'] = df['positive_ratings'] + df['negative_ratings']
    df['rating_ratio'] = df['positive_ratings'] / df['total_ratings']
    df['rating'] = df.apply(calc_rating, axis=1)
    
    # convert release_date to datetime type and create separate column for release_year
    df['release_date'] = df['release_date'].astype('datetime64[ns]')
    df['release_year'] = df['release_date'].apply(lambda x: x.year)
    
    # process genres, categories and steamspy_tag columns
    #df = process_cat_gen_tag(df)
    handleMultipleItemColumn(df,'platforms',';')
    handleMultipleItemColumn(df,'categories',';')
    df['top_tag'] = df['steamspy_tags'].apply(lambda x: x.split(';')[0])
    handleMultipleItemColumn(df,'steamspy_tags',';')
    handleMultipleItemColumn(df,'developer',';')
    handleMultipleItemColumn(df,'publisher',';')
    
    # Create a column to split free vs paid games
    df['type'] = 'Free'
    df.loc[df['price'] > 0, 'type'] = 'Paid'
    
    # Add Value total playtime
    df['total_playtime'] = df.apply (lambda row: row.average_playtime*row.owners_low_bound, axis=1)

    # Add Value total playtime
    df['estimated_revenue'] = df.apply (lambda row: row.price*row.owners_low_bound, axis=1)

    return df

def topDataset(percent,df):
    numberOfTopGames = math.ceil(len(df.index) * percent / 100 )
    print("total number",len(df.index))
    print("top",percent,"%",numberOfTopGames)
    return df.sort_values(by='owners_low_bound',ascending=False).head(numberOfTopGames)