from clients import VkApiClient


def get_related_publics(public_short_name: str):
    # Get list of members dict
    test_users = VkApiClient.get_total_members_list(public_short_name)

    # Collect data on their subs
    found_groups = dict()
    for user in test_users:
        r = VkApiClient.send_get_request(VkApiClient.VK_USERS_GET_SUBS, user_id=user['true_user_id'])
        r = r.json()
        print(r)

        if 'error' in r:
            continue

        for group_id in r['response']['groups']['items']:
            found_groups[group_id] = found_groups.setdefault(group_id, 0) + 1

    # Sorted by value
    found_groups = dict(sorted(found_groups.items(), key=lambda item: item[1]))

    return found_groups
