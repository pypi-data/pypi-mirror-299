"""
Save target's BGCs access codes.
"""

import sys
import json
import tarfile
from itertools import islice
from rich.progress import track
from src.pymibig.console import console
from src.pymibig.treat_args import treat_args
from src.pymibig.constants import METADATA

def save_access_codes(args, basedir) -> list:
    '''
    Create a txt file listing BGCs codes

    Arguments:
    organism -- target taxon name
    basedir -- main module path
    completeness -- Cluster completeness from mibig
    mininal -- annotation status from mibig
    '''
    access_codes: list = []

    try:
        with tarfile.open(f'{basedir}/src/db/{METADATA}') as tar:
            for member in track(islice(tar, 1, None),
            description='[bold green]Searching target access '
                        'codes...[/bold green]',
            total=len(tar.getmembers())-1):
                with tar.extractfile(member) as handle:
                    data = json.load(handle)
                if treat_args(data, args):
                    access_codes.append(data['cluster']['mibig_accession'])
        if not access_codes:
            console.print('[bold yellow]Your search had no '
                          'match[/bold yellow]')
            sys.exit()
        with open(
            f'{args.create_prefix}_codes.txt', 'wt',
            encoding='utf-8'
            ) as  codes:
            codes.write('\n'.join(str(i) for i in access_codes))
        return access_codes
    except PermissionError:
        console.print(
            '[bold red]Permission to read directory or write '
            'file denied.[/bold red]'
            )
        sys.exit()
    except FileNotFoundError:
        console.print(f'[bold red]{tar.name} not found.[/bold red]')
        sys.exit()
