import matplotlib.pyplot as plt


class PlotsGenerator:
    WIDTH = 17
    HEIGHT = 10

    @classmethod
    def visualization1(cls, x: list, y: list, title: str):
        plt.figure(figsize=(cls.WIDTH, cls.HEIGHT))
        plt.bar(x, y)
        plt.title(title)
        plt.grid(True)
        plt.show()
