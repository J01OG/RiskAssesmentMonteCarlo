import streamlit as st
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Set page title and icon
st.set_page_config(page_title="Stock Price Simulation", page_icon=":chart_with_upwards_trend:")

# Main page - Stock Price Simulation
def main():
    # Title and description
    st.title("Stock Price Simulation")
    st.write("This app simulates future stock price paths using Monte Carlo simulation.")

    # Get list of available companies
    companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]  # Add more symbols as needed

    # Select company
    selected_company = st.selectbox("Select a company", companies)

    # Fetch stock data
    stock_data = yf.download(selected_company, start="2020-01-01", end="2023-01-01")  # Adjust date range as needed

    # Calculate daily returns
    stock_data['Daily_Returns'] = stock_data['Adj Close'].pct_change()

    # Mean and standard deviation of daily returns
    mu = stock_data['Daily_Returns'].mean()
    sigma = stock_data['Daily_Returns'].std()

    # Number of simulations
    num_simulations = st.slider("Number of Simulations", min_value=100, max_value=2000, value=1000, step=100)

    # Generate random normal values for each day in the simulation period
    num_days = 252  # Assuming 252 trading days in a year
    rand_returns = np.random.normal(mu, sigma, (num_days, num_simulations))

    # Add 1 to the random returns to get daily growth factor
    simulated_price_paths = np.cumprod(1 + rand_returns, axis=0) * stock_data.iloc[-1]['Adj Close']

    # Plot the simulated price paths
    st.write("## Simulated Price Paths")
    fig, ax = plt.subplots(figsize=(10, 6))
    for i in range(num_simulations):
        color = np.random.rand(3,)  # Random color
        ax.plot(simulated_price_paths[:, i], color=color, alpha=0.1)
    ax.plot(simulated_price_paths.mean(axis=1), color='blue', label='Mean')
    ax.plot(simulated_price_paths.max(axis=1), color='green', linestyle='--', label='Max')
    ax.plot(simulated_price_paths.min(axis=1), color='red', linestyle='--', label='Min')
    ax.fill_between(range(num_days), np.percentile(simulated_price_paths, 10, axis=1),
                    np.percentile(simulated_price_paths, 90, axis=1), color='yellow', alpha=0.3, label='10-90 Percentile')
    ax.set_title(f'Monte Carlo Simulation of Stock Prices for {selected_company}')
    ax.set_xlabel('Days')
    ax.set_ylabel('Price')
    ax.legend()
    st.pyplot(fig)

    # Footer
    st.markdown("---")
    st.write("Minor project by:")
    st.write("Ankit Prakash")
    st.write("Avanish Anand")
    st.write("Jayash Prem")
    st.write("Priya Sinha")
    st.write("Neha Bharti")
# Code Explanation Page
def code_explanation():
    st.title("Code Explanation")
    st.write("""
    Here's an explanation of the main code excluding the Streamlit-specific parts:
    
    ```python
    import yfinance as yf
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Get list of available companies
    companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]  # Add more symbols as needed
    
    # Select company
    selected_company = "AAPL"  # Example selection, can be dynamic based on user input
    
    # Fetch stock data
    stock_data = yf.download(selected_company, start="2020-01-01", end="2023-01-01")
    
    # Calculate daily returns
    stock_data['Daily_Returns'] = stock_data['Adj Close'].pct_change()
    
    # Mean and standard deviation of daily returns
    mu = stock_data['Daily_Returns'].mean()
    sigma = stock_data['Daily_Returns'].std()
    
    # Number of simulations
    num_simulations = 1000  # Example value, can be dynamic based on user input
    
    # Generate random normal values for each day in the simulation period
    num_days = 252  # Assuming 252 trading days in a year
    rand_returns = np.random.normal(mu, sigma, (num_days, num_simulations))
    
    # Add 1 to the random returns to get daily growth factor
    simulated_price_paths = np.cumprod(1 + rand_returns, axis=0) * stock_data.iloc[-1]['Adj Close']
    
    # Plot the simulated price paths
    fig, ax = plt.subplots(figsize=(10, 6))
    for i in range(num_simulations):
        ax.plot(simulated_price_paths[:, i], color='gray', alpha=0.1)
    ax.plot(simulated_price_paths.mean(axis=1), color='blue', label='Mean')
    ax.plot(simulated_price_paths.max(axis=1), color='green', linestyle='--', label='Max')
    ax.plot(simulated_price_paths.min(axis=1), color='red', linestyle='--', label='Min')
    ax.fill_between(range(num_days), np.percentile(simulated_price_paths, 10, axis=1),
                    np.percentile(simulated_price_paths, 90, axis=1), color='yellow', alpha=0.3, label='10-90 Percentile')
    ax.set_title('Monte Carlo Simulation of Stock Prices')
    ax.set_xlabel('Days')
    ax.set_ylabel('Price')
    ax.legend()
    plt.show()
    ```
    """)

# Sidebar navigation
pages = {
    "Stock Price Simulation": main,
    "Code Explanation": code_explanation
}

# Sidebar
st.sidebar.title("Pages:")
selection = st.sidebar.radio("Go to", list(pages.keys()))
    
# Display the selected page
if selection == "Stock Price Simulation":
    main()
elif selection == "Code Explanation":
    code_explanation()
