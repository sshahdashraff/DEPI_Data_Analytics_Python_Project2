import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import re
import seaborn as sns
sns.set(style="whitegrid")
plt.rcParams.update({'figure.max_open_warning': 0})

# Load the dataset
file_path = 'tmdb-movies.csv' 
data = pd.read_csv(file_path)

#print(data.head())
#print(data.info())

# Filter out movies with zero values in budget, revenue, budget_adj, or revenue_adj columns
columns_to_check = ['budget', 'revenue', 'budget_adj', 'revenue_adj']
mask = (data[columns_to_check] != 0).any(axis=1)
filtered_data = data[mask]

# Data Preprocessing
numeric_cols = ['budget', 'revenue', 'budget_adj', 'revenue_adj', 'vote_average', 'vote_count', 'release_year']
for col in numeric_cols:
    filtered_data[col] = pd.to_numeric(filtered_data[col], errors='coerce')

text_columns = ['homepage', 'tagline', 'keywords', 'production_companies']
for col in text_columns:
    filtered_data[col] = filtered_data[col].fillna('Not Found')


# Reset the index to ensure consistent indexing after filtering.
# Drop rows with missing values in key columns for analysis.
# Convert genre, cast, and production company strings into lists.
filtered_data.reset_index(drop=True, inplace=True)
filtered_data.dropna(subset=['revenue', 'release_year', 'genres', 'vote_average', 'vote_count'], inplace=True)
filtered_data['genres'] = filtered_data['genres'].apply(lambda x: x.split('|') if isinstance(x, str) else [])
filtered_data['cast'] = filtered_data['cast'].apply(lambda x: x.split('|') if isinstance(x, str) else [])
filtered_data['production_companies'] = filtered_data['production_companies'].apply(lambda x: x.split('|') if isinstance(x, str) else [])

# Apply the cleaning, splitting, and filling function to the 'director' column
def clean_and_split_directors(text):
    # Replace NaN with 'Unknown'
    if pd.isna(text):
        text = 'Unknown'
    else:
        try:
            #to decode the text from 'latin-1' then re-encode to 'utf-8'
            text = text.encode('latin-1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            text = re.sub(r'[^a-zA-Z0-9\s|]', '', text)
    
    # Remove any remaining special characters
    text = re.sub(r'[^a-zA-Z0-9\s|]', '', text)
    # Split by '|', if present
    return text.split('|')

filtered_data['director'] = filtered_data['director'].apply(clean_and_split_directors)


# for production_companies in data['production_companies']:
#     print(production_companies)

# print(filtered_data['cast'].iloc[2])
# print(filtered_data[['budget', 'revenue', 'budget_adj', 'revenue_adj']].iloc[74])

#FIRST DASHBOARD

# Set the color palette
sns.set_palette('bwr')

# Calculate profit globally
filtered_data['profit'] = filtered_data['revenue'] - filtered_data['budget']

# to make font bold globally
rcParams['font.weight'] = 'semibold'

# Create the figure and subplots for the FIRST DASHBOARD: Profitability Analysis
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Profitability Analysis', fontsize=17,fontstyle='italic',fontweight='bold',bbox=dict(facecolor='#e66771', edgecolor='black', boxstyle='square'))

# 1. Which genres are the most profitable?
genre_profit = filtered_data.explode('genres')
sns.barplot(ax=axs[0, 0], x=genre_profit.groupby('genres')['profit'].mean().index,
             y=genre_profit.groupby('genres')['profit'].mean().values, palette='bwr')
axs[0, 0].set_title('Which genres are the most profitable?', fontsize=14 ,fontweight='bold',bbox=dict(facecolor='#f4c2c2', edgecolor='black', boxstyle='round'))
axs[0, 0].set_xlabel('')
axs[0, 0].set_ylabel('Average Profit', fontsize=12,fontweight='bold')
axs[0, 0].tick_params(axis='x', rotation=45)

# 2. How does the release year impact profitability?
sns.lineplot(ax=axs[0, 1], x=filtered_data.groupby('release_year')['profit'].mean().index,
             y=filtered_data.groupby('release_year')['profit'].mean().values)
axs[0, 1].set_title('How does the release year impact profitability?', fontsize=14,fontweight='bold',bbox=dict(facecolor='#f4c2c2', edgecolor='black', boxstyle='round'))
axs[0, 1].set_xlabel('Release Year', fontsize=12,fontweight='bold')
axs[0, 1].set_ylabel('Average Profit', fontsize=12,fontweight='bold')

# 3. What is the distribution of total profit among the top 5 genres?
plt.subplots_adjust(left=None, bottom=0.2, right=None, top=None, wspace=None, hspace=None)
top_genres = genre_profit.groupby('genres')['profit'].sum().nlargest(5)
axs[1, 0].pie(top_genres, labels=top_genres.index, autopct='%1.1f%%', startangle=270, colors=sns.color_palette('bwr', n_colors=5))
axs[1, 0].set_title('What is the distribution of total profit among top 5 genres ?', fontsize=14,y=-0.1,fontweight='bold',bbox=dict(facecolor='#f4c2c2', edgecolor='black', boxstyle='round'))

# 4. Which directors produce the most profitable movies?
director_profit = filtered_data.explode('director')
sns.barplot(ax=axs[1, 1], y=director_profit.groupby('director')['profit'].mean().nlargest(10).index,
             x=director_profit.groupby('director')['profit'].mean().nlargest(10).values, palette='bwr', orient="h")
axs[1, 1].set_title('Which directors produce the most profitable movies?', fontsize=14,fontweight='bold',bbox=dict(facecolor='#f4c2c2', edgecolor='black', boxstyle='round'))
axs[1, 1].set_ylabel('')
axs[1, 1].set_xlabel('Average Profit', fontsize=12,fontweight='bold')
axs[1, 1].tick_params(axis='y', rotation=45)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

#SECOND DASHBOARD

# Set the color palette
sns.set_palette('rainbow')

# Create the figure and subplots for the SECOND DASHBOARD: Revenue Analysis
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Revenue Analysis',fontsize=17,fontstyle='italic',fontweight='bold',bbox=dict(facecolor='#4169e1', edgecolor='black', boxstyle='square'))

# 1. What are the top-grossing movies?
top_grossing = filtered_data.nlargest(10, 'revenue')
sns.barplot(ax=axs[0, 0], x=top_grossing['revenue'], y=top_grossing['original_title'], palette='rainbow', orient='h')
axs[0, 0].set_title('What are the top-grossing movies?', fontsize=14,fontweight='bold',bbox=dict(facecolor='#c5e384', edgecolor='black', boxstyle='round'))
axs[0, 0].set_xlabel('Revenue', fontsize=12,fontweight='bold')
axs[0, 0].set_ylabel('Movies', fontsize=12,fontweight='bold')
axs[0, 0].tick_params(axis='y', rotation=45)

# 2. How does the budget correlate with revenue?
sns.scatterplot(ax=axs[0, 1], x=filtered_data['budget'], y=filtered_data['revenue'], hue=filtered_data['revenue'],palette='rainbow')
axs[0, 1].set_title('How does the budget correlate with revenue?', fontsize=14,fontweight='bold',bbox=dict(facecolor='#c5e384', edgecolor='black', boxstyle='round'))
axs[0, 1].set_xlabel('Budget', fontsize=12,fontweight='bold')
axs[0, 1].set_ylabel('Revenue', fontsize=12,fontweight='bold')

# 3. How does movie rating (vote_average) impact revenue?
sns.scatterplot(ax=axs[1, 0], x=filtered_data['vote_average'], y=filtered_data['revenue'], hue=filtered_data['revenue'],palette='rainbow')
axs[1, 0].set_title('How does movie rating impact revenue?', fontsize=14,fontweight='bold',bbox=dict(facecolor='#c5e384', edgecolor='black', boxstyle='round'))
axs[1, 0].set_xlabel('Vote Average', fontsize=12,fontweight='bold')
axs[1, 0].set_ylabel('Revenue', fontsize=12,fontweight='bold')

# 4. What is the revenue trend over the years?
sns.lineplot(ax=axs[1, 1], x=filtered_data.groupby('release_year')['revenue'].sum().index,
             y=filtered_data.groupby('release_year')['revenue'].sum().values,color='#e03c31')
axs[1, 1].set_title('What is the revenue trend over the years?', fontsize=14,fontweight='bold',bbox=dict(facecolor='#c5e384', edgecolor='black', boxstyle='round'))
axs[1, 1].set_xlabel('Release Year', fontsize=12,fontweight='bold')
axs[1, 1].set_ylabel('Total Revenue', fontsize=12,fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

#THIRD DASHBOARD

# Set the color palette
sns.set_palette('YlGnBu')

# Create the figure and subplots for the #THIRD DASHBOARD: Budget Allocation
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Budget Allocation',fontsize=17,fontstyle='italic',fontweight='bold',bbox=dict(facecolor='#00ffff', edgecolor='black', boxstyle='square'))

# 1. What is the distribution of budgets among movies?
sns.histplot(ax=axs[0, 0], data=filtered_data, x='budget', bins=30, kde=True, color='#cc00ff')
axs[0, 0].set_title('What is the distribution of budgets among movies?', fontsize=14,fontweight='bold',bbox=dict(facecolor='#77b5fe', edgecolor='black', boxstyle='round'))
axs[0, 0].set_xlabel('Budget', fontsize=12,fontweight='bold')
axs[0, 0].set_ylabel('Frequency', fontsize=12,fontweight='bold')

# 2. Which genres have the highest average budgets?
genre_budget = filtered_data.explode('genres')
sns.barplot(ax=axs[0, 1], x=genre_budget.groupby('genres')['budget'].mean().index,
            y=genre_budget.groupby('genres')['budget'].mean().values, palette='cool')
axs[0, 1].set_title('Which genres have the highest average budgets?', fontsize=14,fontweight='bold',bbox=dict(facecolor='#77b5fe', edgecolor='black', boxstyle='round'))
axs[0, 1].set_xlabel('')
axs[0, 1].set_ylabel('Average Budget', fontsize=12,fontweight='bold')
axs[0, 1].tick_params(axis='x', rotation=45)

# 3. How does budget impact critical acclaim (vote_average)?
sns.scatterplot(ax=axs[1, 0], x=filtered_data['budget'], y=filtered_data['vote_average'], hue=filtered_data['budget'], palette='cool')
axs[1, 0].set_title('How does budget impact critical acclaim?', fontsize=14,fontweight='bold',bbox=dict(facecolor='#77b5fe', edgecolor='black', boxstyle='round'))
axs[1, 0].set_xlabel('Budget', fontsize=12,fontweight='bold')
axs[1, 0].set_ylabel('Vote Average', fontsize=12,fontweight='bold')

# 4. What is the optimal budget range for maximizing revenue?
sns.histplot(ax=axs[1, 1], data=filtered_data[filtered_data['revenue'] > 0], x='budget', bins=30, color='#cc00ff')
axs[1, 1].set_title('What is the optimal budget range for maximizing revenue?', fontsize=14,fontweight='bold',bbox=dict(facecolor='#77b5fe', edgecolor='black', boxstyle='round'))
axs[1, 1].set_xlabel('Budget', fontsize=12,fontweight='bold')
axs[1, 1].set_ylabel('Frequency of Successful Movies', fontsize=12,fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
