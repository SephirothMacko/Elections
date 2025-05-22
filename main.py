## That code has been designed after first round of presidential
## election in Poland (18/05/2025) and before second round (01/06/2025))

import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
## 0 - pie chart
## 1 - column chart

def main():
    df = pd.read_csv("kandydaci.csv", sep=";", header=0, engine="python", index_col=0)
    ##Removal of unnecessary columns
    df.drop(['Poparcie', 'Procent głosów', 'Czy uzyskał mandat'], axis=1, inplace=True)
    ## Enumeration of gender distribution among candidates.
    df["Płeć"] = df["Płeć"].map({"Mężczyzna": 1, "Kobieta": 0})
    gender = {"Male": parity(df["Płeć"], 1), "Female": parity(df["Płeć"], 0)}
    print(f"Among the candidates in the presidential elections, there were {gender["Female"]} women.")
    print(f"Among the candidates in the presidential elections, there were {gender["Male"]} men.")
    ## Party affiliation among candidates.
    party_aff = {"Independent": loyalist(df["Przynależność do partii"], 0), "Party members": loyalist(df["Przynależność do partii"], 1)}
    print(f"In the elections, {party_aff["Party members"]} party members and {party_aff["Independent"]} independent candidates participated.")
    ## Occupation provided by the candidate, ultimately irrelevant in the analysis.
    # print(df.groupby("Zawód").size())
    ## Place of residence indicated by the largest number of candidates.
    print(f"Place of residence most frequently indicated by candidates was "
          f"{list(dict(df.groupby("Miejsce zamieszkania").size().sort_values(ascending=False).head(1)).keys())[0]}.")
    ## Assigning a candidate's surname to their election support count in descending order.
    df.sort_values(by="Liczba głosów", ascending=False, inplace=True)
    df["Nazwisko i imiona"] = df["Nazwisko i imiona"].str.split().str[-1].str.capitalize()
    support = dict()
    for n in range(0, len(list(df["Nazwisko i imiona"]))):
        support[str(list(df["Nazwisko i imiona"])[n])] = list(df["Liczba głosów"])[n]

    # Chart of genders
    charts(gender, 'Genders', 0)
    # Chart of Party affiliation
    charts(party_aff, "Party affinity", 0)
    # Chart of election support
    charts(support, "Candidates' Votes", 1, 90)

def charts(dictionary, title, kind_of_chart, rotation=0):
    df = pd.DataFrame(list(dictionary.items()), columns=['col1', 'col2'])
    # print(df)
    match kind_of_chart:
        case 0:
            plt.pie(df['col2'], labels=df['col1'], autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
        case 1:
            sns.barplot(x='col1', y='col2', data=df,)
            plt.xlabel('')
            plt.ylabel('')
            plt.xticks(rotation=rotation)
            plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
            plt.subplots_adjust(bottom=0.25)
    plt.title(title)

    plt.show()

def parity(col, sex):
    return list(col).count(sex)

def loyalist(col, member):
    return list(col.apply(lambda x: 0 if str(x).startswith('nie') else 1)).count(member)


if __name__ == '__main__':
    main()
