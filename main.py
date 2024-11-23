import time
import cv2
import sys
from ffpyplayer.player import MediaPlayer

video_path = "./PatriceRushen-ForgetMeNots(OfficialVideo).mp4"

# Открытие видео и аудио
video = cv2.VideoCapture(video_path)
music_player = MediaPlayer(video_path)

# Параметры видео
fps = video.get(cv2.CAP_PROP_FPS)
seconds_per_frame = 1 / fps

# Градации серого для ASCII
GRAY_SCALE = "@#8&WM%$*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "
SCALE = 8  # Масштаб уменьшения для вывода

def grayScaleNumber(num):
    # Преобразование яркости пикселя в индекс символа
    scale_size = len(GRAY_SCALE) - 105
    index = int((num / 255) * scale_size)
    return GRAY_SCALE[index]

def printFrameInConsole(frame, height, width):
    # Уменьшение размеров кадра для консоли
    console_out_dim = (int(width / SCALE), int(height / SCALE))
    frame = cv2.resize(frame, console_out_dim, interpolation=cv2.INTER_AREA)

    to_print = ''
    for row in frame:
        to_print += ''.join([grayScaleNumber(num) for num in row.tolist()]) + "\n"

    sys.stdout.write("\033[H\033[J")  # Очистка консоли
    sys.stdout.write(to_print)
    sys.stdout.flush()

# Основной цикл воспроизведения
while True:
    frame_t_start = time.time()

    # Чтение кадра
    ret, frame = video.read()
    if not ret:
        break

    # Обработка аудио
    _, val = music_player.get_frame()
    if val == 'eof':
        break

    # Преобразование кадра в оттенки серого
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Вывод кадра в консоль
    height, width = frame.shape
    printFrameInConsole(frame, height, width)

    # Обработка выхода
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # Задержка для обеспечения корректной частоты кадров
    while (time.time() - frame_t_start) < seconds_per_frame:
        pass

# Освобождение ресурсов
video.release()
cv2.destroyAllWindows()
