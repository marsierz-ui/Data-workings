import pandas as pd
import os
import matplotlib.pyplot as plt

def load_and_preprocess(filepath, date_col, marketcap_col, coin_name):
    """
    Loads a CSV, preprocesses it, and returns a clean DataFrame.
    - Selects specified date and marketcap columns
    - Converts 'Date' to datetime and normalizes it
    - Converts 'Marketcap' to numeric, coercing errors
    - Sets 'Date' as index
    """
    df = pd.read_csv(filepath)

    # Select and rename columns
    df = df[[date_col, marketcap_col]]
    df = df.rename(columns={date_col: 'Date', marketcap_col: f'Marketcap_{coin_name}'})

    # Clean data
    # Convert date column to datetime objects and then just keep the date part
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df[f'Marketcap_{coin_name}'] = pd.to_numeric(df[f'Marketcap_{coin_name}'], errors='coerce')
    df = df.dropna()

    # Set index
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')

    return df

def main():
    """
    Main function to load, process, and visualize gold-backed asset data.
    """
    # Define paths
    data_dir = 'data'
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # --- Configuration for each asset ---
    assets = {
        'KAU': {'file': 'kau-usd-max.csv', 'date_col': 'snapped_at', 'marketcap_col': 'market_cap'},
        'PAXG': {'file': 'paxg-usd-max.csv', 'date_col': 'date', 'marketcap_col': 'marketcap_usd'},
        'XAUT': {'file': 'xaut-usd-max.csv', 'date_col': 'timestamp', 'marketcap_col': 'market_cap'}
    }

    all_dfs = []
    for symbol, config in assets.items():
        filepath = os.path.join(data_dir, config['file'])
        df = load_and_preprocess(filepath, config['date_col'], config['marketcap_col'], symbol)
        all_dfs.append(df)

    # Merge the dataframes on the date index
    merged_df = pd.concat(all_dfs, axis=1, join='inner')

    # Calculate total market capitalization
    market_cap_cols = [f'Marketcap_{symbol}' for symbol in assets.keys()]
    merged_df['Total_Marketcap'] = merged_df[market_cap_cols].sum(axis=1)

    # --- Visualization ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(15, 8))

    # Plot individual market caps
    for symbol in assets.keys():
        ax.plot(merged_df.index, merged_df[f'Marketcap_{symbol}'], label=f'{symbol} Market Cap', alpha=0.7)

    # Plot total market cap
    ax.plot(merged_df.index, merged_df['Total_Marketcap'], label='Total Market Cap (All Assets)', color='black', linewidth=2, linestyle='--')

    # Formatting the plot
    ax.set_title('Gold-Backed Digital Asset Market Capitalization', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Market Capitalization (in USD)', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True)

    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    fig.autofmt_xdate()

    # Save the plot
    output_plot_path = os.path.join(output_dir, 'market_cap_visualization.png')
    plt.savefig(output_plot_path, dpi=300, bbox_inches='tight')

    print(f"Visualization saved successfully to {output_plot_path}")

if __name__ == '__main__':
    main()