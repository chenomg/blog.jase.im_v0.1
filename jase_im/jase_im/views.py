import os
import logging

from django.http import HttpResponse

from jase_im.settings import BASE_DIR


def ssl_verify(request, code):
    logging.info('开始验证')
    file_path = os.path.join(BASE_DIR, 'challenges', code)
    file_open = open(file_path, 'rb').read()
    logging.info('file_path: {}, file_content: {}'.format(
        file_path, file_open))
    return HttpResponse(file_open)
