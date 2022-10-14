import os
import shutil
import yaml
import logging
from tqdm import tqdm
import pandas as pd
import json

def read_yaml(path_to_yaml: str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)

    logging.info(f"yaml file : {path_to_yaml} loaded successfully")
    return content

def create_directories(path_to_directories: list) -> None:
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)

        logging.info(f"created directory at : {path}")

def copy_files(source_download_dir: str, local_data_dir: str) -> None:
    
    list_of_files = os.listdir(source_download_dir)
    N = len(list_of_files)

    for filename in tqdm(list_of_files, total=N, desc=f"copying file from {source_download_dir} to {local_data_dir}", colour="green",):
        source = os.path.join(source_download_dir, filename)
        destination = os.path.join(local_data_dir, filename)

        shutil.copy(source,destination)
    
    logging.info(f"All the files has been copied from {source_download_dir} to {local_data_dir}")


def get_timestamp(name: str) -> str:
    """create unique name with timestamp
    Args:
        name (str): name of file or directory
    Returns:
        str: unique name with timestamp
    """
    timestamp = time.asctime().replace(" ", "_").replace(":", ".")
    unique_name = f"{name}_at_{timestamp}"
    return unique_name