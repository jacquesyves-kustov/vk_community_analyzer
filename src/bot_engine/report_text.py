class ReportTextGenerator:
    @staticmethod
    def get_correctness_assessment(
        total_members,
        total_members_in_json,
        total_men,
        total_women,
        total_men_with_age,
        total_women_with_age,
    ) -> str:
        """
        Оценка репрезентативности получаемых данных

        "ДОВЕРЯТЬ" / "ДОВЕРЯТЬ, НО ПРОВЕРЯТЬ" / "НЕ ДОВЕРЯТЬ"

        ВСЕГО ПОДПИСЧИКОВ: 53188
        ВСЕГО ПОДПИСЧИКОВ В JSON: 52492, (98.69%)

        ВСЕГО МУЖ.: 32625 (62.15%)
        ВСЕГО ЖЕН.: 19866 (37.85%)

        ВСЕГО ПОДПИСЧИКОВ С ВОЗРАСТОМ: 23760 (45.26%)
        ВСЕГО МУЖ. С ВОЗРАСТОМ: 15614 (65.72%)
        ВСЕГО ЖЕН. С ВОЗРАСТОМ: 8146 (34.28%)

        """

        GREAT = "ДОВЕРЯТЬ!"  # Зеленый
        NOT_SURE = "ДОВЕРЯТЬ, НО ПРОВЕРЯТЬ!"  # Коричневый
        BAD = "НЕ ДОВЕРЯТЬ!"  # Красный

        # Если в JSON представляется малая часть от всех подписчиков (менее 70%)
        if total_members_in_json / (total_members / 100) < 70:
            return BAD

    @staticmethod
    def get_report_text():
        pass
