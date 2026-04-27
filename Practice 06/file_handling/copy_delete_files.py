import shutil
import os
from pathlib import Path
shutil.copy('sample.txt', 'sample_backup.txt')
if os.path.exists('sample_backup.txt'):
    os.remove('sample_backup.txt')
    print("Файл удален")