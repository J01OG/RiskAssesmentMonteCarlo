import streamlit as st
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Set page title and icon
st.set_page_config(page_title="Stock Price Simulation", page_icon=":chart_with_upwards_trend:")
def main():
    # Title and description
    st.title("Stock Price Simulation")
    st.write("This app simulates future stock price paths using Monte Carlo simulation.")

    companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]  # Add more symbols as needed

    selected_company = st.selectbox("Select a company", companies)
    max_start_date = datetime.date(2022, 1, 22)
    start_date = st.date_input("Starting Date", value=datetime.date(2000, 1, 1), max_value=max_start_date)
    end_date_first_graph = datetime.date(2023, 1, 22)

    # Fetch stock data for the first graph
    stock_data = yf.download(selected_company, start=start_date, end=end_date_first_graph)
    specific_start_date = datetime.datetime(2023, 1, 20)
    specific_end_date = datetime.datetime(2024, 1, 20)
    # Calculate daily returns
    stock_data['Daily_Returns'] = stock_data['Adj Close'].pct_change()

    # Mean and standard deviation of daily returns
    mu = stock_data['Daily_Returns'].mean()
    sigma = stock_data['Daily_Returns'].std()

    # Number of simulations
    num_simulations = st.slider("Number of Simulations", min_value=100, max_value=2000, value=1000, step=100)

    # Generate random normal values for each day in the simulation period
    num_days = 251
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
    ax.legend(loc='upper right')  # Adjust legend position

    # Annotate plot with input details
    ax.text(0.02, 0.95, f"Selected Company: {selected_company}", transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.90, f"Start Date: {start_date}", transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.85, f"End Date: {end_date_first_graph}", transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.80, f"Number of Simulations: {num_simulations}", transform=ax.transAxes, verticalalignment='top')

    st.pyplot(fig)

    # Fetch stock data for specific time period
    specific_stock_data = yf.download(selected_company, start=specific_start_date, end=specific_end_date)

    # Plot stock prices for the specific time period
    st.write("## Stock Prices from January 20, 2023, to January 20, 2024")
    fig_specific, ax_specific = plt.subplots(figsize=(10, 6))
    ax_specific.plot(specific_stock_data['Adj Close'], color='blue')
    ax_specific.set_title(f'Stock Prices for {selected_company} (Jan 20, 2023 - Jan 20, 2024)')
    ax_specific.set_xlabel('Date')
    ax_specific.set_ylabel('Price')

    st.pyplot(fig_specific)
    fig, ax = plt.subplots(figsize=(10, 6))
    for i in range(num_simulations):
        color = np.random.rand(3,)  # Random color
        ax.plot(simulated_price_paths[:, i], color=color, alpha=0.1)
    ax.plot(simulated_price_paths.mean(axis=1), color='blue', label='Mean')
    ax.plot(simulated_price_paths.max(axis=1), color='green', linestyle='--', label='Max')
    ax.plot(simulated_price_paths.min(axis=1), color='red', linestyle='--', label='Min')
    
    specific_stock_data.reset_index(drop=True, inplace=True)
    specific_stock_data.index = specific_stock_data.index + 1
    ax.fill_between(range(num_days), np.percentile(simulated_price_paths, 10, axis=1),np.percentile(simulated_price_paths, 90, axis=1), color='yellow', alpha=0.3, label='10-90 Percentile')
    ax.set_title(f'Monte Carlo Simulation of Stock Prices for {selected_company}')
    ax.set_xlabel('Days')
    ax.set_ylabel('Price')
    ax.legend(loc='upper right')  # Adjust legend position

    # Annotate plot with input details
    ax.text(0.02, 0.95, f"Selected Company: {selected_company}", transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.90, f"Start Date: {start_date}", transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.85, f"End Date: {end_date_first_graph}", transform=ax.transAxes, verticalalignment='top')
    ax.text(0.02, 0.80, f"Number of Simulations: {num_simulations}", transform=ax.transAxes, verticalalignment='top')
    ax.plot(specific_stock_data['Adj Close'], color='purple', label='Specific Period')

    # Fetch stock data for specific time period


    st.pyplot(fig)





    

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
    
    # Select Company
    selected_company = "AAPL"  # Example selection, can be dynamic based on user input
    
    # Choose starting date and duration
    start_date = "2020-01-01"  # Example starting date, can be dynamic based on user input
    end_date = "2023-01-01"  # Example end date, can be dynamic based on user input
    
    # Fetch stock data
    stock_data = yf.download(selected_company, start=start_date, end=end_date)
    
    # Calculate daily returns
    stock_data['Daily_Returns'] = stock_data['Adj Close'].pct_change()
    
    # Mean and standard deviation of daily returns
    mu = stock_data['Daily_Returns'].mean()
    sigma = stock_data['Daily_Returns'].std()
    
    # Number of simulations
    num_simulations = 1000  # Example value, can be dynamic based on user input
    
    # Generate random normal values for each day in the simulation period
    num_days = (end_date - start_date).days + 1
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

# View .docx File Page
# View .docx File Page
def view_docx():

    # Define the URL
    external_url = "https://in.docworkspace.com/d/sILLDxN3eAbHl2bAG"

    # Display a message with a clickable link
    st.write("[PROJECT REPORT](" + external_url + ")")



# Sidebar navigation
pages = {
    "Stock Price Simulation": main,
    "Code Explanation": code_explanation,
    "Links": view_docx,
}

# Sidebar
st.sidebar.title("Pages:")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page
if selection in pages:
    pages[selection]()
