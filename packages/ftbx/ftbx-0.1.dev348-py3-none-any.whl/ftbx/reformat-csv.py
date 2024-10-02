import pandas as pd

# Sample DataFrame with 'created' column
df = pd.read_csv("combined_file.csv") 

# Convert 'created' column to datetime format and then to desired string format
df['created'] = pd.to_datetime(df['created'], format='%d %b %Y').dt.strftime('%Y-%m-%d')
df = df.sort_values(by='created')

# Print the updated DataFrame
print(df)
df.to_csv("add.csv")

