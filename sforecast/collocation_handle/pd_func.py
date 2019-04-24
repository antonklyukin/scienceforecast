import pandas as pd

def query_to_df(query_list):
    df = pd.DataFrame(query_list, columns =  ['Collocation', 'Publication year', 'Publication quarter'])
    new_df = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0:'records'})
    # print('_________________________________________________________')
    print(new_df)
    return new_df