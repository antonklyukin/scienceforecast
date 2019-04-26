import pandas as pd

def query_to_df(query_list):
    df = pd.DataFrame(query_list, columns =  ['Collocation', 'Publication year', 'Publication quarter'])
    # Получение топ словосочетаний
    ser = df.groupby(['Collocation']).size().sort_values(ascending=False).nlargest(5)

    df = df.loc[df['Collocation'].isin(ser.keys())]  # фильтрация по топу
    new_df = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0:'records'})
    # Получение датафрейма из топ 5 словосочетаний разбитые по кварталам
    new_df.sort_values(by=['Collocation', 'Publication year', 'Publication quarter', 'records'], ascending=False, inplace=True)

    return new_df

def output_for_page (df):
    """
    Функция вводит словарь вида
    {
        'years': [2019, ....],
        'collocation_name': {'years':[], 'records'}
    }
    """
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]
    df = df.drop(columns=['Publication quarter'])
    col_dict = df.to_dict('list')
    output_dict = {'years': df['Publication year'].unique()}
    for collocation, year, records in zip(col_dict['Collocation'], col_dict['Publication year'], col_dict['records']):
        if collocation in output_dict:
            
            if year in output_dict[collocation]['years']:
                ident = output_dict[collocation]['years'].index(year)
                output_dict[collocation]['records'][ident] += records
            else:
                output_dict[collocation]['years'].append(year)
                output_dict[collocation]['records'].append(records)
        else:
            output_dict[collocation] = {'years': [year], 'records': [records]}
    i = 0
    for collocation in output_dict:
        if collocation == 'years':
            continue
        output_dict[collocation]['color'] = colors[i]
        del output_dict[collocation]['years']
        i+=1
    return output_dict