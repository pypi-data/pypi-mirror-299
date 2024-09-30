# The purpose of this is to traverse locations with books and spot those with likely ISBNs in the title.
# This is expected to run on the MacBookPro.


import os

from .isbn import isbn_find, isbn_find_raw

HOME = os.environ.get('HOME', os.environ.get('HOMEPATH', '~'))
DEFAULT_TREES = [
    os.path.join(HOME, 'Google Drive/Books, Papers'),
]

DEFAULT_FILES = [
    '/Volumes/Public/du_filenames.txt',
    #    'V:\\du_filenames.txt',
]

EXCLUDED_EXTS = {
    '.idx',
    '.jpg',
    '.gif',
    '.png',
}

INCLUDED_EXTS = {
    '.chm',
    '.djvu',
    '.epub',
    '.exx',
    '.htm',
    '.pdf',
}


def process_path(pn, isbns):
    _, pn_ext = os.path.splitext(pn)
    if pn_ext.lower() in EXCLUDED_EXTS:
        return

    found_isbn = isbn_find(pn) or isbn_find_raw(pn)
    if found_isbn:
        isbns[found_isbn].add(pn)
        print(found_isbn)


def process_tree(root, isbns):
    for subroot, dirs, files in os.walk(root):
        dirs.sort()
        files.sort()

        print(subroot)

        for entry in dirs + files:
            process_path(os.path.join(subroot, entry), isbns)
