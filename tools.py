import os
import shutil


def prepare_output_directory(path):
    """ Очищает папку output от файлов предыдущего запуска """
    try:
        shutil.rmtree(path)
    except OSError:
        print("Directory %s is deleted" % path)

    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory '%s' " % path)


def save_text_in_file(text_file_path, text):
    text_file = open(text_file_path, "w")
    text_file.write(text)
    text_file.close()