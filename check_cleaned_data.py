import pandas as pd

df=pd.read_csv('cleaned_dataset.csv')


# Check for duplicates based on all columns
duplicate_rows = df[df.duplicated()]

if not duplicate_rows.empty:
    print("Duplicate rows:")
    print(duplicate_rows)
else:
    print("No duplicate rows found.")

null_values = df.isnull().any()

if null_values.any():
    print("Columns with null values:")
    print(null_values[null_values])  # Print columns that have null values
else:
    print("No null values found.")


unknown_values = (df == 'Unknown').any()

if unknown_values.any():
    print("Columns with 'Unknown' values:")
    print(unknown_values[unknown_values])  # Print columns that have 'Unknown' values
else:
    print("No 'Unknown' values found.")


date_formats = df['Join Date'].apply(lambda x: pd.to_datetime(x, errors='coerce').strftime('%Y-%m-%d') if pd.notna(x) else None).dropna().unique()

if len(date_formats) == 1:
    print(f"The common date format in the 'Join Date' column is: {date_formats[0]}")
else:
    print("Multiple date formats are present. Additional analysis may be needed.")
ntdate=df['Join Date'].count().sum()
print('COUNT OF VALUES:', countdate)


date_formats = df['Join Date'].apply(lambda x: pd.to_datetime(x, errors='coerce').strftime('%Y-%m-%d') if pd.notna(x) else None).dropna().unique()

if len(date_formats) == 1:
    print(f"The common date format in the 'Join Date' column is: {date_formats[0]}")
else:
    # Filter rows with dates not matching the unique formats
    filtered_df = df[~df['Join Date'].isin(date_formats)]

    if not filtered_df.empty:
        print("\nRows with multiple date formats:")
        print(filtered_df[['Join Date']])
    else:
        print("\nNo rows found with multiple date formats.")
