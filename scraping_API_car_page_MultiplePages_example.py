import requests
import pandas as pd
# from sqlalchemy import create_engine
import argparse

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6,lt;q=0.5',
    'priority': 'u=1, i',
    'referer': 'https://www.autolist.com/listings',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'has_been_prompted=true; OPTIMIZELY_USER_ID=f1c2ba51-960c-41fb-be50-d010dd126c92; client_guid_timestamp=52e0bd6d-d505-4c8b-bb8c-30aade257144.1745618790392; _gid=GA1.2.126041630.1745618791; _sp_ses.8ca5=*; _gcl_au=1.1.1998076695.1745618792; cto_bundle=ExbY519qTGkxNmhlV2dYbk92UkcyZUdXT2JpYlZUQWt1TzdMZTRXb0psbVBkcHI2WFJqb3N5d3AwMmhMa1NzbktPWHB3ZE9vVUZkbEFPVXp1VFZCaHJuc044ZGd6UDVjWVpuVmFtSjZsJTJGOW8lMkIlMkZUMXFjMWJIZDlhYzB2Mzc2d2hhdDJaMW9pVWFSTTJsbmlZJTJCNE1Wb2daMENNTndDb0FvVSUyQm9DVWpsN3M1JTJGTCUyRnFNVSUzRA; _ga_KKZ1EQJKEV=GS1.1.1745624642.2.0.1745624642.0.0.0; _ga=GA1.2.1080224247.1745618791; _sp_id.8ca5=119480b5-3b70-4bb9-8eff-f67120df30af.1745618791.1.1745624644.1745618791.f4ee4210-7d85-4586-b2ac-230f747364cc',
}

def building_parameters(brand, pages):
    return {
        'ads': 'true',
        'include_total_price_change': 'true',
        'include_time_on_market': 'true',
        'include_relative_price_difference': 'true',
        'latitude': '37.7749295',
        'limit': '20',
        'longitude': '-122.4194155',
        'make': brand,
        'page': f"{pages}",
        'radius': '100',
        'sort_filter': 'blended_score:desc',
        'zip': '10310',
    }

def making_request_to_API(brand, pages):
    try:
        response = requests.get('https://www.autolist.com/api/v2/search', params=building_parameters(brand, pages), headers=headers)
        return response.json()['records']
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_all_data(brand, pages):
    
    make_name = []
    model = []
    mileage = []
    dealer_name = []
    trim = []
    year = []
    full_name = []
    price = []
    
    for i in range(1, pages+1):
        
        if making_request_to_API(brand, pages) is None:
            break
        
        for info in making_request_to_API(brand, pages):
            make_name.append(info['make_name'])
            model.append(info['model_name'])
            mileage.append(info['mileage'])
            dealer_name.append(info['dealer_name'])
            trim.append(info['trim'])
            year.append(info['year'])
            full_name.append(f"{info.get('year')} {info.get('make_name')} {info.get('model_name')} {info.get('trim')}") 
            price.append(info['price'])
            
    
    return pd.DataFrame({'Ad title':full_name,
                         'Make':make_name,
                         'Model':model,
                         'Mileage':mileage,
                         'Dealer name':dealer_name,
                         'Price':price,
                         'Year':year})
    
def main():
    parser = argparse.ArgumentParser(description='Fetch car listings by brand')
    parser.add_argument('--brand', required=True, help='Choose a car brand')
    parser.add_argument('--pages', required=True, type=int, help='How many pages you want to fetch data from')
    parser.add_argument('--output', default='car_listings.xlsx', help='Output excel file name')
    args = parser.parse_args()
    
    data_table = get_all_data(args.brand, args.pages)
    data_table.to_excel(args.output, index=False)
    
    print(f"All the data for {args.brand} car brand, which contained {args.pages} pages, was saved in {args.output} file.")
     
    # # saving to Postgresql 
    # engine = create_engine('postgresql://postgres:Satsok14@localhost:5432/postgres')
    # merged_tables.to_sql('car_results', engine)

if __name__ == "__main__":
    main()
