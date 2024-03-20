from function import cal_function as f
f.history()

import matplotlib.pyplot as plt

# # Sample data: incremental growth values over time
# time_periods = [1, 2, 3, 4, 5]  # Time periods
# data = [100, 50, 50, -5, 50]  # Incremental growth values at each time period

# # Calculate cumulative growth values
# processed_data = [sum(data[:i+1]) for i in range(len(data))]

# # Plotting the cumulative growth over time
# plt.plot(time_periods, processed_data, marker='o', linestyle='-')

# # Filling the area below the line with a color
# plt.fill_between(time_periods, processed_data, color='skyblue', alpha=0.4)

# # Adding labels and title
# plt.xlabel('Time Period')
# plt.ylabel('Cumulative Growth')
# plt.title('Cumulative Growth Over Time')

# # Display the plot
# plt.grid(True)
# plt.show()
