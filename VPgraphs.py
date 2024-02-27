

import matplotlib.pyplot as plt
import numpy as np
import random

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
inc = []

for i in range(6):
    n = int(input("Enter your income: "))
    inc.append(n)

plt.plot(days, inc, marker="o")
plt.legend(["income"], loc=2)
plt.grid(color="grey", linewidth=1)
plt.xlabel("Days")
plt.ylabel("Income")
plt.title("Weekly Business Analysis")

# success boundary be 5000
total_income = sum(inc)
average_income = total_income / 6

if average_income >= 5000:
    profit = int(average_income - 5000)
    profit_message = f"You have a profit of {profit} rupees.\nKeep it up!"
    plt.text(0.5, 0.9, profit_message, transform=plt.gca().transAxes, fontsize=10, va='center', ha='center', bbox=dict(facecolor='green', alpha=0.5))
else:
    loss = int(5000 - average_income)
    loss_message = f"You have a loss of {loss} rupees.\nConsider these suggestions\n1.Review and analyze all expenses to identify where costs can be reduced without compromising quality.\n2.Implement innovative solutions to stay competitive in the market."
    plt.text(0.5, 0.9, loss_message, transform=plt.gca().transAxes, fontsize=10, va='center', ha='center', bbox=dict(facecolor='red', alpha=0.5))

plt.show()