import plotly.graph_objects as go
from thomson_sampling import ThompsonSampling
from datetime import datetime


if __name__ == '__main__':
    coin_probs = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    thompson = ThompsonSampling(coin_probs)

    num_rounds = 2000
    moving_avg_window = 100
    plot_interval = 500
    results, moving_averages = thompson.run_simulation(num_rounds, moving_avg_window, plot_interval)

    # Count the number of times each coin was selected
    selection_counts = [0] * len(coin_probs)
    for coin_index, result in results:
        selection_counts[coin_index] += 1

    # Print the results
    for i, coin in enumerate(thompson.coins):
        print(f"Coin {i+1} (p={coin_probs[i]}) - Number of trials: {coin.n}, Sum of heads: {coin.sum_heads}")
        print(f"Alpha: {thompson.alpha[i]}, Beta: {thompson.beta[i]}")
        print(f"Selection count: {selection_counts[i]}")

    # Plot the moving average of the reward using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(moving_avg_window, num_rounds + 1)),
        y=moving_averages,
        mode='lines',
        name='Moving Average Reward'
    ))

    fig.update_layout(
        title='Moving Average of Reward Over Time',
        xaxis_title='Round',
        yaxis_title='Moving Average Reward',
        showlegend=True,
    )
    # Save the plot with a unique name
    unique_filename = f"moving_average_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    fig.write_image(unique_filename)

    # Show the plot
    fig.show()

    print(f"Plot saved as {unique_filename}")