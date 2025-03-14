import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('players_data.csv')

# Convert time to datetime
data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S').dt.hour

# Define day and night
data['period'] = data['time'].apply(lambda x: 'Day' if 6 <= x < 18 else 'Night')

# Group by period and calculate mean score
period_scores = data.groupby('period')['score'].mean()

# Plot
plt.figure(figsize=(10, 5))
period_scores.plot(kind='bar', color=['skyblue', 'orange'])
plt.title('Average Scores by Day and Night')
plt.xlabel('Period')
plt.ylabel('Average Score')
plt.show()

# Conclusion
print("Conclusion: The graph shows the average scores achieved during the day and night. This helps determine if players perform better during specific times of the day.")

import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('players_data.csv')

# Filter data for two players
player1_data = data[data['player_id'] == 1]
player2_data = data[data['player_id'] == 2]

# Calculate mean scores
player1_mean_score = player1_data['score'].mean()
player2_mean_score = player2_data['score'].mean()

# Plot
plt.figure(figsize=(10, 5))
plt.bar(['Player 1', 'Player 2'], [player1_mean_score, player2_mean_score], color=['blue', 'green'])
plt.title('Comparison of Achievements Between Two Players')
plt.xlabel('Player')
plt.ylabel('Average Score')
plt.show()

# Conclusion
print("Conclusion: The graph compares the average scores of two players, providing insights into their relative performance.")


import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('players_data.csv')

# Filter data for a specific player
player_data = data[data['player_id'] == 1].copy()

# Extract hour from time
player_data.loc[:, 'hour'] = pd.to_datetime(player_data['time'], format='%H:%M:%S').dt.hour

# Count occurrences of each hour
hour_counts = player_data['hour'].value_counts().sort_index()

# Plot
plt.figure(figsize=(10, 5))
hour_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Playing Hours Distribution for Player 1')
plt.ylabel('')
plt.show()

# Conclusion
print("Conclusion: The pie chart shows the distribution of playing hours for a specific player, indicating their most active times.")

import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('players_data.csv')

# Filter data for a specific player
player_data = data[data['player_id'] == 1].copy()

# Convert date to datetime
player_data.loc[:, 'date'] = pd.to_datetime(player_data['date'])

# Group by date and calculate mean score
daily_scores = player_data.groupby('date')['score'].mean()

# Plot
plt.figure(figsize=(10, 5))
daily_scores.plot(kind='line', marker='o')
plt.title('Player 1 Performance Over Time')
plt.xlabel('Date')
plt.ylabel('Average Score')
plt.grid(True)
plt.show()

# Conclusion
print("Conclusion: The line graph shows the performance of a specific player over time, highlighting trends and patterns in their scores.")