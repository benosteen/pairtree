import os
import shutil

def copytree(src, dst):
    for f in os.listdir(src):
        src_path = os.path.join(src, f)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst)
        if os.path.isdir(src_path):
            dst_path = os.path.join(dst, f)
            shutil.copytree(src_path, dst_path)
    return
