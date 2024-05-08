import pandas as pd
from matplotlib import pyplot as plt
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from wordcloud import WordCloud


df = pd.read_csv("onion.csv")

categories = {
    "Stimulants": ["Adderall", "Methamphetamine", "Cocaine", "MDMA", "Amphetamine"],
    "Depressants/Anxiolytics": ["Xanax", "Valium", "Klonopin", "Ativan", "Suboxone"],
    "Pain Management": ["Oxycodone", "Hydrocodone", "Fentanyl", "Percocet", "Morphine"],
    "Hallucinogens": ["LSD", "DMT", "Psilocybin Mushrooms", "Ketamine", "PCP"],
    "Cannabinoids": ["Cannabis", "Synthetic Cannabinoids"],
    "Other Substances": ["GHB", "Nembutal", "Methaqualone", "Benzodiazepines", "Heroin"],
    "Additional Items": ["Rohypnol", "Diazepam", "Dilaudid", "Codeine", "Psychedelic Mushrooms"]
}

def visualize_WC(count):
    def map_to_category(product_name):
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in product_name.lower():
                    return category
        return product_name

    new_product_series = df['product'].apply(map_to_category)

    new_df = df.copy()  
    new_df['product'] = new_product_series 
    count = new_df.groupby('product').size().reset_index(name='count')

    d = {}

    for index,row in count.iterrows():
      d[f"{row['product']}"] = row["count"]

    wc = WordCloud(random_state = 1234,
                   width = 2000,
                   height = 2000,
                   background_color = "white"
                   )
    img_wordcloud = wc.generate_from_frequencies(d)
    img_wordcloud.to_file("0502.jpg")

def visualize_proba(count):
    def map_to_category(product_name):
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in product_name.lower():
                    return category
        return product_name

    #카테고리에 맞게 시리즈생성
    new_product_series = df['product'].apply(map_to_category)

    new_df = df.copy()  
    new_df['product'] = new_product_series 

    count = new_df.groupby('product').size().reset_index(name='count')


    drugs ,counts = count["product"],count["count"]

    colors = ['skyblue', 'salmon', 'lightgreen', 'orange', 'lightcoral']

    plt.figure(figsize=(8, 5)) 

    bars = plt.barh(drugs, counts, color=colors)

    plt.xlabel('Count')  
    plt.ylabel('drugs')  
    plt.title('drugs count') 

    for bar, drug, count in zip(bars, drugs, counts):
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, f'{count}', ha='left', va='center')

    plt.tight_layout()
    plt.savefig('proba.png') 
    plt.show()  

if __name__ == "__main__":
    visualize_WC()
    visualize_proba()
