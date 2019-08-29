import os
import logging

from django.http import HttpResponse

from jase_im.settings import BASE_DIR


def ssl_verify(request, code):
    logging.info('ssl开始验证')
    file_path = os.path.join(BASE_DIR, 'ssl_verify', 'challenges', code)
    file_open = ""
    with open(file_path, 'w') as f:
        f.write(code)
        file_open = open(file_path, 'rb').read()
    logging.info('file_path: {}, file_content: {}'.format(
        file_path, file_open))
    return HttpResponse(file_open)
