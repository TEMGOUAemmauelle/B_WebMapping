#!/usr/bin/env python3
import re
from pathlib import Path

def fix_sql(input_path):
    output_path = input_path.parent / "LIVRABLE_FINAL_CLEAN.sql"
    print(f"🛠️ Réparation de {input_path.name}...")
    
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Commenter les commandes psql incompatibles
    print("🚫 Désactivation des commandes incompatibles...")
    content = content.replace('\\restrict', '-- \\restrict')
    content = content.replace('\\unrestrict', '-- \\unrestrict')
    content = re.sub(r'(SET\s+transaction_timeout\s*=\s*.*?;)', r'-- \1', content)

    # 2. Ajouter DROP TABLE IF EXISTS avant CREATE TABLE
    print("🧹 Ajout des DROP TABLE CASCADE...")
    content = re.sub(r'CREATE TABLE ([\w.]+)', r'DROP TABLE IF EXISTS \1 CASCADE;\nCREATE TABLE \1', content)
    
    # 3. Ajouter DROP SEQUENCE IF EXISTS avant CREATE SEQUENCE
    content = re.sub(r'CREATE SEQUENCE ([\w.]+)', r'DROP SEQUENCE IF EXISTS \1 CASCADE;\nCREATE SEQUENCE \1', content)

    # 4. Correction des chaînes vides dans les données COPY
    print("📝 Correction des données (chaînes vides -> NULL)...")
    # Remplacement des tabulations suivies de "" par \N (NULL)
    content = content.replace('\t""\t', '\t\\N\t')
    content = content.replace('\t""\n', '\t\\N\n')
    content = content.replace('""\t', '\\N\t')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Terminé ! Fichier généré : {output_path.name}")

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    # On cible le dernier fichier que vous avez essayé d'importer
    input_file = script_dir / "LIVRABLE_COMPLET_FOX2.sql"
    
    if input_file.exists():
        fix_sql(input_file)
    else:
        print(f"❌ Erreur : {input_file.name} introuvable dans {script_dir}")
