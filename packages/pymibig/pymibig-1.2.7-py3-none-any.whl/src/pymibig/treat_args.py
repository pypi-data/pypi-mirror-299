"""
Treat all arguments passed by the user.
"""

def treat_args(data, args) -> bool:
    '''
    Lower all user inputs an compare to lowered metadata. Evaluate the
    presence of an argument and include it in treatment

    Arguments:
    data -- MIBiG metadata from json files
    args -- object of class Args containing user inputs
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
    if args.completeness != 'all':
        add &= (
            data['cluster']['loci']['completeness'].lower()
            == args.completeness.lower()
            )
    # if all ignore this parameter
    if args.minimal  == 'maximum':
        add &= data['cluster']['minimal'] is False
    elif args.minimal == 'minimal':
        add &= data['cluster']['minimal'] is True

    return add
