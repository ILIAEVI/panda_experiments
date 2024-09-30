import pandas as pd
import sqlite3

connection = sqlite3.connect('database.db')

query_wells = "SELECT * FROM wells"
query_plates = "SELECT * FROM plates"
query_experiments = "SELECT * FROM experiments"

wells_df = pd.read_sql(query_wells, connection)
plates_df = pd.read_sql(query_plates, connection)
experiments_df = pd.read_sql(query_experiments, connection)

merged_df = wells_df.merge(plates_df, how='left', on='plate_id', suffixes=('', '_plate'))

final_df = merged_df.merge(experiments_df, how='left', on='experiment_id', suffixes=('', '_experiment'))


def fill_properties(row):
    if pd.isnull(row['property_name']) and not pd.isnull(row['property_name_plate']):
        row['property_name'] = row['property_name_plate']
    if pd.isnull(row['property_value']) and not pd.isnull(row['property_value_plate']):
        row['property_value'] = row['property_value_plate']
    if pd.isnull(row['property_name']) and not pd.isnull(row['property_name_experiment']):
        row['property_name'] = row['property_name_experiment']
    if pd.isnull(row['property_value']) and not pd.isnull(row['property_value_experiment']):
        row['property_value'] = row['property_value_experiment']
    return row

final_df = final_df.apply(fill_properties, axis=1)

final_result = final_df[['well_id', 'well_row', 'well_column', 'property_name', 'property_value']]

output_file_path = 'merged_results.xlsx'
final_result.to_excel(output_file_path, index=False)

print(f"Results saved to {output_file_path}")

connection.close()
