"""
Curation operations in individual directories.
"""

import json
import logging
import os
from typing import Dict

from .dir_data import DirMetadata, FileMetadata

def read_dir_json(path) -> Dict:
    logging.debug('read_dir_json')
    try:
        with open(os.path.join(path, '.json'), 'r', encoding='utf-8') as f_in:
            return json.load(f_in)
    except Exception:
        return {}


def write_dir_json(path: str, dir_metadata: DirMetadata):
    """write the directory metedata as JSON

    Args:
        path (str): the path to the directory's .json file
        dir_metadata (FileMetadata): the directory metadata
    """
    logging.debug(f'write_dir_json:  {path}')
    with open(os.path.join(path, '.json'), 'w', encoding='utf-8') as f_out:
        json.dump(dir_metadata.to_json(), f_out)


def parse_json_file(content: Dict) -> DirMetadata:
    """convert whatever version this file is to the latest version.

    Args:
        content (Dict): the content of a dir .json file
    """
    result: DirMetadata = DirMetadata()
    
    if 'version' not in content:
        logging.debug('Version 0')
        
        process_files_section(content, result)
        return result
    elif isinstance(content['version'], int):
        logging.debug(f'Version {content["version"]}')
        
        if content['version'] == 1:
            process_files_section(content['files'], result)
            
        return result
            
    logging.error(f'Version is bogus: {content['version']}')  
    
def process_files_section(files:Dict, metadata: DirMetadata) -> None:
    """process the "files" section of the file

    Args:
        files (Dict): the files dict of the .json file
        result (DirMetadata): the dir metadata to add the files to
    """
    for filename, details in files.items():
        metadata.add_file(filename, FileMetadata(details))
