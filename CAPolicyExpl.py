import json
from dataclasses import dataclass
import argparse

__all = "All"

def parse_list(list:list):
    if len(list) == 0:
        return None
    elif list[0].lower() == "all":
        return __all
    elif list[0].lower() == "none":
        return None
    else:
        return list

@dataclass
class User_condition:
    included: list
    excluded: list
    included_groups: list
    excluded_groups: list
    included_roles: list
    excluded_roles: list

def construct_user_conditions(conditions):
    new_user = User_condition(
        parse_list(conditions["includeUsers"]),
        parse_list(conditions["excludeUsers"]),
        parse_list(conditions["includeGroups"]),
        parse_list(conditions["excludeGroups"]),
        parse_list(conditions["includeRoles"]),
        parse_list(conditions["excludeRoles"]),
    )
    return new_user

@dataclass
class Application_condition:
    included: list
    excluded: list
    included_user_actions: list
    included_auth_context: list

def construct_app_conditions(conditions):
    new_app = Application_condition(
        parse_list(conditions["includeApplications"]),
        parse_list(conditions["excludeApplications"]),
        parse_list(conditions["includeUserActions"]),
        parse_list(conditions["includeAuthenticationContextClassReferences"])
    )
    return new_app

@dataclass
class Device_condition:
    device_filter_rule: list
    device_filter_mode: str
    include_platforms: list
    exclude_platforms: list

def construct_device_conditions(device_conditions, device_platform_conditions):
    if device_conditions == None and device_platform_conditions == None:
        return None
    new_device = Device_condition(
        None if device_conditions == None else parse_list(device_conditions["deviceFilter"]["rule"]),
        None if device_conditions == None else parse_list(device_conditions["deviceFilter"]["mode"]),
        None if device_platform_conditions == None else parse_list(device_platform_conditions["includePlatforms"]),
        None if device_platform_conditions == None else parse_list(device_platform_conditions["excludePlatforms"])
    )
    return new_device

@dataclass
class Grant_controls:
    operator: str
    controls: list
    custom_auth_factor: list
    terms_of_use: list

def construct_grant_controls(conditions):
    new_grant_controls = Grant_controls(
        conditions["operator"],
        "block" if conditions["builtInControls"][0] == "block" else conditions["builtInControls"],
        conditions["customAuthenticationFactors"],
        conditions["termsOfUse"],
    )
    return new_grant_controls


@dataclass
class Policy:
    id: str
    displayName: str
    state: str
    applications: Application_condition
    users: User_condition
    client_app_types: list
    devices: dir
    grant_controls: Grant_controls

def get_policies(filePath):
    try:
        with open(filePath, "r") as policy_file:
            return json.loads(policy_file.read())["value"]
    except FileNotFoundError:
        print(f"The file at {filePath}, do not exist")
        SystemExit()

def construct_policy(policy):
    new_policy = Policy(
        policy["id"],
        policy["displayName"],
        "reporting" if policy["state"] == "enabledForReportingButNotEnforced" else policy["state"],
        construct_app_conditions(policy["conditions"]["applications"]),
        construct_user_conditions(policy["conditions"]["users"]),
        parse_list(policy["conditions"]["clientAppTypes"]),
        construct_device_conditions(policy["conditions"]["devices"], policy["conditions"]["platforms"]),
        construct_grant_controls(policy["grantControls"]),
        
    )
    return new_policy

def parse_arguments():
    parser = argparse.ArgumentParser(prog="Azure Conditional Access Explorer")
    parser.add_argument("input_file_path", type=str)
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    policies = get_policies(args.input_file_path)
    # construct_policy(policies[0])
    # return
    policy_objs = []
    for policy in policies:
        policy_obj = construct_policy(policy)
        policy_objs.append(policy_obj)
        print(policy_obj)
        print()


if __name__ == "__main__":
    main()