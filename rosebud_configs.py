import configparser, os, sys, copy

elid = "181057933654622208"
wishid = "304080356900995092"
roseid = "464161516212715530"

trans = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xFFFD)

# TODO create more catregories for settings (money etc)
def get_config(category):
    cfg = configparser.ConfigParser(
        {
            "prefix": ",,",
            "home_dir": os.path.dirname(os.path.abspath(__file__)) + "/resources",
            "suppress_loading_messages": "0",
            "token": "CHANGEME",
            "main_server_id": "425046326275866626",
            "entry_channel_id": "425057127632207902",
            "money_high": "15",
            "money_low": "10",
        }
    )

    if not os.path.isfile(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.cfg")
    ):
        with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.cfg"), "w"
        ) as f:
            cfg.write(f)

    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.cfg"), "r"
    ) as f:
        cfg.read_file(f)

    return cfg[category]


class settings:
    """
    Formalized container class for grabbing settings regardless of category

    Redundant, but useful when we scale Rosebud
    """

    # defaults
    cfg_default = dict(get_config("DEFAULT"))
    suppress_loading_messages = int(cfg_default["suppress_loading_messages"])
    home_dir = cfg_default["home_dir"]
    token = cfg_default["token"]
    money_range = (int(cfg_default["money_low"]), int(cfg_default["money_high"]))
    prefix = cfg_default["prefix"]

    # all vals
    setting = copy.deepcopy(cfg_default)
