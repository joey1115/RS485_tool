import os
import shutil


dir = os.path.abspath(os.curdir)
pyc_list = []
for dirpath, dirnames, filenames in os.walk(dir):
    if '__pycache__' in dirnames:
        pyc_list.append(dirpath)

path = dir + '\\pyc_template' + '\\' + os.path.split(dir)[-1]

if os.path.exists(path):
    shutil.rmtree(path)
os.makedirs(path)

for pyc in pyc_list:
    pyc_path = pyc + '\\__pycache__'
    files = os.listdir(pyc_path)
    for file in files:
        if file.endswith('.pyc') and 'cpython-34' in file and file != 'py_test.cpython-34.pyc':
            oldname = pyc_path + '\\' + file
            file_path = path + pyc[len(dir):]
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            newname = path + pyc[len(dir):] + '\\' + file.replace('.cpython-34', '')
            shutil.copyfile(oldname, newname)
