import shutil
import os

if not os.path.exists('destination'):
    os.mkdir('destination')
with open('move_me.txt', 'w') as f:
    f.write('Temporary file')
shutil.move('move_me.txt', 'destination/moved_file.txt')