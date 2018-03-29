import os

CMD = r'D:\ImageMagick\ImageMagick-7.0.7-Q16\magick.exe'
SOURCE_PATH = r'D:\pj\fgo\resource1'


def doStrip(path):
    data = {};
    print(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            name = file.lower();
            if name.find('.png') != -1:
                path = os.path.join(root, file)
                os.system('"{0}" {1} -strip {1}'.format(CMD, path, path));


doStrip(SOURCE_PATH)