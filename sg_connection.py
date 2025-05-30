"""sg_connection.py

This module defines a reusable ShotGridConnector class that establishes a
connection to the LAIKA ShotGrid demo site using the Shotgun Python API. The
connection is shared for use across other modules in the project.

Example usage:
    from sg_connection import ShotGridConnector

    sg = ShotGridConnector().get_connection()
    project = sg.find_one("Project", [["id", "is", 85]], ["name"])
    print(project["name"])
"""

from shotgun_api3 import Shotgun


class ShotGridConnector:
    """
    Handles authentication and connection to the ShotGrid API.

    Attributes:
        site_url (str): The ShotGrid server URL.
        script_name (str): The name of the API script.
        api_key (str): The API key associated with the script.
        connection (Shotgun): The authenticated Shotgun connection object.
    """

    def __init__(self):
        """
        Initializes the ShotGridConnector with predefined credentials
        for the LAIKA demo ShotGrid instance.
        """
        self.site_url = "https://laika-demo.shotgunstudio.com"
        self.script_name = "code_challenge"
        self.api_key = "2Drsqmdcfhjvfcv%kvxdaqvft"
        self.connection = None

    def get_connection(self):
        """
        Returns a Shotgun connection object. Initializes the connection if not
        already done.

        Returns:
            Shotgun: An authenticated Shotgun API object.
        """
        if self.connection is None:
            self.connection = Shotgun(
                self.site_url,
                script_name=self.script_name,
                api_key=self.api_key,
                connect=True,
                http_proxy=None,
            )
        return self.connection
