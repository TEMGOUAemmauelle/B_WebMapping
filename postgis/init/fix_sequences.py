import re
import os

filepath = "/home/gates/Documents/Niveau5/Traitement d'image/Webmapping/backend/postgis/init/LIVRABLE_AVEC_SCHEMA.sql"
output_path = "/home/gates/Documents/Niveau5/Traitement d'image/Webmapping/backend/postgis/init/LIVRABLE_AVEC_SCHEMA_FIXED.sql"

tables_to_fix = [
    "data_elevage_nat_temp",
    "data_elevage_reg_temp",
    "data_peche_dep_temp",
    "data_peche_infra_temp",
    "data_peche_nat_temp",
    "ref_arrondissements",
    "ref_chefs_lieux_arrond",
    "ref_chefs_lieux_dep",
    "ref_departements",
    "ref_pays",
    "ref_regions"
]

print(f"Fixing sequences for tables: {tables_to_fix}")

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f_in:
    content = f_in.read()

for table in tables_to_fix:
    # Pattern to find the CREATE TABLE block and replace BIGINT with BIGSERIAL for the id column
    # We look for CREATE TABLE public.table_name followed by "id" BIGINT PRIMARY KEY
    pattern = rf'(CREATE TABLE public\.{table} \(\s+"id") BIGINT PRIMARY KEY'
    replacement = r'\1 BIGSERIAL PRIMARY KEY'
    
    if re.search(pattern, content):
        print(f"Updating table {table}")
        content = re.sub(pattern, replacement, content)
    else:
        print(f"Could not find pattern for table {table}")

with open(output_path, 'w', encoding='utf-8') as f_out:
    f_out.write(content)

print(f"Fixed file saved to {output_path}")
