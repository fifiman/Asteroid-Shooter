
def generate_levels():
    """
    Generates level score limits.
    10, 30, 60, 100, 150, ...
    """
    level = 0
    delta = 1

    while 1:
        level += delta
        yield level

        delta += 1


if __name__ == '__main__':

    gen = generate_levels()
    num = next(gen)
    print num
