import pandas as pd

def process_data(df):
    '''Format Item_fetched, restrict price range and remove too cheap new homes'''
    # Datetime formatting
    df.Item_fetched = pd.to_datetime(df.Item_fetched)
    
    # Let's restrcit to under 1.5 million eur prices
    df = df.loc[(df.Price < 1500000) & (df.Price > 50000)]
    
    # Let's restrcit to under 399 m2 homes
    df = df.loc[(df.Size <= 300)]
    
    # Clean some incorrect prices 
    # There may be too cheap ones in new buildings? Likely to wrong price (myyntihinta not velaton myyntihinta)
    df = df.loc[~((df.Year_build >= 2000) & (df.Price/df.Size < 2000) & (df.House_type.isin(['Block of flats','Terraced house'])))]
    return df

def sortList(lista):
    lista = [x for x in lista if type(x) == str]
    lista=sorted(lista)
    return lista

def get_missing_data(data):
    mod_data_na = (data.isnull().sum() / len(data)) * 100
    mod_data_na = mod_data_na.drop(mod_data_na[mod_data_na == 0].index).sort_values(ascending=False)[:30]
    missing_data = pd.DataFrame({'Missing Ratio' :mod_data_na})
    display(missing_data)
    return

def getElevatorImputing(df):
    return df.loc[df.Elevator.notna()].groupby('Year_build')['Elevator'].apply(lambda x: x.mode().iloc[0]).to_dict()


def drop_unique_area_rows(data):
    # Drop unique area rows.
    counts = data['Area'].value_counts()
    data = data[~data['Area'].isin(counts[counts < 2].index)]
    return data