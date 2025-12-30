# -*- coding:utf-8 -*-
import numpy,os
import os.path as osp
import json
from PyQt5.QtCore import Qt,QRect

PHOTO_PLEIN_ECRAN = True
# 1 : ecran secondaire / 2 : ecran portable
ECRAN_DEFAULT_ARBO = 1
ECRAN_DEFAULT_MINIATURE = 1
VISIONNEUSE_GEOMETRY = QRect(0,0,1140,625)
MINIATURES_GEOMETRY = ((320,25,1280,840),(1920,25,1600,1040))
#MINIATURES_GEOMETRY = ((320,25,1280,840),(1920,25,1600,400))
ARBO_GEOMETRY = ((0,25,500,850),(1600,25,500,1050))
RENOMMAGE_GEOMETRY = ((500,25,500,500),(2170,25,500,500))
#THUMBS_GEOMETRY = (0,20,1440,600)
FILTRE_POS = (0,590)
COORD_FEN_MINIATURE = QRect(1100,20,296,700)
LARGEUR_IMAGE = 256
AUTO_CHARGEMENT = numpy.array([0,1,-1,2,-2])
PRINT_TOUCHE = False
ETOILE0 = Qt.Key_0
ETOILE1 = Qt.Key_1
ETOILE2 = Qt.Key_2
ETOILE3 = Qt.Key_3
PREC = Qt.Key_A
SUIV = Qt.Key_Z
NETTE = Qt.Key_N
NOM = Qt.Key_R
NOMBRE_MINIATURES_PAR_LIGNE = 6
LISTE_WORKSPACE = []
NOM_PANO = "Pano_"

MODE = 0 
MODE_TRI = 0 # mode tri avec case à cocher
MODE_TRI_SS_CAC = 2 # mode tri sans case à cocher
MODE_VISIONNEUSE = 1 # mode visionneuse simple

DESCRIPTION_PHOTO={'date':'DateTimeOriginal',
                   'heure':'DateTimeOriginal',
                   'pivoter':'Orientation',
                   'qualite':'Quality',
                   'vitesse':'ExposureTime',
                   'ouverture':'FNumber',
                   'iso':'ISOSpeedRatings',
                   'correction':'ExposureBiasValue',
                   'flash':'Flash',
                   'focale':'FocalLength',
                   'tailleY':'PixelYDimension',
                   'tailleX':'PixelXDimension',
                   'appareil':'Model',
                   'zoom':'LensModel'}
 

cwd = os.getcwd()
WORKSPACE_PATH = None
FILTRE_PATH = None
EXEC_PATH = None
ICON_PATH = None
if osp.isdir(cwd+'/Data'):
    EXEC_PATH = cwd
elif osp.isdir(cwd+'/../Data'): 
    EXEC_PATH = cwd + '/..'
    
WORKSPACE_PATH = EXEC_PATH + '/Data/workspace.dat'
ICON_PATH = EXEC_PATH + '/icon/'
FILTRE_PATH = EXEC_PATH + '/Data/filtre.dat'
GEOMETRY_FEN_ARBO_PATH = EXEC_PATH + '/Data/geometry_arbo.dat'
GEOMETRY_FEN_THUMB_PATH = EXEC_PATH + '/Data/geometry_thumb.dat'
GEOMETRY_FEN_VISIO_PATH = EXEC_PATH + '/Data/geometry_visio.dat'
       
def getWorkspaces():
    global LISTE_WORKSPACE
    if LISTE_WORKSPACE: return LISTE_WORKSPACE
    if osp.isfile(WORKSPACE_PATH):
        with open(WORKSPACE_PATH,'r') as f:
            try:
                LISTE_WORKSPACE = json.load(f)
                return LISTE_WORKSPACE
            except:
                pass
    return ['Images']

def addWorkspace(workspace):
    global LISTE_WORKSPACE
    if workspace in LISTE_WORKSPACE:
        LISTE_WORKSPACE.remove(workspace)
    LISTE_WORKSPACE.insert(0,workspace)
    with open(WORKSPACE_PATH,'w') as f:
        json.dump(LISTE_WORKSPACE,f)

def removeWorkspace(workspace):
    global LISTE_WORKSPACE
    if workspace in LISTE_WORKSPACE:
        LISTE_WORKSPACE.remove(workspace)
    with open(WORKSPACE_PATH,'w') as f:
        json.dump(LISTE_WORKSPACE,f)

def getFiltreDefaut():
    filtre = None
    if osp.isfile(FILTRE_PATH):
        with open(FILTRE_PATH,'r') as f:
            try:
                filtre = json.load(f)
            except:
                pass
    return filtre
        
def setFiltreDefaut(filtre):
    import pickle
    with open(FILTRE_PATH,'w') as f:
        filtre.__album=None
        print("filtre non sauvegardé")
        #pickle.dump(filtre,f)

def setMode(mode):
    global MODE
    MODE = mode
    
def nbColMiniatures():
    if MODE != MODE_VISIONNEUSE:
        return NOMBRE_MINIATURES_PAR_LIGNE
    else:
        return 1
    
def getIcon(icon_name):
    return ICON_PATH+icon_name