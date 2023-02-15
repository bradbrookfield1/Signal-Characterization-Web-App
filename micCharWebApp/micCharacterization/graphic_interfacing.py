import base64, os
from io import BytesIO
from matplotlib import pyplot as plt

def file_path_to_img(file_path):
    if file_path == None:
        return None
    img = open(file_path, 'rb').read()
    img = base64.b64encode(img)
    return img.decode('utf-8')

def get_graph(temp_spec, attr, mic_Data_Record):
    full_name = 'Uploads/' + temp_spec + '/' + attr + '/' + attr + '_' + str(mic_Data_Record.pk) + '.png'
    if os.path.exists(full_name):
        os.remove(full_name)
    plt.savefig(full_name)
    return full_name

def get_abs_coeff_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    buffer.close()
    return graph.decode('utf-8')