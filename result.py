import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Fetch the required data
cursor.execute('SELECT age, rating, helpful, diverse, usage, gender FROM main_recommendationrating')
rows = cursor.fetchall()

# Initialize variables
ages = []
ratings = []
helpfuls = []
diverses = []
usage_yes_count = 0
female = 0
male = 0

# Process each row
for row in rows:
    age, rating, helpful, diverse, usage, gender = row
    ages.append(age)
    ratings.append(rating)
    helpfuls.append(helpful)
    diverses.append(diverse)
    if usage.lower() == 'yes':
        usage_yes_count += 1
    if gender.lower() == 'female':
        female += 1
    if gender.lower() == 'male':
        male += 1

# Calculate means
mean_age = sum(ages) / len(ages)
mean_rating = sum(ratings) / len(ratings)
mean_helpful = sum(helpfuls) / len(helpfuls)
mean_diverse = sum(diverses) / len(diverses)

# Calculate percentage of 'yes' answers for usage
total_count = len(rows)
usage_yes_percentage = (usage_yes_count / total_count) * 100
female_percentage = (female / total_count) * 100
male_percentage = (male / total_count) * 100

# Output results
print(f"Mean Age: {mean_age:.2f}")
print(f"Mean Rating: {mean_rating:.2f}")
print(f"Mean Helpful: {mean_helpful:.2f}")
print(f"Mean Diverse: {mean_diverse:.2f}")
print(f"Percentage of 'Yes' for Usage: {usage_yes_percentage:.2f}%")
print(f"Number of Female Participants: {female_percentage:.2f}%")
print(f"Number of Male Participants: {male_percentage:.2f}%")

# Close the connection
conn.close()
