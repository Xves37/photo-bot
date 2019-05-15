from PIL import Image, ImageFilter


def file_saving(post):
    def decor(func):
        def wrapped(path, arg=None):
            img = Image.open(path)

            if arg:
                img = func(img, arg)
            else:
                img = func(img)

            dest = path.replace('sent', 'edited')
            dest = dest.replace('.', '-' + post + '.')

            img.save(dest)

            return dest
        return wrapped
    return decor


@file_saving(post='blur')
def blur(img):
    return img.filter(ImageFilter.BLUR)


@file_saving(post='contour')
def contour(img):
    return img.filter(ImageFilter.CONTOUR)


@file_saving(post='Gauss-blur')
def gauss_blur(img, arg=10):
    return img.filter(ImageFilter.GaussianBlur(radius=arg))
