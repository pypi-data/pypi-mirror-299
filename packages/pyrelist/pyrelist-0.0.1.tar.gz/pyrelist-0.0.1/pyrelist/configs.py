"""
All configurations for pyrelist
"""
from pytconf import Config, ParamCreator


class ConfigNada(Config):
    """
    Dont know what this is for
    """
    folder = ParamCreator.create_existing_folder(
        help_string="Which folder to work on?",
    )
