import os
from typing import TextIO

from core.config import settings


def main() -> None:
    home: str = os.path.expanduser("~")
    aws_folder: str = f"{home}/.aws"
    if not os.path.exists(aws_folder):
        os.mkdir(aws_folder)

    credentials_file: TextIO = open(f"{aws_folder}/credentials", "w")
    secret_key_id: str = f"aws_access_key_id = {settings.AWS_ACCESS_KEY_ID}\n"
    secret_access_key: str = f"aws_secret_access_key = {settings.AWS_SECRET_ACCESS_KEY}\n"
    credentials_file.write(f"[default]\n{secret_key_id}{secret_access_key}")
    credentials_file.close()

    config_file: TextIO = open(f"{aws_folder}/config", "w")
    default_region: str = f"region = {settings.AWS_REGION}\n"
    config_file.write(f"[default]\n{default_region}")
    config_file.close()


if __name__ == "__main__":
    main()
