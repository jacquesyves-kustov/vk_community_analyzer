from .versions_schema import Versions
from .vk_users_schema import VkUsers, VkUsersGeneralData, VkUsersFollowingGroups
from .vk_groups_schema import VkUniqueGroups, VkGroupsGeneralData, VkGroupsAgeData
from .tg_users_schema import TgUsers
from .create_tables import create_database, db_session
from .data_collector import DataCollector