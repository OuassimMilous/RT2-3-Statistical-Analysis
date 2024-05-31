import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats

# Execution times data

# collegue's data
collegues_data = [
    39.17593717575073, 35.67468976974487, 47.991981983184814, 37.851794481277466,
    47.25392508506775, 37.184141635894775, 39.37392497062683, 59.74052977561951,
    39.738651275634766, 37.18262791633606, 41.81641340255737, 33.480597734451294,
    51.30228519439697, 42.94026231765747, 44.47332048416138, 39.913494348526,
    50.38465619087219, 49.49549412727356, 48.684606075286865, 39.47776746749878,
    48.667150259017944, 47.27253079414368, 40.27370882034302, 44.91829180717468,
    40.93896961212158, 46.674877405166626, 34.41720652580261, 45.45862793922424,
    44.71782922744751, 43.4380521774292, 47.4894483089447, 45.998939752578735,
    42.18389630317688, 40.76705265045166, 43.237879037857056, 41.98980379104614,
    39.369401693344116, 53.61984872817993, 43.21582889556885, 44.08116388320923,
    43.10384225845337, 47.55291128158569, 43.69208264350891, 51.42169117927551,
    47.52693295478821, 46.18242621421814, 47.771875858306885, 47.632659673690796,
    44.91829180717468, 39.47776746749878
]

# my data
mine = [
    48.13187289237976, 128.55767393112183, 52.73160648345947, 49.56117129325867,
    47.65165567398071, 45.95206665992737, 49.05328416824341, 34.532639026641846,
    46.23897361755371, 39.87034296989441, 42.61948275566101, 40.004302740097046,
    34.87387037277222, 54.4050714969635, 49.826955795288086, 52.18607521057129,
    62.33963871002197, 51.85245394706726, 45.34819412231445, 59.50053095817566,
    45.60940980911255, 37.43087601661682, 38.43876266479492, 53.158101320266724,
    43.89826250076294, 29.116892099380493, 46.10402297973633, 130.74855208396912,
    41.37489700317383, 48.44751977920532, 42.99095940589905, 44.416335582733154,
    43.84186100959778, 42.38340473175049, 50.54225206375122, 43.96574068069458,
    55.473950147628784, 52.764405488967896, 58.51520133018494, 50.264798402786255,
    43.79601788520813, 42.11333775520325, 43.78447341918945, 56.08797025680542,
    58.40659785270691, 49.24154782295227, 46.13136649131775, 46.54616951942444,
    63.27558660507202, 46.53680920600891
]

# Convert data to a NumPy array
execution_times1 = np.array(collegues_data)
execution_times2 = np.array(mine)

# Create a histogram for collegue's data
plt.figure(figsize=(10, 6))
plt.hist(execution_times1, bins=20, color='blue', edgecolor='black', alpha=0.7, label='collegue')
plt.title('Histogram of Execution Times')
plt.xlabel('Execution Time (seconds)')
plt.ylabel('Frequency')
plt.grid(True)
plt.legend()
plt.show()

# Create a Q-Q plot for collegue's data
plt.figure(figsize=(10, 6))
stats.probplot(execution_times1, dist="norm", plot=plt)
plt.title('Q-Q Plot of Execution Times (collegue)')
plt.grid(True)
plt.show()

# Perform the Shapiro-Wilk test for collegue's data
shapiro_test1 = stats.shapiro(execution_times1)
print("collegue's Data:")
print(f"Shapiro-Wilk test statistic: {shapiro_test1.statistic}, p-value: {shapiro_test1.pvalue}")
print()

# Create a histogram for my data
plt.figure(figsize=(10, 6))
plt.hist(execution_times2, bins=20, color='red', edgecolor='black', alpha=0.7, label='mine')
plt.title('Histogram of Execution Times')
plt.xlabel('Execution Time (seconds)')
plt.ylabel('Frequency')
plt.grid(True)
plt.legend()
plt.show()

# Create a Q-Q plot for my data
plt.figure(figsize=(10, 6))
stats.probplot(execution_times2, dist="norm", plot=plt)
plt.title('Q-Q Plot of Execution Times (mine)')
plt.grid(True)
plt.show()

# Perform the Shapiro-Wilk test for my data
shapiro_test2 = stats.shapiro(execution_times2)
print("My Data:")
print(f"Shapiro-Wilk test statistic: {shapiro_test2.statistic}, p-value: {shapiro_test2.pvalue}")
