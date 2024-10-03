from PIL import Image
import os


def replace_white_with_red(image_path):
    img = Image.open(image_path).convert('RGB')
    data = img.getdata()

    new_data = []
    for item in data:
        # Заменяем белый цвет (255, 255, 255) на красный (255, 0, 0)
        if item == (255, 255, 255):
            new_data.append((255, 0, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(image_path)


folder_path = 'COVID/masks'
for filename in os.listdir(folder_path):
    if filename.endswith('.png') or filename.endswith('.jpg'):
        replace_white_with_red(os.path.join(folder_path, filename))
