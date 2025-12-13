import os,glob

exe = '"C:/Program Files (x86)/Kolor/autopano_v103zip/autopano.exe"'

def execAutopano(lfiles,rep,output):
    os.chdir(rep)
    lf = ' '.join(glob.glob(lfiles))
    ch = exe + ' /f ' + lf + " /path:./ /project:hugin /name:" + output
    print(ch)
    os.system(ch)
    
if __name__=="__main__":
    rep="C:/Users/marc/Documents/Dossiers personnel/Mes images/2019/2019-08_Ecosse/TriPhotos/Pano/"
    execAutopano("Pano_160_*.JPG",rep,"Pano_160")