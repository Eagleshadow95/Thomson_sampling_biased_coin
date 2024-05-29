# -*- coding: utf-8 -*-
"""flip_multiple_coins.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1A0M0Y8m3UdPxgcxJZcoUUN5P13PDVIi_
"""

import numpy as np

class Coins:
    """
    A class to simulate flipping an unfair coin using a binomial distribution.

    Attributes:
    -----------
    p : float
        The probability of getting heads in a single coin flip. Assumes an unfair coin.
    n : int
        A counter to keep track of the number of times the getting_heads method has been called.
    sum_heads : int
        A cumulative sum of the heads obtained from the getting_heads method.

    Methods:
    --------
    getting_heads():
        Simulates a single flip of the unfair coin and updates the counter and cumulative sum.
    """
    def __init__(self, p):
        self.p = p
        self.n = 0
        self.sum_heads = 0

    def getting_heads(self):
        s = np.random.binomial(1, self.p)
        self.n += 1
        self.sum_heads += s
        return s

    @staticmethod
    def test_coin_simulation(p,n):
        # Create coins with different probabilities p
        coin = Coins(p)  # Biased coin towards heads

        # Simulate getting heads n times for each coin
        for _ in range(n):
            coin.getting_heads()

        # Print the number of trials and the sum of heads for each coin
        print("Number of trials for coin:", coin.n)
        print("Sum of heads for coin:", coin.sum_heads)

    @staticmethod
    def run_simulations(coin_probs=None, num_simulations=1000):
      if coin_probs is None:
        coin_probs = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

      for p in coin_probs:
        print(f"Simulation for coin with success probability {p}")
        Coins.test_coin_simulation(p, num_simulations)
        print("Simulation end\n")


if __name__ == '__main__':
    Coins.run_simulations()