#!/usr/bin/env python3
"""
Script pour analyser et corriger le fichier SQL LIVRABLE_COMPLET_FOX.sql
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

class SQLAnalyzer:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.issues = []
        self.copy_commands = []
        self.terminators = []
        
    def analyze(self):
        """Analyse le fichier SQL pour identifier les problèmes"""
        print(f"📖 Analyse du fichier: {self.filepath.name}")
        print(f"📏 Taille: {self.filepath.stat().st_size / (1024*1024):.2f} MB")
        print("-" * 80)
        
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            line_num = 0
            in_copy_block = False
            current_copy_table = None
            copy_start_line = None
            data_lines_count = 0
            
            for line in f:
                line_num += 1
                
                # Détection des commandes COPY
                if line.strip().startswith('COPY '):
                    match = re.match(r'COPY\s+([\w.]+)\s*\((.*?)\)\s+FROM\s+stdin;', line)
                    if match:
                        table_name = match.group(1)
                        self.copy_commands.append({
                            'line': line_num,
                            'table': table_name,
                            'command': line.strip()
                        })
                        in_copy_block = True
                        current_copy_table = table_name
                        copy_start_line = line_num
                        data_lines_count = 0
                        print(f"✅ Ligne {line_num}: COPY pour table '{table_name}'")
                
                # Détection des terminateurs \.
                elif line.strip() == '\\.':
                    if in_copy_block:
                        self.terminators.append({
                            'line': line_num,
                            'table': current_copy_table,
                            'data_lines': data_lines_count
                        })
                        print(f"   └─ Ligne {line_num}: Terminateur (données: {data_lines_count} lignes)")
                        in_copy_block = False
                        current_copy_table = None
                    else:
                        # Terminateur orphelin !
                        self.issues.append({
                            'type': 'orphan_terminator',
                            'line': line_num,
                            'severity': 'ERROR',
                            'message': f'Terminateur orphelin (pas de COPY avant)'
                        })
                        print(f"❌ Ligne {line_num}: ERREUR - Terminateur orphelin !")
                
                # Si dans un bloc COPY, compter les lignes de données
                elif in_copy_block:
                    # Vérifier si c'est une ligne de données valide (non vide, non commentaire)
                    if line.strip() and not line.strip().startswith('--'):
                        data_lines_count += 1
                        
                        # Vérifier les patterns suspects
                        if data_lines_count == 1:
                            # La première ligne de données ne devrait pas ressembler à une commande SQL
                            if any(keyword in line.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE']):
                                self.issues.append({
                                    'type': 'sql_in_data',
                                    'line': line_num,
                                    'table': current_copy_table,
                                    'severity': 'WARNING',
                                    'message': f'Ligne ressemblant à du SQL dans les données de {current_copy_table}'
                                })
                                print(f"⚠️  Ligne {line_num}: Commande SQL suspecte dans données de {current_copy_table}")
                
                # Détection de données en dehors d'un bloc COPY
                elif line.strip() and not line.strip().startswith('--') and not line.strip().startswith('SET'):
                    # Vérifier si ça ressemble à des données tabulées
                    if '\t' in line and not any(keyword in line.upper() for keyword in 
                                                ['CREATE', 'ALTER', 'DROP', 'SELECT', 'INSERT', 
                                                 'UPDATE', 'DELETE', 'TOC', 'GRANT', 'DEPENDENCIES']):
                        # Pattern de données détecté hors COPY
                        self.issues.append({
                            'type': 'data_outside_copy',
                            'line': line_num,
                            'severity': 'ERROR',
                            'content': line.strip()[:100] + ('...' if len(line.strip()) > 100 else ''),
                            'message': f'Données détectées hors bloc COPY'
                        })
                        print(f"❌ Ligne {line_num}: ERREUR - Données hors bloc COPY: {line.strip()[:50]}...")
        
        print("-" * 80)
        self.print_summary()
        
    def print_summary(self):
        """Affiche un résumé de l'analyse"""
        print("\n" + "="*80)
        print("📊 RÉSUMÉ DE L'ANALYSE")
        print("="*80)
        
        print(f"\n✅ Tables avec COPY valides: {len(self.copy_commands)}")
        for cmd in self.copy_commands[:10]:  # Afficher les 10 premières
            print(f"   - Ligne {cmd['line']}: {cmd['table']}")
        if len(self.copy_commands) > 10:
            print(f"   ... et {len(self.copy_commands) - 10} autres")
        
        print(f"\n🔚 Terminateurs détectés: {len(self.terminators)}")
        
        # Grouper les problèmes par type
        errors = [i for i in self.issues if i['severity'] == 'ERROR']
        warnings = [i for i in self.issues if i['severity'] == 'WARNING']
        
        print(f"\n❌ ERREURS trouvées: {len(errors)}")
        for issue in errors[:20]:  # Afficher les 20 premières erreurs
            print(f"   - Ligne {issue['line']}: {issue['type']} - {issue['message']}")
            if 'content' in issue:
                print(f"     Contenu: {issue['content']}")
        if len(errors) > 20:
            print(f"   ... et {len(errors) - 20} autres erreurs")
        
        print(f"\n⚠️  AVERTISSEMENTS trouvés: {len(warnings)}")
        for issue in warnings[:10]:
            print(f"   - Ligne {issue['line']}: {issue['message']}")
        if len(warnings) > 10:
            print(f"   ... et {len(warnings) - 10} autres avertissements")
        
        # Recommandations
        print("\n" + "="*80)
        print("💡 RECOMMANDATIONS")
        print("="*80)
        
        if errors:
            print("\n🔧 ACTIONS CORRECTIVES NÉCESSAIRES:")
            
            orphan_terminators = [i for i in errors if i['type'] == 'orphan_terminator']
            if orphan_terminators:
                print(f"\n1. Supprimer {len(orphan_terminators)} terminateur(s) orphelin(s):")
                for t in orphan_terminators[:5]:
                    print(f"   - Ligne {t['line']}")
            
            data_outside = [i for i in errors if i['type'] == 'data_outside_copy']
            if data_outside:
                print(f"\n2. Corriger {len(data_outside)} ligne(s) de données hors bloc COPY:")
                print("   Options:")
                print("   a) Retrouver la commande COPY manquante")
                print("   b) Supprimer ces lignes si elles sont corrompues")
                print("   Premières occurrences:")
                for d in data_outside[:5]:
                    print(f"   - Ligne {d['line']}: {d['content'][:80]}...")
        
        if not errors and not warnings:
            print("\n🎉 Aucun problème détecté ! Le fichier semble valide.")
        
        print("\n" + "="*80)

    def fix_sql_file(self, output_path: str = None):
        """Tente de corriger automatiquement les problèmes"""
        if not output_path:
            output_path = str(self.filepath.parent / f"{self.filepath.stem}_FIXED.sql")
        
        print(f"\n🔧 Correction en cours...")
        print(f"📝 Fichier de sortie: {output_path}")
        
        errors = [i for i in self.issues if i['severity'] == 'ERROR']
        
        if not errors:
            print("✅ Aucune correction nécessaire !")
            return
        
        # Créer un set des lignes à ignorer
        lines_to_skip = set()
        
        # Marquer les terminateurs orphelins à supprimer
        for issue in errors:
            if issue['type'] == 'orphan_terminator':
                lines_to_skip.add(issue['line'])
            elif issue['type'] == 'data_outside_copy':
                lines_to_skip.add(issue['line'])
        
        # Écrire le fichier corrigé
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f_in:
            with open(output_path, 'w', encoding='utf-8') as f_out:
                line_num = 0
                lines_removed = 0
                
                for line in f_in:
                    line_num += 1
                    
                    if line_num in lines_to_skip:
                        lines_removed += 1
                        f_out.write(f"-- LIGNE CORROMPUE SUPPRIMÉE (ligne {line_num}): {line[:80]}...\n")
                    else:
                        f_out.write(line)
        
        print(f"✅ Correction terminée !")
        print(f"📊 {lines_removed} ligne(s) supprimée(s) ou commentée(s)")
        print(f"💾 Fichier corrigé : {output_path}")


def main():
    """Fonction principale"""
    print("="*80)
    print("🔍 ANALYSEUR ET CORRECTEUR SQL")
    print("="*80)
    
    # Chemin du fichier
    sql_file = Path(__file__).parent / "LIVRABLE_COMPLET_FOX.sql"
    
    if not sql_file.exists():
        print(f"❌ ERREUR: Fichier non trouvé: {sql_file}")
        sys.exit(1)
    
    # Créer l'analyseur
    analyzer = SQLAnalyzer(str(sql_file))
    
    # Analyser
    analyzer.analyze()
    
    # Demander si correction
    print("\n" + "="*80)
    response = input("\n🔧 Voulez-vous créer une version corrigée du fichier ? (o/N): ").strip().lower()
    
    if response in ['o', 'oui', 'y', 'yes']:
        analyzer.fix_sql_file()
    else:
        print("✋ Correction annulée. Fichier d'origine préservé.")
    
    print("\n✅ Analyse terminée !")


if __name__ == "__main__":
    main()
