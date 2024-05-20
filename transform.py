import pandas as pd

def transform():
    df = pd.read_excel("scraped_data.xlsx")
    df["postal_code"] = df["postal_information"].apply(
        lambda x: " ".join(x.split(" ")[:2]) 
        if pd.notna(x) else None
    )
    df["city"] = df["postal_information"].apply(
        lambda x:" ".join(x.split(" ")[2:]) if pd.notna(x) else None
    )
    del df["postal_information"]
    df.to_excel("data_transformed.xlsx")

if __name__=='__main__':
    transform()