def compter_candidats(df):
    """
    [Question 2] 
    Compte le nombre de candidats à l'élection présidentielle 2022
    en excluant les bulletins blancs, nuls et abstentions.

    Paramètre
    ----------
    df : pandas.DataFrame
        DataFrame contenant les données électorales

    Retour
    ------
    str : phrase type avec le nombre de candidats
    """
    mask_exprimes = ~df["nom"].str.contains("BLANC|NUL|ABSTENTION", case=False, na=False)
    df_exprimes = df[mask_exprimes]

    candidats = df_exprimes["candidat"].nunique()

    return f"En 2022, il y avait {candidats} candidats à l'élection présidentielle."


