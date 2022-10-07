# import shutil
#
# shutil.rmtree('d:\python_projects\Beetroot_Django\media\images\\')
import transliterate

# import os
#
# dir = 'd:\python_projects\Beetroot_Django\media\images\\'
# for f in os.listdir(dir):
#     os.remove(os.path.join(dir, f))

slug=transliterate.translit('ЄЇіame', reversed=True).lower().replace(' ', '-').\
    replace('є', 'ye').replace('ї', 'yi').replace('і', 'i')
print(slug)