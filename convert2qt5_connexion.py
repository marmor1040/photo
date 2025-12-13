import re
import sys

def convertir_syntaxe_pyqt(input_file, output_file):
    """
    Convertit la syntaxe PyQt4 vers PyQt5 pour les connexions de signaux.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        contenu = f.readlines()

    pattern = re.compile(
        r'QtCore\.QObject\.connect\((\w+),\s*QtCore\.SIGNAL\("([^"]+)"\),\s*(\w+)\)'
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        for ligne in contenu:
            match = pattern.search(ligne)
            if match:
                objet = match.group(1)
                signal = match.group(2)
                slot = match.group(3)
                # Remplace la ligne
                nouvelle_ligne = f"{objet}.{signal}.connect({slot})\n"
                ligne = nouvelle_ligne
            f.write(ligne)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_pyqt.py <input_file> <save_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convertir_syntaxe_pyqt(input_file, output_file)
    print(f"Conversion terminée. Résultat enregistré dans {output_file}")
