import pandas as pd
from matplotlib import pyplot as plt


def antall_foringer(df):
    return sum(df.loc[:, 'NForingNE']) + sum(df.loc[:, 'NForingSW'])


def antall_motspill(df):
    return sum(df.loc[:, 'NMotspillNE']) + sum(df.loc[:, 'NMotspillSW'])


def antall_spill(df):
    return antall_foringer(df) + antall_motspill(df)


def get_andel_foringer(df):
    return antall_foringer(df) * 100 / antall_spill(df)


def get_andel_motspill(df):
    return antall_motspill(df) * 100 / antall_spill(df)


def get_score_foring_ne(df):
    scores, antall, ant_par = df.loc[:, 'ForingNE'], df.loc[:, 'NForingNE'], df.loc[:, 'AntallPar']
    s = 0
    for i in range(0, len(scores)):
        if antall[i] > 0:
            s += (((scores[i] / antall[i]) + get_middel(ant_par[i])) / (get_middel(ant_par[i]) * 2) * 100) * antall[i]
    return s / sum(df.loc[:, 'NForingNE'])


def get_score_foring_sw(df):
    scores, antall, ant_par = df.loc[:, 'ForingSW'], df.loc[:, 'NForingSW'], df.loc[:, 'AntallPar']
    s = 0
    for i in range(0, len(scores)):
        if antall[i] > 0:
            s += (((scores[i] / antall[i]) + get_middel(ant_par[i])) / (get_middel(ant_par[i]) * 2) * 100) * antall[i]
    return s / sum(df.loc[:, 'NForingSW'])


def get_score_motspill_ne(df):
    scores, antall, ant_par = df.loc[:, 'MotspillNE'], df.loc[:, 'NMotspillNE'], df.loc[:, 'AntallPar']
    s = 0
    for i in range(0, len(scores)):
        if antall[i] > 0:
            s += (((scores[i] / antall[i]) + get_middel(ant_par[i])) / (get_middel(ant_par[i]) * 2) * 100) * antall[i]
    return s / sum(df.loc[:, 'NMotspillNE'])


def get_score_motspill_sw(df):
    scores, antall, ant_par = df.loc[:, 'MotspillSW'], df.loc[:, 'NMotspillSW'], df.loc[:, 'AntallPar']
    s = 0
    for i in range(0, len(scores)):
        if antall[i] > 0:
            s += (((scores[i] / antall[i]) + get_middel(ant_par[i])) / (get_middel(ant_par[i]) * 2) * 100) * antall[i]
    return s / sum(df.loc[:, 'NMotspillSW'])


def get_score_motspill(df):
    sw = get_score_motspill_sw(df) * sum(df.loc[:, 'NMotspillSW'])
    ne = get_score_motspill_ne(df) * sum(df.loc[:, 'NMotspillNE'])
    return (sw + ne) / antall_motspill(df)


def get_score_foring(df):
    sw = get_score_foring_sw(df) * sum(df.loc[:, 'NForingSW'])
    ne = get_score_foring_ne(df) * sum(df.loc[:, 'NForingNE'])
    return (sw + ne) / antall_foringer(df)


def get_score_ne(df):
    foring = get_score_foring_ne(df) * sum(df.loc[:, 'NForingNE'])
    motspill = get_score_motspill_ne(df) * sum(df.loc[:, 'NMotspillNE'])
    return (foring + motspill) / (sum(df.loc[:, 'NForingNE']) + sum(df.loc[:, 'NMotspillNE']))


def get_score_sw(df):
    foring = get_score_foring_sw(df) * sum(df.loc[:, 'NForingSW'])
    motspill = get_score_motspill_sw(df) * sum(df.loc[:, 'NMotspillSW'])
    return (foring + motspill) / (sum(df.loc[:, 'NForingSW']) + sum(df.loc[:, 'NMotspillSW']))


def get_score(df):
    sw = get_score_foring_sw(df) * sum(df.loc[:, 'NForingSW']) + get_score_motspill_sw(df) * sum(df.loc[:, 'NMotspillSW'])
    ne = get_score_foring_ne(df) * sum(df.loc[:, 'NForingNE']) + get_score_motspill_ne(df) * sum(df.loc[:, 'NMotspillNE'])
    return (sw + ne) / antall_spill(df)


def get_middel(ant_par):
    return int(ant_par / 2) - 1


def get_df_by_year_and_month(df, year, month):
    new_df = pd.DataFrame()
    for i in range(0, len(df)):
        if df.loc[i, 'Ar'] == year and df.loc[i, 'Maned'] == month:
            new_df = new_df.append(df.loc[i, :], ignore_index=True)
    return new_df


def get_df_by_year(df, year):
    new_df = pd.DataFrame()
    for i in range(0, len(df)):
        if df.loc[i, 'Ar'] == year:
            new_df = new_df.append(df.loc[i, :], ignore_index=True)
    return new_df


def get_df_by_turnering(df, string):
    new_df = pd.DataFrame()
    for i in range(0, len(df)):
        if string in df.loc[i, 'Turnering']:
            new_df = new_df.append(df.loc[i, :], ignore_index=True)
    return new_df


def plot_2016_2019(df):
    score_ne = []
    score_sw = []
    score = []
    for i in range(2016, 2019):
        for j in range(1, 13):
            data2 = get_df_by_year_and_month(df=df, year=i, month=j)
            if len(data2):
                score_ne.append(get_score_ne(data2))
                score_sw.append(get_score_sw(data2))
                score.append(get_score(data2))

    # plt.plot(score, label="Score")
    plt.plot(score_ne, label="Score Løke")
    plt.plot(score_sw, label="Score Sæther")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)
    plt.show()


# data = pd.read_csv(filepath_or_buffer="C:/Users/Joppe/PycharmProjects/Eggeliste/res/eggeliste.csv", sep=',')
# data = pd.read_csv(filepath_or_buffer="C:/Users/Joppe/PycharmProjects/Eggeliste/res/joakim.csv", sep=',')
# data = get_df_by_year(data, 2019)
# df = pd.read_csv(filepath_or_buffer="C:/Users/Joppe/PycharmProjects/Eggeliste/res/eggeliste_fozzilet.csv", sep=',')
data = pd.read_csv(filepath_or_buffer="C:/Users/Joppe/PycharmProjects/Eggeliste/res/bbo.csv")

# plot_2016_2019(data)
# data = get_df_by_year(data, 2019)


print("Antall spill:", antall_spill(data))
print("Gjennomsnittscore:", get_score(data), "%")
print("Andel føringer:", get_andel_foringer(data), "%")
print("Score føringer:", get_score_foring(data), "%")
print("Andel motspill:", get_andel_motspill(data), "%")
print("Score motspill:", get_score_motspill(data), "%")
print("Score N/E:", get_score_ne(data), "%")
print("Score S/W:", get_score_sw(data), "%")


# Antall spill: 261.0
# Gjennomsnittscore: 51.33643495712461 %
# Andel føringer: 50.57471264367816 %
# Score føringer: 51.42045454545455 %
# Andel motspill: 49.42528735632184 %
# Score motspill: 51.25046142488003 %
# Score N/E: 48.81406761177753 %
# Score S/W: 53.878205128205124 %
