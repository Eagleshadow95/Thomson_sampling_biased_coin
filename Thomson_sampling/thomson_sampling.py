# -*- coding: utf-8 -*-
"""thomson_sampling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mo33voTi5E0T9DHD4zn33pMJReAyX8uL
"""
from flip_multiple_coins import Coins
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

class ThompsonSampling:
    """
    A class to perform Thompson Sampling for selecting among multiple biased coins (arms) in a multi-armed bandit problem.

    Attributes:
    -----------
    coins : list of Coins
        A list of Coins objects, each representing a biased coin with a different probability of landing heads.
    alpha : list of int
        The alpha parameters (successes + 1) for the Beta distribution used in Thompson Sampling, initialized to 1.
    beta : list of int
        The beta parameters (failures + 1) for the Beta distribution used in Thompson Sampling, initialized to 1.
    rewards : list of int
        A list to store the results (rewards) of each coin flip during the simulation.

    Methods:
    --------
    select_coin():
        Uses Thompson Sampling to select which coin to flip next by sampling from the Beta distribution.
    update(coin_index, result):
        Updates the alpha and beta parameters based on the result of the coin flip.
    run_simulation(num_rounds, moving_avg_window, plot_interval):
        Runs the Thompson Sampling simulation for a specified number of rounds and calculates the moving average of the rewards.
        Periodically plots the Beta distributions for each coin.
    """

    def __init__(self, coin_probs):
        self.coins = [Coins(p) for p in coin_probs]  # Initialize Coins objects with given probabilities
        self.alpha = [1] * len(coin_probs)           # Initialize alpha parameters for Beta distribution
        self.beta = [1] * len(coin_probs)            # Initialize beta parameters for Beta distribution
        self.rewards = []                            # List to store the results of each coin flip

    def select_coin(self):
        # Sample theta values from the Beta distribution for each coin and select the coin with the highest sampled theta
        sampled_theta = [beta(a, b).rvs() for a, b in zip(self.alpha, self.beta)]
        return np.argmax(sampled_theta)   # Returns the index of the maximum value

    def update(self, coin_index, result):
        # Update the alpha and beta parameters based on the result of the coin flip
        self.alpha[coin_index] += result             # Increment alpha if heads (success)
        self.beta[coin_index] += (1 - result)        # Increment beta if tails (failure)

    def plot_beta_distributions(self, round_num):
        x = np.linspace(0, 1, 100)
        plt.figure(figsize=(12, 6))
        for i, (a, b) in enumerate(zip(self.alpha, self.beta)):
            y = beta(a, b).pdf(x)
            plt.plot(x, y, label=f'Coin {i+1} (α={a}, β={b})')
        plt.title(f'Beta Distributions at Round {round_num}')
        plt.xlabel('Probability of Heads')
        plt.ylabel('Density')
        plt.legend()
        plt.show()

    def run_simulation(self, num_rounds, moving_avg_window, plot_interval):
        results = []                                 # List to store the results of each round (selected coin and result)
        moving_averages = []                         # List to store the moving average of the rewards

        for i in range(num_rounds):
            selected_coin = self.select_coin()       # Select a coin to flip using Thompson Sampling
            result = self.coins[selected_coin].getting_heads()  # Get the result of the coin flip (1 for heads, 0 for tails)
            self.update(selected_coin, result)       # Update the alpha and beta parameters based on the result
            self.rewards.append(result)              # Store the result (reward)

            # Calculate the moving average of the reward if enough rounds have been completed
            if i + 1 >= moving_avg_window:
                moving_avg = np.mean(self.rewards[-moving_avg_window:])
                moving_averages.append(moving_avg)

            results.append((selected_coin, result))  # Store the selected coin and the result for this round

            # Plot the Beta distributions at specified intervals
            if (i + 1) % plot_interval == 0:
                self.plot_beta_distributions(i + 1)

        return results, moving_averages              # Return the results and the moving averages