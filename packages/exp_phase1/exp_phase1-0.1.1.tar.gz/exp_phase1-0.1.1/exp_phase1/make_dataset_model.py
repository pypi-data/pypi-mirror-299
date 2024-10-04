import pandas as pd


def find_outliers(df):
    """
    Function that will remove the outliers present.
    """
    outliers = pd.DataFrame()
    for column in df.select_dtypes(include=['float64', 'int64']).columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        column_outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        outliers = pd.concat([outliers, column_outliers])
    return outliers.drop_duplicates()

def split_item_id(df):
    """
    Function that will split the item id column into depart id and item id.
    """
# Check if 'item_id' column exists in the DataFrame
    if 'item_id' not in df.columns:
        raise ValueError("DataFrame must contain 'item_id' column.")

    # Split the 'item_id' column
    components = df['item_id'].str.split('_', expand=True)

    # Create new columns in the DataFrame
    df['depart_id'] = components[0]+ '_' + components[1]  # Category
    df['item_id'] = components[2]  # Identifier
    return df
def split_store_id(df):
    """
    Function that will split the store id column into state and store id.
    """
# Check if 'item_id' column exists in the DataFrame
    if 'store_id' not in df.columns:
        raise ValueError("DataFrame must contain 'store_id' column.")

    # Split the 'store_id' column
    components = df['store_id'].str.split('_', expand=True)

    # Create new columns in the DataFrame
    df['state'] = components[0]  # Category
    df['store_id'] = components[1]  # Identifier
    return df

def make_dataset_model(train_df,test_df):
  """
    Function that will perform all the above functions '
    to develop a training and testing dataset for modelling phase.

    returns: Training and Testing Data
  """
  train_df = find_outliers(train_df)
  print("Removed Outliers Training")
  test_df = find_outliers(test_df)
  print("Removed Outliers Testing")
  train_df = split_item_id(train_df)
  train_df=split_store_id(train_df)
  print("Spliting Item ID Outliers Training...")
  print("Spliting Store ID Outliers Training...")
  test_df = split_item_id(test_df)
  test_df=split_store_id(test_df)
  print("Spliting Item ID Outliers Testing...")
  print("Spliting Store ID Outliers Testing...")
  return train_df,test_df