import sys
from geopy.distance import distance
import pandas as pd
from collections import OrderedDict

latitude_rowname = "LATITUDE"
longitude_rowname = "LONGITUDE"

def main():
    print("Loading Excel Files...")
    cities_xl_file = pd.ExcelFile(sys.argv[1])
    cities_dataframe = cities_xl_file.parse("Cities")
    num_city_rows = 26984

    geopoints_xl_file = pd.ExcelFile(sys.argv[2])
    geopoints_dataframe = geopoints_xl_file.parse("Points")
    num_point_rows = 36017

    cities_list = []
    i=0
    j=0

    print("Starting...")
    # while(i < num_city_rows):
    #     print("City",i+1,"of",num_city_rows)
    #     cities_list += [[cities_dataframe["NAME"][i],cities_dataframe["POP_2010"][i],cities_dataframe["COUNTY"][i],cities_dataframe["STATE"][i]] 
    #         for j in range(num_point_rows) if distance((cities_dataframe[latitude_rowname][i],cities_dataframe[longitude_rowname][i]),
    #         (geopoints_dataframe[latitude_rowname][j],geopoints_dataframe[longitude_rowname][j])).miles < 7]
    #     i+=1
    # city_set = set(tuple(x) for x in cities_list)
    # city_list_no_duplicates = [ list(x) for x in city_set ]

    while(i < num_city_rows):
        print("City",i+1,"of",num_city_rows)
        while(j < num_point_rows):
            j+=1
            if distance((cities_dataframe[latitude_rowname][i],cities_dataframe[longitude_rowname][i]),
            (geopoints_dataframe[latitude_rowname][j],geopoints_dataframe[longitude_rowname][j])).miles < 7:
                cities_list.append([cities_dataframe["NAME"][i],cities_dataframe["POP_2010"][i],cities_dataframe["COUNTY"][i],cities_dataframe["STATE"][i]])
                break
        i, j = i+1, 0
    
    output_dataframe = pd.DataFrame(cities_list,columns=["City/Town","2010 Population","County","State"])
    excel_writer = pd.ExcelWriter('output.xlsx',engine='xlsxwriter')
    output_dataframe.to_excel(excel_writer,sheet_name='Sheet1',index=False)
    excel_writer.save()

if len(sys.argv) != 3:
    raise SyntaxError("Incorrect Syntax\nUsage: python Generate-Cites.py [US_Cities_File] [lat_long_points_file]")

if __name__ == "__main__":
    main()