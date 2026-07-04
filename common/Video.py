import sys,os
import cv2
import vlc
import subprocess
import json
from datetime import datetime
import win32api, win32con
import numpy as np

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

os.environ["PATH"] += ";C:\\Program Files\\FFmpeg\\bin"

def get_stream(md, stream_type):
    return next(
        (s for s in md.get("streams", []) if s.get("codec_type") == stream_type),
        None
    )

def get_metadata_ffmpeg(video_path):
    metadata = {}
    cmd = [
        "ffprobe",
        "-v", "error",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    md = json.loads(result.stdout)
    video = get_stream(md, "video")

    if video:
        codec = video.get("codec_name")
        date_heure = getDateHeure(md["format"]["tags"].get("creation_time", ""))
        metadata = {
            "duree": f"{float(video.get('duration', 0)):.2f}",
            "largeur": video.get("width"),
            "hauteur": video.get("height"),
            "date": date_heure[0],
            "heure": date_heure[1],
            "codec": codec,
        }
    return metadata

def getDateHeure(ch):
    if ch:
        dt = datetime.fromisoformat(ch.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y"),dt.strftime("%H:%M:%S")
    return "unknown","unknown"

def rotate_video(video_path, output_path, angle):
    pass

def creerThumbnail(pVideo,pThumb):
    cap = cv2.VideoCapture(pVideo)
    if not cap.isOpened():
        return None

    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None

    h, w = frame.shape[:2]

    # Calcul du facteur d'échelle (conserve le ratio)
    scale = 1.0
    if w > 256:
        scale = min(scale, 256 / w)
    if h > 256:
        scale = min(scale, 256 / h)

    if scale != 1.0:
        new_w = int(w * scale)
        new_h = int(h * scale)
        frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

    h, w = frame.shape[:2]
    size = 60

    cx, cy = w // 2, h // 2

    # Triangle ▶
    pts = np.array([(cx - 8, cy - 15),(cx - 8, cy + 15),(cx + 15, cy)], np.int32)

    overlay = frame.copy()
    cv2.circle(overlay, (cx, cy), 30, (100,100,100), -1)
    cv2.fillConvexPoly(overlay, pts, (255, 255, 255))

    # Fusion alpha
    alpha=0.6             # transparence
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Sauvegarde JPG
    try:
        # Utilisation de l'API OpenCV pour sauvegarder l'image
        # imwrite ne fonctionne pas si caratères spéciaux dans le chemin
        # cv2.imwrite(pThumb,frame,[cv2.IMWRITE_JPEG_QUALITY, 90])
        success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        with open(pThumb, "wb") as f: 
            f.write(buffer.tobytes())
    except Exception as e:
        print("Erreur sauvegarde miniature :", e)
        return
    win32api.SetFileAttributes(pThumb,win32con.FILE_ATTRIBUTE_HIDDEN)

    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # h, w, ch = frame.shape
    # h=256
    # w=int
    # qimg = QImage(frame.data,w,h,ch * w,QImage.Format_RGB888)
    # qimg.save(pThumb,"JPG")

def video_first_frame_to_pixmap(video_path, max_width=300):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None

    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    h, w = frame.shape[:2]

    # Calcul du facteur d'échelle (conserve le ratio)
    scale = 1.0
    if w > 256:
        scale = min(scale, 256 / w)
    if h > 256:
        scale = min(scale, 256 / h)

    if scale != 1.0:
        new_w = int(w * scale)
        new_h = int(h * scale)
        frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, ch = frame.shape
    color=(255, 255, 255)
    alpha=0.6             # transparence
    h, w = frame.shape[:2]
    size = 60

    cx, cy = w // 2, h // 2

    # Triangle ▶
    pts = np.array([
        (cx - 8, cy - 15),
        (cx - 8, cy + 15),
        (cx + 15, cy)
    ], np.int32)

    overlay = frame.copy()
    cv2.circle(overlay, (cx, cy), 30, (100,100,100), -1)
    cv2.fillConvexPoly(overlay, pts, (255, 255, 255))

    # Fusion alpha
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    qimg = QImage(frame.data,w,h,ch * w,QImage.Format_RGB888)

    pixmap = QPixmap.fromImage(qimg)
    print("scaled2")
    return pixmap.scaledToWidth(max_width)

def get_video_duration_vlc(path):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(path)
    player.set_media(media)

    media.parse()
    return media.get_duration() / 1000  # ms → s

class VideoWidget(QWidget):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def showEvent(self, event):
        self.player.set_hwnd(int(self.winId()))

        media = self.instance.media_new(self.video_path)
        self.player.set_media(media)

        # Démarrer légèrement après l'affichage
        QTimer.singleShot(100, self.player.play)

class MainWindow(QWidget):
    def __init__(self, video_path):
        super().__init__()

        self.setWindowTitle("Miniature + Vidéo")
        self.resize(1000, 500)

        layout = QHBoxLayout(self)

        # Miniature
        thumb_label = QLabel()
        pixmap = video_first_frame_to_pixmap(video_path)
        if pixmap:
            thumb_label.setPixmap(pixmap)
        else:
            thumb_label.setText("Miniature indisponible")

        # Vidéo
        video_widget = VideoWidget(video_path)

        layout.addWidget(thumb_label)
        layout.addWidget(video_widget, 1)  # prend plus de place

if __name__ == "__main__":
    app = QApplication(sys.argv)

    video_path = "C:/Users/Marc/Pictures/test2/PXL_20250209_142638724.mp4"
    video_path = "C:/Users/Marc/Pictures/test2/20221214_075013.mp4"
    md = get_metadata_ffmpeg(video_path)
    print("Métadonnées vidéo :", md)
    window = MainWindow(video_path)
    window.show()

    sys.exit(app.exec_())
