import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Execution times data
execution_times2 = [
    39.17593717575073, 35.67468976974487, 47.991981983184814, 37.851794481277466, 47.25392508506775, 
    37.184141635894775, 39.37392497062683, 59.74052977561951, 39.738651275634766, 37.18262791633606, 
    41.81641340255737, 33.480597734451294, 51.30228519439697, 42.94026231765747, 44.47332048416138, 
    39.913494348526, 50.38465619087219, 49.49549412727356, 48.684606075286865, 39.47776746749878, 
    48.667150259017944, 47.27253079414368, 40.27370882034302, 44.91829180717468, 40.93896961212158, 
    46.674877405166626, 34.41720652580261, 45.45862793922424, 44.71782922744751, 43.4380521774292, 
    47.4894483089447, 45.998939752578735, 42.18389630317688, 40.76705265045166, 43.237879037857056, 
    41.98980379104614, 39.369401693344116, 53.61984872817993, 43.21582889556885, 44.08116388320923, 
    43.10384225845337, 47.55291128158569, 43.69208264350891, 51.42169117927551, 47.52693295478821, 
    46.18242621421814, 47.771875858306885, 47.632659673690796
]

# Create a DataFrame
execution_numbers = np.arange(1, len(execution_times2) + 1)
df = pd.DataFrame({
    'Execution Number': execution_numbers,
    'Execution Time': execution_times2,
    'Success': [True] * len(execution_times2)
})

# Save the DataFrame as a CSV file
df.to_csv('attempts_data_table.csv', index=False)

# Plotting the bar graph
plt.figure(figsize=(10, 6))
plt.bar(df['Execution Number'], df['Execution Time'], color='blue')
plt.title('Execution Times')
plt.xlabel('Execution #')
plt.ylabel('Time (seconds)')
plt.xticks(ticks=range(1, 50), rotation=90)  # Set x-ticks from 1 to 49
plt.ylim(0, 70)  # Set y-axis range from 0 to 70
plt.grid(True, axis='y')

# Save the plot as a PNG file
plt.savefig('execution_times_bar_graph.png', bbox_inches='tight')

# Show the plot
plt.show()

print("Data has been saved to 'attempts_data_table.csv' and 'execution_times_bar_graph.png'")

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# # Data provided
# execution_times = np.array([
#     39.17593717575073, 35.67468976974487, 47.991981983184814, 37.851794481277466, 47.25392508506775, 
#     37.184141635894775, 39.37392497062683, 59.74052977561951, 39.738651275634766, 37.18262791633606, 
#     41.81641340255737, 33.480597734451294, 51.30228519439697, 42.94026231765747, 44.47332048416138, 
#     39.913494348526, 50.38465619087219, 49.49549412727356, 48.684606075286865, 39.47776746749878, 
#     48.667150259017944, 47.27253079414368, 40.27370882034302, 44.91829180717468, 40.93896961212158, 
#     46.674877405166626, 34.41720652580261, 45.45862793922424, 44.71782922744751, 43.4380521774292, 
#     47.4894483089447, 45.998939752578735, 42.18389630317688, 40.76705265045166, 43.237879037857056, 
#     41.98980379104614, 39.369401693344116, 53.61984872817993, 43.21582889556885, 44.08116388320923, 
#     43.10384225845337, 47.55291128158569, 43.69208264350891, 51.42169117927551, 47.52693295478821, 
#     46.18242621421814, 47.771875858306885, 47.632659673690796
# ])

# # Create an execution number column
# execution_numbers = np.arange(1, len(execution_times) + 1)

# # Create a success column with all values set to True
# success = np.full(len(execution_times), True)

# # Creating a DataFrame
# df = pd.DataFrame({
#     'Execution Number': execution_numbers,
#     'Execution Time': execution_times,
#     'Success': success
# })

# # Saving the DataFrame to a CSV file
# df.to_csv('attempts_data_table.csv', index=False)

# # Plotting the DataFrame as a table
# fig, ax = plt.subplots(figsize=(6, 6))  # Set the size of the figure
# ax.axis('tight')
# ax.axis('off')
# table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

# # Save the table as a PNG file
# plt.savefig('attempts_data_table.png', bbox_inches='tight')

# print("Data has been saved to 'attempts_data_table.csv' and 'attempts_data_table.png'")

