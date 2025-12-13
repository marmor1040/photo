from distutils.core import setup
import py2exe
setup(console=[("../src/TriPhoto.py"),("../src/Visionneuse.py")],
      data_files=[("Data",["../src/Data/rep_defaut.dat",
                           "../src/Data/filtre.dat",
                           "../src/Data/etoile.bmp",
                           "../src/Data/2etoiles.bmp",
                           "../src/Data/3etoiles.bmp",
                           "../src/Data/repTri.png",
                           "../src/Data/repImage.png",
                           "../src/Data/repVideo.png",
                           "../src/Data/repNormal.png"]),
                  # il faut copier la dll de jpeg pour charger les images
                  ("imageformats",["C:\Python26\Lib\site-packages\PyQt5\plugins\imageformats\qjpeg4.dll"])],
      options={"py2exe" : {
                           # Needed only for Qt-based applications:
                           "includes" : ['sip','PyQt5.Qt'],
                           "dll_excludes": ['MSVCP90.dll']  
                           }}
    )

