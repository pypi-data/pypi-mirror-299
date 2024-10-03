"""
Treat all arguments passed by the user.
"""

def treat_args(data, args) -> bool:
    '''
    Lower all user inputs an compare to lowered metadata. Evaluate the
    presence of an argument and include it in treatment

    Arguments:
    organism -- target organism name
    product -- target compound name
    biosynt -- target biosynthetic class name
    completeness -- Cluster completeness from mibig
    mininal -- annotation status from mibig
    '''

    add: bool = True

    if args.organism:
        add &= (
            args.organism.lower() in data['cluster']['organism_name'].lower()
            )
    if args.product:
        add &= args.product.lower() in [
            c.get('compound').lower() for c in data['cluster']['compounds']
            ]
    if args.biosynt:
        add &= args.biosynt.lower() in [
            b.lower() for b in data['cluster']['biosyn_class']
            ]

    add &= (
        data['cluster']['loci']['completeness'].lower()
        == args.completeness.lower()
        )
    add &= data['cluster']['minimal'] is args.minimal

    return add
