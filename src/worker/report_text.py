from enum import Enum


class ReportContent(Enum):
    NAME = "Группа: {} \n"
    LINK = "Ссылка: https://vk.com/{} \n"
    TOTAL_MEMBERS_NUMS = "Всего подписчиков: {}, из них обработано {}. Мужчины - {} ({}%), женщины - {} ({}%). \n"
    PROCESSED_MEMBERS_NUMS = "Подписчиков с полным возрастом: {}. Из них мужчины - {} ({}%), женщины - {} ({}%). \n"
    ASSESSMENT = "Оценка репрезентативности обработанных данных: {} \n"
    ERROR = "Группы {} не существует =("
    GREAT = "Прекрасно - доверять! :)"
    NOT_SURE = "Нормально."
    BAD = "Плохо - не доверять :("


class ReportGenerator:
    @staticmethod
    def get_correctness_assessment(
        total_members,
        total_members_in_json,
        total_men,
        total_women,
        total_men_with_age,
        total_women_with_age,
    ) -> str:
        shift = 0.15

        # Если в JSON представляется малая часть от всех подписчиков (менее 70%)
        if total_members_in_json / (total_members / 100) < 70:
            return ReportContent.BAD.value

        return (
            ReportContent.GREAT.value
            if (total_men_with_age / total_women_with_age) - shift
            <= (total_men / total_women)
            <= (total_men_with_age / total_women_with_age) + shift
            else ReportContent.NOT_SURE.value
        )

    @classmethod
    def get_report_text(cls, group_data: dict) -> str:
        """
        "title", "screen_name", "actual_members_count", "processed_members_count", "total_men": , "total_women":
        "all_ages_dict": , "men_ages_dict": , "women_ages_dict": , "total_men_with_ages": ,"total_women_with_ages":

        :param group_data:
        :return:
        """
        report = "*" + ReportContent.NAME.value.format(group_data["title"]) + "*"

        if not "_" in group_data["screen_name"]:
            report += ReportContent.LINK.value.format(group_data["screen_name"])

        report += "\n"

        report += ReportContent.TOTAL_MEMBERS_NUMS.value.format(
            group_data["actual_members_count"],
            group_data["processed_members_count"],
            group_data["total_men"],
            round(
                group_data["total_men"] / (group_data["processed_members_count"] / 100),
                2,
            ),
            group_data["total_women"],
            round(
                group_data["total_women"]
                / (group_data["processed_members_count"] / 100),
                2,
            ),
        )

        report += "\n"

        report += ReportContent.PROCESSED_MEMBERS_NUMS.value.format(
            group_data["total_users_with_age"],
            group_data["total_men_with_ages"],
            round(
                group_data["total_men_with_ages"]
                / (group_data["total_users_with_age"] / 100),
                2,
            ),
            group_data["total_women_with_ages"],
            round(
                group_data["total_women_with_ages"]
                / (group_data["total_users_with_age"] / 100),
                2,
            ),
        )

        report += ReportContent.ASSESSMENT.value.format(
            cls.get_correctness_assessment(
                group_data["actual_members_count"],
                group_data["processed_members_count"],
                group_data["total_men"],
                group_data["total_women"],
                group_data["total_men_with_ages"],
                group_data["total_women_with_ages"],
            )
        )

        return report

    @staticmethod
    def get_error_message(group_screen_name: str) -> str:
        cursed_link = "https://vk.com/" + group_screen_name
        return ReportContent.ERROR.value.format(cursed_link)
