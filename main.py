import pandas as pd
import os
from datetime import datetime

def transform_source1(df):
    """
    Transforms the DataFrame from source1.csv to a standard format.
    - Renames columns to 'id', 'name', 'age'.
    """
    df = df.rename(columns={'ID': 'id', 'Name': 'name', 'Age': 'age'})
    return df

def transform_source2(df):
    """
    Transforms the DataFrame from source2.csv to a standard format.
    - Renames 'user_id' to 'id' and 'full_name' to 'name'.
    - Calculates 'age' from 'birth_year'.
    """
    df = df.rename(columns={'user_id': 'id', 'full_name': 'name'})
    current_year = datetime.now().year
    df['age'] = current_year - df['birth_year']
    df = df.drop(columns=['birth_year'])
    return df

def main():
    """
    Main function to orchestrate the data processing pipeline.
    """
    # Define file paths
    data_dir = 'data'
    output_dir = 'output'
    source1_path = os.path.join(data_dir, 'source1.csv')
    source2_path = os.path.join(data_dir, 'source2.csv')
    output_path = os.path.join(output_dir, 'unified_data.csv')

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read and transform source1
    df1 = pd.read_csv(source1_path)
    df1_transformed = transform_source1(df1)

    # Read and transform source2
    df2 = pd.read_csv(source2_path)
    df2_transformed = transform_source2(df2)

    # Merge the transformed dataframes
    merged_df = pd.concat([df1_transformed, df2_transformed], ignore_index=True)

    # Export the unified data
    merged_df.to_csv(output_path, index=False)
    print(f"Data processing complete. Unified data exported to {output_path}")

if __name__ == '__main__':
    main()