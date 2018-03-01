import os
import subprocess

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    f = f.split('.')
    name = '.'.join(f[:-1])
    ext = f[-1]
    if ext == 'ui':
        print(subprocess.run([r"C:\Users\alex1\AppData\Local\Programs\Python\Python36-32\Scripts\pyuic5.exe", name + ".ui", "-o", name + ".py"], stdout=subprocess.PIPE).stdout.decode("utf8"))
