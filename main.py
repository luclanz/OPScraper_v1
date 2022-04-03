import main_function

# https://img.mghubcdn.com/file/imghub/one-piece-colored/1/1.jpg

# insert first and last chapter to download
first = 909
last = 909
# insert download path
path = '/Users/Luca/Downloads/'

for i in range(int(first), int(last) + 1):
    main_function.download_images('https://img.mghubcdn.com/file/imghub/one-piece-colored',i, path, '.jpg', 1)
    main_function.png2jpg(path, i)
    main_function.make_pdf(i, '/Users/Luca/Downloads/')

