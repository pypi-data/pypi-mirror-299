import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Sample data (replace with your actual data)
data = {
    'Keyword1': ['apple', 'banana', 'apple', 'banana', 'cherry'],
    'Keyword2': ['red', 'yellow', 'green', 'yellow', 'red'],
    'Keyword3': ['sweet', 'tasty', 'sweet', 'tasty', 'sour']
}

df = pd.DataFrame(data)

# Count occurrences of each combination of keywords
keyword_counts = df.groupby(['Keyword1', 'Keyword2', 'Keyword3']).size().reset_index(name='Count')

# Create a 3D cube plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Extract axes data
x = keyword_counts['Keyword1']
y = keyword_counts['Keyword2']
z = keyword_counts['Keyword3']
counts = keyword_counts['Count']

# Convert categorical labels to numeric indices
x_unique = x.unique()
y_unique = y.unique()
z_unique = z.unique()
x_indices = [x_unique.tolist().index(val) for val in x]
y_indices = [y_unique.tolist().index(val) for val in y]
z_indices = [z_unique.tolist().index(val) for val in z]

# Normalize counts for color mapping
norm_counts = (counts - counts.min()) / (counts.max() - counts.min())

# Plot the cube with colored blocks
for xi, yi, zi, count in zip(x_indices, y_indices, z_indices, norm_counts):
    ax.bar3d(xi, yi, zi, dx=0.5, dy=0.5, dz=count, shade=True, cmap='coolwarm')

# Customize labels
ax.set_xticks(range(len(x_unique)))
ax.set_xticklabels(x_unique, rotation=45)
ax.set_yticks(range(len(y_unique)))
ax.set_yticklabels(y_unique, rotation=45)
ax.set_zticks(range(len(z_unique)))
ax.set_zticklabels(z_unique)

ax.set_xlabel('Keyword1')
ax.set_ylabel('Keyword2')
ax.set_zlabel('Keyword3')
ax.set_title('3D Cube Heatmap of Keyword Combinations (Color by Occurrences)')

# Show the plot
plt.show()
