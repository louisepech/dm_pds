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
    condition = "nom != 'Blancs' and nom != 'Nuls' and nom != 'Abstentions'"
    
    df_exprimes = df.query(condition)
    
    candidats = df_exprimes["candidat"].nunique()

    return f"En 2022, il y avait {candidats} candidats à l'élection présidentielle."


def scores_nationaux_2(df):
    """
    [Question 3]
    Calcule le nombre de voix et le score (%) national par candidat
    (en excluant les votes blancs, nuls, et abstentions)
    """

    df = df.copy()
    df["nom"] = df["nom"].fillna("")
    df["voix"] = pd.to_numeric(df["voix"], errors="coerce").fillna(0)

    votes_exprimes = ~df["nom"].str.contains("BLANC|NUL|ABSTENTION", case=False, na=False)
    df_exprimes = df[votes_exprimes]

    res = (
        df_exprimes
        .groupby("candidat", as_index=False)["voix"]
        .sum()
        .rename(columns={"voix": "votes"})
    )

    total = res["votes"].sum()

    res["score"] = (res["votes"] / total * 100 ).round(2).astype(str) + "%"

    res = res.sort_values(by="votes", ascending=False)

    res = res.rename(columns={
    "candidat": "Candidat",
    "votes": "Nombre de votes (total)",
    "score": "Score (% votes exprimés)"
})
    return res



def scores_departements(df):
    """
    [Question 4 ]
    Calcule les scores (%) aux présidentielles par département et candidat
    """

    df = df.copy()
    df["nom"] = df["nom"].fillna("")
    df["voix"] = pd.to_numeric(df["voix"], errors="coerce").fillna(0)

    mask_exprimes = ~df["nom"].str.contains("BLANC|NUL|ABSTENTION", case=False, na=False)
    df_exprimes = df[mask_exprimes]

    res = (
        df_exprimes
        .groupby(["code_departement", "candidat"], as_index=False)["voix"]
        .sum()
        .rename(columns={"voix": "votes"})
    )

    total_dep = res.groupby("code_departement")["votes"].transform("sum")

    res["score"] = (res["votes"] / total_dep * 100).round(2).astype(str) + "%"

    res = res.sort_values(by=["code_departement", "votes"], ascending=[True, False])

    return res


def comparaison_nationale(df):
    """
    [Question 5]
    Ajoute les scores nationaux aux scores départementaux
    """

    national = scores_nationaux_2(df).rename(
        columns={"votes": "votes_national", "score": "score_national"}
    )
    
    dep = scores_departements(df).rename(
        columns={"votes": "votes_departement", "score": "score_departement"}
    )

    res = dep.merge(national, on="candidat", how="left")

    return res


def comparaison_departement(df, code_dep):
    """
    [question 5 verif]
    Compare les scores départementaux et nationaux pour un département donné
    """

    df_comp = comparaison_nationale(df).copy()
    
    df_dep = df_comp[df_comp["code_departement"] == str(code_dep)]

    df_dep = df_dep.sort_values(by="votes_departement", ascending=False)

    df_dep = df_dep.rename(columns={
        "code_departement": "Département",
        "candidats": "Candidat",
        "votes_departement": "Votes (dep)",
        "score_departement": "Score dep (%)",
        "votes_national": "Votes (national)",
        "score_national_2": "Score national (%)"
    })

    return df_dep