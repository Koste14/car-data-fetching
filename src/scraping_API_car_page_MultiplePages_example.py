import requests
import pandas as pd
from config.config import HEADERS, API_URL
import argparse

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
        response = requests.get(API_URL, params=building_parameters(brand, pages), headers=HEADERS)
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
if __name__ == "__main__":
    main()
