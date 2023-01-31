import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import config
import database

db = database.db

# Get the current date and the date five days ago
now = datetime.now()
five_days_ago = now - timedelta(days=5)

# Initialize a dictionary to store the number of articles per day and per category
data = {day.strftime("%Y-%m-%d"): {category: 0 for category in config.keywords} for day in (five_days_ago + timedelta(n) for n in range(6))}

print(data)

# Loop through all the collections
for keyword in config.keywords:
    collection = db[keyword]
    # Find all the articles in the collection that were published in the last 5 days
    articles = collection.find({"publishedAt": {"$gte": five_days_ago}})
    # Loop through all the articles and increment the count for the corresponding day and category
    for article in articles:
        day = article["publishedAt"].strftime("%Y-%m-%d")
        data[day][keyword] += 1

# Get the dates and the categories for the x and y axis respectively
dates = list(data.keys())

# Create the stacked bar plot
fig, ax = plt.subplots()
ax.set_ylabel('Date')
ax.set_xlabel('Amount')
ax.set_title('Articles Published per Day and per Category')

# Create the bars for each category
bars = []
for i, keyword in enumerate(config.keywords):
    bar = ax.barh(dates, [data[date][keyword] for date in dates], left=[sum(data[date][c] for c in config.keywords[:i]) for date in dates], label=keyword)
    bars.append(bar)

# Add the legend and show the plot
ax.legend()
plt.show()
