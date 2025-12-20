import re
import sys,os,shutil

def convertir_syntaxe_pyqt(input_file):
    """
    Convertit la syntaxe PyQt4 vers PyQt5 pour les connexions de signaux.
    """
    if not os.path.isfile(input_file+".qt4"):
        shutil.copyfile(input_file, input_file+".qt4")
        print(f"Fichier original sauvegardé sous {input_file}.qt4")

    with open(input_file, 'r', encoding='utf-8') as f:
        contenu = f.readlines()

    #                                 connect(  'widget',QtCore.SIGNAL("signal()"),slot)
    pattern = re.compile(r"(\s+)[\w\.]+connect\(([\w\.]+),[^\"]+\"([^\"]+)\"\),([\w\.]+)")
    #    QObject.connect(self.bt_repertoire,QtCore.SIGNAL("clicked()"),self.choixRepertoire)
    #    QObject.connect(self.sb_reduction,QtCore.SIGNAL("valueChanged(int)"),self.afficheEstime)

    with open(input_file, 'w', encoding='utf-8') as f:
        for ligne in contenu:
            match = pattern.search(ligne)
            if match:
                print(match)
                deb = match.group(1)
                objet = match.group(2)
                signal = match.group(3).split('(')[0]
                slot = match.group(4)
                # Remplace la ligne
                nouvelle_ligne = f"{deb}{objet}.{signal}.connect({slot})\n"
                ligne = nouvelle_ligne
                print("-->", nouvelle_ligne)
            f.write(ligne)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_pyqt.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    convertir_syntaxe_pyqt(input_file)
    print(f"Conversion terminée.")
