import requests, time
from bs4 import BeautifulSoup as bs
import pandas as pd
import itertools

def collecting_info(brutto_lohn_jahr: str="30000", abrechnungs_jahr: str="2024", steuerklasse: str="1"):
    url = 'https://www.brutto-netto-rechner.info/index.php'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.brutto-netto-rechner.info',
        'referer': 'https://www.brutto-netto-rechner.info/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    data = {
        'f_start': '1',
        'ok': '1',
        'f_bruttolohn': f'{brutto_lohn_jahr}',
        'f_abrechnungszeitraum': 'jahr',
        'f_geld_werter_vorteil': '0',
        'f_abrechnungsjahr': f'{abrechnungs_jahr}',
        'f_steuerfreibetrag': '',
        'f_steuerklasse': f'{steuerklasse}',
        'f_kirche': 'nein',
        'f_bundesland': 'baden-wuerttemberg',
        'f_alter': '35',
        'f_kinder': 'nein',
        'f_kinderfreibetrag': '0',
        'f_kinder_anz': '0',
        'f_krankenversicherung': 'pflichtversichert',
        'f_private_kv': '',
        'f_arbeitgeberzuschuss_pkv': 'ja',
        'f_KVZ': '1.7',
        'f_rentenversicherung': 'pflichtversichert',
        'f_arbeitslosenversicherung': 'pflichtversichert'
    }

    response = requests.post(url, headers=headers, data=data)
    return response

def clean_table(table):
    table_data = []
    for row in table.find_all("tr"):
        data = row.find_all("td")
        small_list = []
        for info in data:
            if info.text.strip():
                small_list.append(info.text.strip())
        table_data.append(small_list)

    clean_table_data = []

    for row in table_data:
        clean_row = []
        for cell in row:
            # Replace non-breaking spaces with regular spaces and strip leading/trailing whitespace
            clean_cell = cell.replace('\xa0', ' ').strip()
            clean_row.append(clean_cell)
        # Filter out empty strings if the entire row isn't empty
        if any(clean_row):
            clean_row = [cell for cell in clean_row if cell != '']
            clean_table_data.append(clean_row)

    for i, row in enumerate(clean_table_data):
        if len(row) != 3:
            del clean_table_data[i]
    
    return clean_table_data

def dataframe_operations(clean_table_data):
    df = pd.DataFrame(clean_table_data)
    df  = df.transpose()
    df.columns = df.iloc[0]
    df = df[1:]

    new_data = {
        # Brutto
        "Brutto Monat": df.loc[df["Ergebnis"] == "Monat", "Brutto:"].values,
        "Brutto Jahr": df.loc[df["Ergebnis"] == "Jahr", "Brutto:"].values,
        
        # Geldwerter Vorteil
        "Geldwerter Vorteil Monat": df.loc[df["Ergebnis"] == "Monat", "Geldwerter Vorteil:"].values,
        "Geldwerter Vorteil Jahr": df.loc[df["Ergebnis"] == "Jahr", "Geldwerter Vorteil:"].values,
        
        # Solidaritätszuschlag
        "Solidaritätszuschlag Monat": df.loc[df["Ergebnis"] == "Monat", "Solidaritäts- zuschlag:"].values,
        "Solidaritätszuschlag Jahr": df.loc[df["Ergebnis"] == "Jahr", "Solidaritäts- zuschlag:"].values,
        
        # Kirchensteuer
        "Kirchensteuer Monat": df.loc[df["Ergebnis"] == "Monat", "Kirchensteuer:"].values,
        "Kirchensteuer Jahr": df.loc[df["Ergebnis"] == "Jahr", "Kirchensteuer:"].values,
        
        # Lohnsteuer
        "Lohnsteuer Monat": df.loc[df["Ergebnis"] == "Monat", "Lohnsteuer:"].values,
        "Lohnsteuer Jahr": df.loc[df["Ergebnis"] == "Jahr", "Lohnsteuer:"].values,
        
        # Steuern
        "Steuern Monat": df.loc[df["Ergebnis"] == "Monat", "Steuern:"].values,
        "Steuern Jahr": df.loc[df["Ergebnis"] == "Jahr", "Steuern:"].values,
        
        # Rentenversicherung
        "Rentenversicherung Monat": df.loc[df["Ergebnis"] == "Monat", "Renten- versicherung:"].values,
        "Rentenversicherung Jahr": df.loc[df["Ergebnis"] == "Jahr", "Renten- versicherung:"].values,
        
        # Arbeitslosenversicherung
        "Arbeitslosenversicherung Monat": df.loc[df["Ergebnis"] == "Monat", "Arbeitslosen- versicherung:"].values,
        "Arbeitslosenversicherung Jahr": df.loc[df["Ergebnis"] == "Jahr", "Arbeitslosen- versicherung:"].values,
        
        # Krankenversicherung
        "Krankenversicherung Monat": df.loc[df["Ergebnis"] == "Monat", "Kranken- versicherung:"].values,
        "Krankenversicherung Jahr": df.loc[df["Ergebnis"] == "Jahr", "Kranken- versicherung:"].values,
        
        # Pflegeversicherung
        "Pflegeversicherung Monat": df.loc[df["Ergebnis"] == "Monat", "Pflege- versicherung:"].values,
        "Pflegeversicherung Jahr": df.loc[df["Ergebnis"] == "Jahr", "Pflege- versicherung:"].values,
        
        # Sozialabgaben
        "Sozialabgaben Monat": df.loc[df["Ergebnis"] == "Monat", "Sozialabgaben:"].values,
        "Sozialabgaben Jahr": df.loc[df["Ergebnis"] == "Jahr", "Sozialabgaben:"].values,
        
        # Netto
        "Netto Monat": df.loc[df["Ergebnis"] == "Monat", "Netto:"].values,
        "Netto Jahr": df.loc[df["Ergebnis"] == "Jahr", "Netto:"].values
    }

    new_df = pd.DataFrame(new_data, index=["Values"])

    for column in new_df.columns:
        # Remove currency symbol (€) and thousands separator (.), and replace comma with dot for decimal
        new_df[column] = new_df[column].str.replace('€', '').str.replace('.', '').str.replace(',', '.').astype(float)
    
    return new_df

# Define your lists of search terms
brutto_lohn_jahr = [str(x) for x in range(30000, 120000, 1000)]
abrechnungsjahr = ['2023', '2024']
steuerklasse = ['1', '3']

# Use itertools.product to generate all combinations of search terms
combinations = list(itertools.product(brutto_lohn_jahr, abrechnungsjahr, steuerklasse))

main_df = pd.DataFrame()
# Iterate over the combinations and call collecting_info with each combination
for i, combo in enumerate(combinations):
    time.sleep(1)  # not to send too many requests
    print(i, combo)
    response = collecting_info(*combo)
    soup = bs(response.content, 'lxml')

    table = soup.find('table', {'class': 'rechner'})
    clean_table_data = clean_table(table=table)
    df = dataframe_operations(clean_table_data=clean_table_data)
    df["Steuerklasse"] = combo[2]
    df["Abrechnungsjahr"] = combo[1]
    main_df = pd.concat([main_df, df],axis=0)

main_df.to_csv("results.csv")
