#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'album_sender'

from PIL import Image
from telegram import InputMediaPhoto, InputMediaVideo, InputMediaDocument
import cached_url
import pic_cut
from telegram_util import cutCaption, isUrl, cutCaptionHtml
import os
import time

next_send_time = {}
count_by_chat_id = {}
def waitSend(chat_id, media_group_size):
    if next_send_time.get(chat_id, 0) < time.time() - 10 * 60:
        count_by_chat_id[chat_id] = 0
    count_by_chat_id[chat_id] = count_by_chat_id.get(chat_id, 0) + media_group_size + 2
    wait = next_send_time.get(chat_id, 0) + media_group_size * 10 - time.time() + min(30, count_by_chat_id[chat_id]) - 15
    next_send_time[chat_id] = time.time() + media_group_size ** 2
    if wait > 0:
        time.sleep(wait)
    
def properSize(fn):
    size = os.stat(fn).st_size
    if fn.endswith('mp4'):
        return 100 < size and size < (1 << 25)
    return 100 < size and size < (1 << 23)

def getCap(result, limit):
    if result.cap_html_v2:
        if not result.url:
            return cutCaptionHtml(result.cap_html_v2, limit)
        return (cutCaptionHtml(result.cap_html_v2, limit) + 
            ' <a href="%s">source</a>' % result.url).strip()
    if result.getParseMode() == 'HTML':
        # currently, the only use case is repost the telegram post
        # later on, this part might need expansion
        return result.cap_html
    if result.url:
        suffix = '[source](%s)' % result.url
    else:
        suffix = ''
    return cutCaption(result.cap, suffix, limit)

def sendVideo(chat, result):
    if 'doubanio.com' in result.video:
        cached_url.get(result.video, mode='b', headers={'referer': 'https://www.douban.com/'}, force_cache = True)
        content = open(cached_url.getFilePath(result.video), 'rb')
    else:
        content = result.video
    group = [InputMediaVideo(content, 
        caption=getCap(result, 1000), parse_mode=result.getParseMode())]
    return chat.bot.send_media_group(chat.id, group, timeout = 20*60)

def imgRotate(img_path, rotate):
    if img_path.endswith('mp4'):
        return
    if not rotate:
        return
    if rotate == True:
        rotate = 180
    img = Image.open(img_path)
    img = img.rotate(rotate, expand=True)
    img.save(img_path)

def getMedia(fn, result = None, original_file=False):
    # see if animated gif still work or not
    if pic_cut.isAnimated(fn):
        tag = InputMediaVideo
    else:
        tag = InputMediaPhoto
    if original_file:
        tag = InputMediaDocument
    return tag(open(fn, 'rb'), 
        caption=result and getCap(result, 1000),
        parse_mode=result and result.getParseMode())

def getMediaGroup(imgs, result, original_file=False):
    return [getMedia(imgs[0], result = result, original_file=original_file)] + [getMedia(img, original_file=original_file) for img in imgs[1:]]

def getImage(img):
    cached_url.get(img, force_cache=True, mode='b')
    return cached_url.getFilePath(img)

def prepareCache(img):
    if '.sinaimg.cn' in img:
        cached_url.get(img, mode='b', headers={'referer': 'https://m.weibo.cn/'}, force_cache = True)
        
def send_v2_imp(chat, result, rotate=0, send_all=False, no_cut=False, size_factor = None, rotate_detail = {}, start_page = 0, original_file=False):
    # may need to revisit this line
    if (not result.video) and len(result.imgs) == 1 and result.imgs[0].endswith('mp4'):
        result.video = result.imgs[0]
    if result.video:
        return sendVideo(chat, result)

    img_limit = start_page * 10 + (100 if send_all else 10)
    [prepareCache(img) for img in result.imgs]
    if no_cut:
        imgs = [getImage(img) for img in result.imgs]
    else:
        args = {}
        if size_factor:
            args['size_factor'] = size_factor
        imgs = pic_cut.getCutImages(result.imgs, img_limit, **args) 
    imgs = [x for x in imgs if properSize(x)]
    [imgRotate(x, rotate) for x in imgs]
    for index, rotate_single in rotate_detail.items():
        imgRotate(imgs[index], rotate_single)
    imgs = imgs[start_page * 10:]
    
    if imgs:
        return_result = []
        for page in range(1 + int((len(imgs) - 1) / 10)):
            group = getMediaGroup(imgs[page * 10: page * 10 + 10], result, original_file=original_file)
            waitSend(chat.id, len(group))
            return_result += chat.bot.send_media_group(chat.id, group, timeout = 20*60)
        return return_result

    if result.cap or result.cap_html or result.cap_html_v2:
        waitSend(chat.id, 1)
        return [chat.send_message(getCap(result, 4000), 
            parse_mode=result.getParseMode(), timeout = 20*60, 
            disable_web_page_preview = (not isUrl(result.cap) and not isUrl(result.cap_html_v2)))]

def send_v2(chat, result, rotate=0, send_all=False, no_cut=False, size_factor = None, rotate_detail = {}, start_page=0, original_file=False):
    args = {'rotate': rotate, 'send_all': send_all, 'no_cut': no_cut, 
      'size_factor': size_factor, 'rotate_detail': rotate_detail, 
      'start_page': start_page, 'original_file': original_file}
    encoutered_errors = set()
    while True:
        try:
            return send_v2_imp(chat, result, **args)
        except Exception as e:
            if str(e) in encoutered_errors:
                raise e
            if len(encoutered_errors) > 5:
                raise e
            encoutered_errors.add(str(e))
            if 'Timed out' in str(e):
                return []
            if str(e).endswith('seconds'):
                wait = int(str(e).split()[-2])
                time.sleep(wait + 5)
                continue
            if "an't parse entities" in str(e):
                result.no_parse = True
                continue
            raise e

def send(chat, url, result, rotate=0, send_all=False):
    result.url = url
    send_v2(chat, result, rotate=rotate, send_all=send_all)