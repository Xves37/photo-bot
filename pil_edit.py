from PIL import Image, ImageFilter


def file_saving(post):
    def decor(func):
        def wrapped(path, arg=None):
            img = Image.open(path)

            if arg is not None:
                img = func(img, arg)
            else:
                img = func(img)

            dest = path.replace('sent', 'edited')

            if arg is not None:
                dest = dest.replace('.', '-{post}-{arg}.'.format(post=post, arg=arg))
            else:
                dest = dest.replace('.', '-{post}.'.format(post=post))

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


@file_saving(post='smooth')
def smooth(img):
    return img.filter(ImageFilter.SMOOTH)


@file_saving(post='sharpen')
def sharpen(img):
    return img.filter(ImageFilter.SHARPEN)


@file_saving(post='Gauss-blur')
def gauss_blur(img, arg=10):
    arg = float(arg)
    return img.filter(ImageFilter.GaussianBlur(radius=arg))


@file_saving(post='rotate')
def rotate(img, arg=90):
    arg = float(arg)
    return img.rotate(arg)


if __name__ == '__main__':
    help(ImageFilter)