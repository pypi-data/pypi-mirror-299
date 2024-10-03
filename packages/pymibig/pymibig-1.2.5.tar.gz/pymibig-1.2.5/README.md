# pyMIBiG

A small tool to download, match and save sequences from [MIBiG](https://mibig.secondarymetabolites.org/).

`pyMIBiG` can search by "organism name", "compound / product" and / or
"biosynthetic class" as intersections of every argument added. Which means
that the more arguments you add more restrictive your search becomes.
It uses the available MIBiG download files which have less information then
those returned when using their web search. So, for very specific queries,
that yield fewer results, you will be better using the web interface.

## Usage

Download the available package of `pyMIBiG` and execute `pymibig -<target>`
where target is the term you wanto to search in MIBiG database.

By default `pyMIBiG` will fetch sequences with complete cluster data and
complete information of a given taxon.

You may change that using optional aguments passed along with the `<target>`:

```{bash}
usage: pyMIBiG [-h] [-o ORGANISM] [-p PRODUCT] [-b BIOSYNT] [-c {complete,incomplete,unknown}] [-m]

A small tool to download, match and save taxon sequences from MIBiG.

options:
  -h, --help            show this help message and exit
  -o ORGANISM, --organism ORGANISM
                        Organism name to query in database.
  -p PRODUCT, --product PRODUCT
                        Compound to query in database.
  -b BIOSYNT, --biosynt BIOSYNT
                        Biosynthetic class to query in database.
  -c {complete,incomplete,unknown}, --completeness {complete,incomplete,unknown}
                        Loci completeness.
  -m, --minimal         Minimal annotation.
```

You have to use at least one of the following arguments: organism, product or
biosynt. The others are optional.

On first execution `pyMIBiG` will download the database files from
[MIBiG](https://mibig.secondarymetabolites.org/download) and save locally,
so an internet connection will be needed, after that it can be used offline.

As for this release `pyMIBiG` will download from MIBiG
**Version 3.1 (October 7th, 2022)** the:
- [Metadata](https://dl.secondarymetabolites.org/mibig/mibig_json_3.1.tar.gz)
in compressed format, including several JSON files;
- [Nucleotide](https://dl.secondarymetabolites.org/mibig/mibig_gbk_3.1.tar.gz)
sequences of the biosynthetic gene clusters in compressed format, including
several GBK files;
- [Amino acid sequence translations](https://dl.secondarymetabolites.org/mibig/mibig_prot_seqs_3.1.fasta)
of all genes from MIBiG entries are also available in a single compressed
FASTa file.

## License

`pyMiBiG` is distributed under the terms of the [LGPL 3.0](https://spdx.org/licenses/LGPL-3.0-or-later.html) license.
