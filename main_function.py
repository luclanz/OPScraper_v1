import requests
import shutil
import webbrowser
import os
import zipfile
from PIL import Image
import img2pdf


def download_images(base_url, chapter, download_path, ext, page):
    from urllib.request import urlopen, Request
    import urllib

    i = page
    while True:
        # create the url of the chapter
        image_url = base_url + "/" + str(chapter) + "/" + str(i) + str(ext)
        # split the last part of the string before "/", getting the name of the image
        # filename = image_url.split("/")[-1]
        filename = str(i).zfill(2) + str(ext)
        # Open the url image, set stream to True, this will return the stream content.

        try:
            request = Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(request)

        except urllib.error.HTTPError as e:
            if e.code == 404:
                if i < 10:
                    print("Try Chapter " + str(chapter) + " with different format")
                    if str(ext) == ".jpg":
                        download_images(base_url, chapter, download_path, '.png', i)
                    else:
                        download_images(base_url, chapter, download_path, '.jpg', i)
                    return
                else:
                    print("chapter " + str(chapter) + " has " + str(i - 1) + " pages")
                    return
            raise print("UNKNOWN ERROR ON CHAPTER " + str(chapter))

        r = response.read()
        print(str(chapter) + ": image " + str(i) + " downloaded")

        with open(download_path + '/' + filename, "wb") as f:
            f.write(r)

        i = i + 1


def make_pdf(chapter, download_path):
    image_list = os.listdir(download_path)
    image_list.sort()
    with open(download_path + '/' + str(chapter) + '.pdf', 'wb') as f:
        f.write(img2pdf.convert([(download_path + '/' + i) for i in image_list
                                 if i.endswith('.jpg')]))

    delete_junk(chapter, download_path, '.jpg')
    return print('CHAPTER ' + str(chapter) + ' -> PDF COMPLETED')


def png2jpg(download_path, chapter):
    # loop to convert files to jpg
    file_list = os.listdir(download_path)
    for i in file_list:
        if i.endswith('.png'):
            im = Image.open(download_path + '/' + i)
            rgb_im = im.convert('RGB')
            new_name = os.path.splitext(i)[0]
            rgb_im.save(download_path + '/' + new_name + '.jpg')
    # loop to delete older png files
    print('Chapter ' + str(chapter) + ' -> Fully converted to jpg, ')
    j = 0
    file_list = os.listdir(download_path)
    for i in file_list:
        if i.endswith('.png'):
            os.remove(download_path + '/' + i)
            j += 1
    print('Chapter ' + str(chapter) + ' -> Fully removed ' + str(j) + ' older file(s)')


def delete_junk(chapter, download_path, ext):
    j = 0
    file_list = os.listdir(download_path)
    for i in file_list:
        if i.endswith(str(ext)):
            os.remove(download_path + '/' + i)
            j += 1
    print('Chapter ' + str(chapter) + ' -> temp ' + str(j) + ' image(s) removed')