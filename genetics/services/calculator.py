DOMINANT = 'DOMINANT'
RECESSIVE = 'RECESSIVE'
CODOMINANT = 'CODOMINANT'


def predict_offspring(genes_a, genes_b):
    """Predict morph probability from parent gene lists.

    genes_a/genes_b: list of dicts {gene_name, inheritance_type, genotype}
    Returns dict morph_label -> probability (0-1).
    """
    if not genes_a and not genes_b:
        return {'Normal': 1.0}

    results = {}
    for ga in genes_a or [{'gene_name': 'Normal', 'inheritance_type': RECESSIVE, 'genotype': 'HOM'}]:
        for gb in genes_b or [{'gene_name': 'Normal', 'inheritance_type': RECESSIVE, 'genotype': 'HOM'}]:
            label = _combine(ga, gb)
            results[label] = results.get(label, 0) + 1.0

    total = sum(results.values())
    return {k: round(v / total, 2) for k, v in results.items()}


def _combine(ga, gb):
    it = ga.get('inheritance_type', RECESSIVE)
    if it == RECESSIVE:
        if ga.get('genotype') == 'HOM' or gb.get('genotype') == 'HOM':
            return ga['gene_name']
        if ga.get('genotype') == 'HET' and gb.get('genotype') == 'HET':
            return f"{ga['gene_name']} (66% het)"
        return 'Normal'
    if it == CODOMINANT:
        return f"{ga['gene_name']} × {gb['gene_name']}"
    return ga['gene_name']
