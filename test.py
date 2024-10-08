import pandas as pd

urls2021= ['https://recaps.competitionsuite.com/f5857673-6380-422b-8471-cea7cd2e5b55.htm', 'https://recaps.competitionsuite.com/7ad58ffb-db14-4c6a-991b-b04210613c02.htm', 'https://recaps.competitionsuite.com/31f07290-b6c8-4df0-82c3-875e2186b3fc.htm', 'https://recaps.competitionsuite.com/c7df6848-d9d9-4d69-aece-36c93b6c5003.htm', 'https://recaps.competitionsuite.com/b1ff8463-0f06-456e-830b-686de4093a3c.htm', 'https://recaps.competitionsuite.com/48ca6831-859f-4f39-8f40-ac4d847e0aa0.htm', 'https://recaps.competitionsuite.com/c121ee96-6dd5-4342-9599-5bff22a23b46.htm', 'https://recaps.competitionsuite.com/845557ce-dc84-4a25-b4b8-95793abca6e9.htm', 'https://recaps.competitionsuite.com/9f546ff0-89cb-4dfa-9799-565314c629d1.htm', 'https://recaps.competitionsuite.com/c2e6b7a1-c56d-4839-b3e6-02e568d2cc96.htm', 'https://recaps.competitionsuite.com/35ddfcbc-e84d-4b41-a704-dee2a275d596.htm', 'https://recaps.competitionsuite.com/8aa4d197-f8e0-4daf-8390-fe793f2d5d1c.htm', 'https://recaps.competitionsuite.com/72edbad5-6fbc-472c-b377-2d1d8b9e6538.htm', 'https://recaps.competitionsuite.com/d5e19e63-c68c-4002-a7a8-9f971fae0c66.htm', 'https://recaps.competitionsuite.com/625e8afb-99cb-49cb-bebe-f207b20f9e4a.htm', 'https://recaps.competitionsuite.com/891938a1-0456-4e2c-9136-52a859ca9570.htm', 'https://recaps.competitionsuite.com/68aede15-fa6b-4937-a555-cd3f9f63f38b.htm', 'https://recaps.competitionsuite.com/d8e2ea0a-fa48-4f57-b7c3-b29d52b09840.htm', 'https://recaps.competitionsuite.com/836d8bf2-956b-4ad5-a41c-da184cfca6ef.htm', 'https://recaps.competitionsuite.com/42651f85-779a-4290-9130-c49775af163d.htm', 'https://recaps.competitionsuite.com/66e2e967-37cf-49cc-aacb-4138b82d1f44.htm', 'https://recaps.competitionsuite.com/e75b2f44-5162-40e5-9856-c71e641b17dd.htm', 'https://recaps.competitionsuite.com/d5221904-a3aa-4aab-83b5-1b9360c55805.htm', 'https://recaps.competitionsuite.com/a1581e9a-cafb-4fbe-aa8f-6f64d5c951f1.htm', 'https://recaps.competitionsuite.com/f795951c-760b-4e8e-8c92-98ebd4edb092.htm', 'https://recaps.competitionsuite.com/05868879-8b45-4ef6-be25-5ca5536a71d3.htm', 'https://recaps.competitionsuite.com/0c994b24-eba8-4b62-9145-30438c6b07bc.htm', 'https://recaps.competitionsuite.com/b50e85fd-8b08-4666-893f-c6985e9fe54c.htm', 'https://recaps.competitionsuite.com/abb8978d-4b0a-41fd-99f1-906e4602d063.htm', 'https://recaps.competitionsuite.com/e13fb282-59fd-4871-a67f-87d825538de4.htm']

df = pd.read_csv('csbcData2023.csv')


# print(df['comp'].unique())
# print(df[df['school'].str.contains('Tournament')])

# print(f'The selected dataframe has ' + str(df['comp'].nunique())+ ' competitions')
# print(df[df['division'].str.contains('Finals')])



# colsFix = ['MPER', 'MPIR', 'MPSTR', 'VPER', 'VPIR', 'VPSTR', 'PerfTR', 'GEMCER', 'GEMPER', 'GEMSTR', 'GEVCER', 'GEVPER', 'GEVSTR', 'GETR', 'PCR', 'PAR', 'PTR', 'PSTR', 'GCR', 'GAR', 'GTR', 'GSTR', 'STR', 'TotalRank', 'MPES', 'MPIS', 'MPSTS', 'VPES', 'VPIS', 'VPSTS', 'PerfTS', 'GEMCES', 'GEMPES', 'GEMSTS', 'GEVCES', 'GEVPES', 'GEVSTS', 'GETS', 'PCS', 'PAS', 'PTS', 'PSTS', 'GCS', 'GAS', 'GTS', 'GSTS', 'STS', 'T/P', 'TotalScore']
# def convert_list_to_scalar(value):
#     if isinstance(value, str):
#         return float(value.replace('[', '').replace(']', ''))
        
#     elif isinstance(value, float):
    
#         return value




# for col in colsFix: 
#     df[col] = df[col].apply(convert_list_to_scalar)
    
# df.to_csv('csbcData2023.csv', index = False)

# Function to convert values in the 'Scores' column to floats


