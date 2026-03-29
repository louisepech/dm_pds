import pandas as pd

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


def scores_nationaux(df):
    """
    [Question 3]
    Calcule les scores nationaux des candidats en excluant les votes non exprimés
    (blanc, nul, abstention).

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
        Tableau trié des candidats avec le nombre de voix et leur score (%)
    """

    df = df.copy()

    vote_exclusion = ["BLANCS", "NULS", "ABSTENTIONS"]

    mask_non_exprimes = df["candidat"].astype(str).str.lower().isin(vote_exclusion)

    df_exprimes = df[~mask_non_exprimes]

    result = (
        df_exprimes.groupby("candidat", as_index=False)["voix"]
        .sum()
        .rename(columns={"voix": "nombre_vote"})
    )

    total_exprimes = result["nombre_vote"].sum()

    result["score_%"] = (result["nombre_vote"] / total_exprimes) * 100

    result = result.sort_values("score_%", ascending=False).reset_index(drop=True)

    return result