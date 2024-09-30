"""
Data Structures for curation of a single directory
"""

from collections import defaultdict
from typing import Any, Dict, List

CURRENT_VERSION: int = 1

class FileMetadata:
        
    def __init__(self, json_data: Dict[str, Any]) -> None:
        """a representation of the metadata for a file, from json

        Args:
            json_data (Dict[str, Any]): a JSON dict with the data in it
        """
        self.date: float = json_data.get('date', 0.0)
        self.sha256: str = json_data.get('sha256', "")
        self.size: int = json_data.get('int', 0)

    def to_json(self) -> Dict[str, Any]:
        """return a json-suitable representation of a file's metadata
        
            Returns:
                dict: with the metadata
        """
        return {
            'date': self.date,
            'sha256': self.sha256,
            'size': self.size,
        }
        
class DirMetadata:
    def __init__(self) -> None:
        # files[filename] = FileMetadata
        self.files: Dict[str, FileMetadata] = {}
        
        # groups of files with the same size/hash
        self.groups: Dict[str, List[str]] = defaultdict(list)
        
    def to_json(self) -> Dict:
        """return a json-suitable representation of the directory
        
            Returns:
                dict: with the metadata
        """
        return {
            'version': CURRENT_VERSION,
            'files': {
                filename: metadata.to_json()
                for filename, metadata in sorted(self.files.items(), key=lambda x: x[0])
            },
        }
        
    def add_file(self, filename: str, metadata: FileMetadata) -> None:
        """add information for a single file in the directory

        Args:
            filename (str): the filename
            metadata (FileMetadata): the file's metadata
        """

        self.files[filename] = metadata
        
        group: str = f'{metadata.sha256}_{metadata.size}'
        self.groups[group].append(filename)
