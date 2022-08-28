import matplotlib.pyplot as plt


class PlotsGenerator:
    WIDTH = 10
    HEIGHT = 7

    @classmethod
    def two_plots_in_one(
        cls, title: str, men_data_d: dict, women_data_d: dict, user_id: str
    ):
        plt.figure(figsize=(cls.WIDTH, cls.HEIGHT))

        plt.plot(
            men_data_d.keys(), men_data_d.values(), color="tab:blue", label="Мужчины"
        )
        plt.plot(
            women_data_d.keys(),
            women_data_d.values(),
            color="tab:orange",
            label="Женщины",
        )

        plt.xlabel("Возраст")
        plt.ylabel("Число людей")
        plt.title(f"Аудитория {title}")

        plt.legend()
        plt.grid(True)

        # plt.show()
        plt.savefig(f"{user_id}-plot.png", bbox_inches="tight")
        return f"{user_id}-plot.png"
