# DEPI_Data_Analytics_Python_Project2

Absolutely! Here's a README file with emojis for your Python script analyzing the TMDB movie data::

**TMDB Movie Analysis**

This Python script explores the fascinating world of movies using the TMDB dataset! We'll delve into aspects like profitability, revenue, budget allocation, and more to uncover interesting insights.  ✨

**Libraries Used:**

* pandas  - Powerful data manipulation library 
* matplotlib  - Essential for creating visualizations 
* seaborn   - Seaborn enhances matplotlib for beautiful plots 

**Script Breakdown:**

1. **Data Loading and Cleaning**
   - We'll load the TMDB movie data from a CSV file (`tmdb-movies.csv`). 
   - We'll filter out movies with missing values in crucial columns (`budget`, `revenue`, etc.) to ensure data quality.  ️
   - Data preprocessing steps include converting numeric columns to numeric data types and filling missing values in text columns with "Not Found". 

2. **Profitability Analysis**
   - We'll calculate the profit for each movie by subtracting the budget from the revenue. 
   - A comprehensive dashboard will be created using seaborn to visualize:
     - **Most Profitable Genres:** Discover which genres generate the highest average profit.  
     - **Profitability by Release Year:** Explore how profitability trends over release years.  
     - **Top Genre Distribution:** See the distribution of total profit among the top 5 genres.  
     - **Most Profitable Directors:** Identify directors who consistently deliver high-profit movies.  

3. **Revenue Analysis**
   - We'll uncover insights related to movie revenue:
     - **Top Grossing Movies:** Find out which movies brought in the most revenue.  
     - **Budget vs. Revenue Correlation:** Explore the correlation between a movie's budget and its revenue.  ⚖️
     - **Impact of Rating on Revenue:** Investigate how movie rating (vote_average) affects revenue.  ⭐
     - **Revenue Trend Over Years:** Analyze the overall revenue trend across different release years.  

4. **Budget Allocation Analysis**
   - We'll delve into how budgets are allocated:
     - **Budget Distribution:** Visualize the distribution of budgets across movies. ‍ (This emoji might not be the best fit, but it conveys the idea of spread)
     - **Genre vs. Average Budget:** Identify genres with the highest average budgets.  
     - **Budget vs. Critical Acclaim:** Investigate the relationship between budget and critical acclaim (vote_average).  ⚖️
     - **Optimal Budget Range:** Explore the budget range that might maximize revenue.  

