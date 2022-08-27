from json import loads

from sqlalchemy.orm import Session

from storage.vk_groups_schema import VkGroupsAgeData, VkGroupsGeneralData


class DataSender:
    @staticmethod
    def get_groups_data(short_name: str, session: Session) -> dict:
        q = (
            session.query(VkGroupsGeneralData, VkGroupsAgeData)
            .join(VkGroupsAgeData)
            .filter(VkGroupsGeneralData.screen_name == short_name)
            .first()
        )

        res_d = dict()

        if q is None:
            res_d["error"] = "error"
            return res_d

        res_d["title"] = q[0].title
        res_d["screen_name"] = q[0].screen_name
        res_d["actual_members_count"] = q[0].actual_members_count
        res_d["processed_members_count"] = q[0].processed_members_count
        res_d["total_men"] = q[0].total_men
        res_d["total_women"] = q[0].total_women
        res_d["all_ages_dict"] = loads(q[1].all_ages_dict.replace("'", '"'))
        res_d["men_ages_dict"] = loads(q[1].men_ages_dict.replace("'", '"'))
        res_d["women_ages_dict"] = loads(q[1].women_ages_dict.replace("'", '"'))
        res_d["total_men_with_ages"] = q[1].total_men_with_ages
        res_d["total_women_with_ages"] = q[1].total_women_with_ages

        return res_d
