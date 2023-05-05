"""
Name: Jani Jia
CS230: Section SN1F
Data: volcanoes.xlsx
URL: http://192.168.31.163:8501

Description:

This project includes:
    A project manual
    Volcano's Attributes
    A pie chart shows top 10 countires that have the most volcanoes in the world
    A bar chart shows different types of volcanos
    A Search Result fields(User could do filter on the navigation bar based on their preference)
    A visualization map, which recording all the location of volcanoes in the csv file.
    A side bar, which has 9 first option to select which volcanoes the user want to choose,
        and also a sub-options that helps user to do the detailed filter.
    12 functions
    9 imported packages
    some basic CSS style edition


    In order to do the functional implementation, I also use a technique about the database, to be specific, the primary key,
    so everything the user want to search on the side bar, the web page will record the volcano number of it, and later the script will
    use the volcano number to find other data that relate to it. In this case, the script will reduce memory usage at runtime.

    Overall, I think the coolest part of my code is the search side bar. But it used some complex if expressions, function, and it needs to
    transfer the argument between 4 places: FindVol(), line 292-327(sidebar), line 397-417(use the funtion) and line 420-440(the search result output).
    It also has some places have html technique.

"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import math
from PIL import Image
import numpy as np
import sys
import matplotlib


filename = 'volcanoes.xlsx'
volcanoesFile = pd.read_excel(filename)

#Initialize and reset the dictionary to deposit csv data
def DicReset(Dict):
    Dict = {"Volcano Number": "","Volcano Name": "","Country": "","Primary Volcano Type": "","Activity Evidence": "","Last Known Eruption": "","Region": "","Subregion": "","Latitude": "","Longitude": "","Elevation (m)": "","Dominant Rock Type": "","Tectonic Setting": "","Link": ""}
    return Dict
#Find all unique countries and return them as a list
def FindCountries(ListofDic):
    Countries = []
    for dic in ListofDic:
        country = dic["Country"]
        if country not in Countries: Countries.append(country)
    return Countries
#Find all unique Primary Volcano Types and return them as a list
def FindVolcanoTypes(ListofDic):
    Types = []
    for dic in ListofDic:
        type = dic["Primary Volcano Type"]
        if type not in Types: Types.append(type)
    return Types
#Find all unique Rock Types and return them as a list
def FindRockTypes(ListofDic):
    RockTypes = []
    for dic in ListofDic:
        rocktype = dic["Dominant Rock Type"]
        if rocktype not in RockTypes: RockTypes.append(rocktype)
    return RockTypes
#Find all unique Activity Evidence and return them as a list
def FindActiEvi(ListofDic):
    ActiEvis = []
    for dic in ListofDic:
        actievi = dic["Activity Evidence"]
        if actievi not in ActiEvis: ActiEvis.append(actievi)
    return ActiEvis
#Find all unique Tectionic Setting and return them as a list
def FindTectonicSetting(ListofDic):
    TectSettings = []
    for dic in ListofDic:
        tectsetting = dic["Tectonic Setting"]
        if tectsetting not in TectSettings: TectSettings.append(tectsetting)
    return TectSettings
#Find all unique Regions
def FindRegions(ListofDic):
    Regions = []
    for dic in ListofDic:
        region = dic["Region"]
        if region not in Regions: Regions.append(region)
    return Regions
#Find the country with its volcano's quantity
def FindMostVolCountry(ListofDic):
    VolNuminCountry = {}
    Countries = FindCountries(ListofDic)
    for country in Countries:VolNuminCountry[country] = 0
    for dic in ListofDic:
        for country in Countries:
            if dic["Country"] == country: VolNuminCountry[country] += 1
    return VolNuminCountry
#Find the volcano type with its quantity
def FindMostVolType(ListofDic):
    VolTypeCount = {}
    Types = FindVolcanoTypes(ListofDic)
    for type in Types: VolTypeCount[type] = 0
    for dic in ListofDic:
        for type in Types:
            if dic["Primary Volcano Type"] == type: VolTypeCount[type] += 1
    return VolTypeCount
#barchart function
def barchart(Dic, Type):
    plt.cla()
    plt.clf()
    p = Dic.values()
    x = Dic.keys()
    if Type == "VolType":
        plt.bar(x, p, color='r')
        plt.xticks(rotation=90)
        plt.xlabel("Primary Volcano Type")
        plt.ylabel("Quantity")
    elif Type == "VolinCountries":
        plt.bar(x, p, color='b')
        plt.xticks(rotation=90)
        plt.xlabel("Countries")
        plt.ylabel("Quantity")
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    return plt
#piechart function
def piechart(Dic, Type):
    VolinCountries = FindMostVolCountry(Dic)
    VolinCountries = sorted(VolinCountries.items(),reverse=True)
    if Type == "VolinCountries":
        countries = []
        quantity = []
        i = 0
        for key, value in VolinCountries:
            if i == 10: break
            else:
                quantity.append(value)
                countries.append(key)
                i+=1
        myexplode = [0,0,0,0.2,0,0,0,0,0,0]
        y = np.array(quantity)
        mylabels = countries
        plt.pie(y,labels = mylabels,explode=myexplode)
        plt.title("Top 10 countries that have the most volcanoes.")
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        return plt
#The VERY USEFUL function to find detailed information by user's input on the side bar.
def FindVol(Col,ListofDic,SearchInput="",SearchInput2=""):
    Result = []
    if Col == 1:
        SearchInput = int(float(SearchInput))
        for dic in ListofDic:
            volnum = dic["Volcano Number"]
            if volnum == SearchInput:
                Result.append(volnum)
        return Result
    elif Col == 2:
        for dic in ListofDic:
            volname = dic["Volcano Name"]
            if volname == SearchInput:
                Result.append(dic["Volcano Number"])
        return Result
    elif Col == 3:
        for dic in ListofDic:
            country = dic["Country"]
            if country == SearchInput:
                Result.append(dic["Volcano Number"])
        return Result
    elif Col == 4:
        for dic in ListofDic:
            type = dic["Primary Volcano Type"]
            if type == SearchInput:
                Result.append(dic["Volcano Number"])
        return Result
    elif Col == 5:
        for dic in ListofDic:
            actievi = dic["Activity Evidence"]
            if actievi == SearchInput:
                Result.append(dic["Volcano Number"])
        return Result
    elif Col == 7:
        for dic in ListofDic:
            region = dic["Region"]
            subregion = dic["Subregion"]
            if region == SearchInput and subregion == SearchInput2:
                Result.append(dic["Volcano Number"])
        return Result
    elif Col == 8:
        for dic in ListofDic:
            ele = dic["Elevation (m)"]
            if ele <= SearchInput:
                Result.append(dic["Volcano Number"])
        return Result
    elif Col == 9:
        for dic in ListofDic:
            rocktype = dic["Dominant Rock Type"]
            if rocktype == SearchInput:
                Result.append(dic["Volcano Number"])
        return Result
    elif Col == 10:
        for dic in ListofDic:
            tectsetting = dic["Tectonic Setting"]
            if tectsetting == SearchInput:
                Result.append(dic["Volcano Number"])
        return Result

#initialize volcanoes information variable
volcanoes_info = {
    "Volcano Number": "",
    "Volcano Name": "",
    "Country": "",
    "Primary Volcano Type": "",
    "Activity Evidence": "",
    "Last Known Eruption": "",
    "Region": "",
    "Subregion": "",
    "Latitude": "",
    "Longitude": "",
    "Elevation (m)": "",
    "Dominant Rock Type": "",
    "Tectonic Setting": "",
    "Link": ""
}
#A list to deposit dictionaries
volcanoesList = []
#transfer data from csv file into a dictionary, then put the dictionary into the list
for list in volcanoesFile.values:
    volcanoes_info["Volcano Number"] = list[0]
    volcanoes_info["Volcano Name"] = list[1]
    volcanoes_info["Country"] = list[2]
    volcanoes_info["Primary Volcano Type"] = list[3]
    volcanoes_info["Activity Evidence"] = list[4]
    volcanoes_info["Last Known Eruption"] = list[5]
    volcanoes_info["Region"] = list[6]
    volcanoes_info["Subregion"] = list[7]
    volcanoes_info["Latitude"] = list[8]
    volcanoes_info["Longitude"] = list[9]
    volcanoes_info["Elevation (m)"] = list[10]
    volcanoes_info["Dominant Rock Type"] = list[11]
    volcanoes_info["Tectonic Setting"] = list[12]
    volcanoes_info["Link"] = list[13]
    volcanoesList.append(volcanoes_info)
    volcanoes_info = DicReset(volcanoes_info) #iterate each row in csv file, and put them in a dic variable, then append the dic variable into a list

#I think this part is cool because it will need to use the sub-relationship between regions and subregions.
##################################################################################################
#Add elements into RegionwithSubregion Dictionary
Regions = []
#Add elements into Regions list
Regions = FindRegions(volcanoesList)
RegionwithSubregion = {}
for region in Regions:
    RegionwithSubregion[region] = []
for key, value in RegionwithSubregion.items():
    Subregions = []
    for dic in volcanoesList:
        if dic["Region"] == key:
            if dic["Subregion"] not in Subregions:
                Subregions.append(dic["Subregion"])
    RegionwithSubregion[key] = Subregions
##################################################################################################

#Initialize some list variables
Countries = FindCountries(volcanoesList)
Countries.sort()
VolcanoTypes = FindVolcanoTypes(volcanoesList)
VolcanoTypes.sort()
RockTypes = FindRockTypes(volcanoesList)
ActiEvi = FindActiEvi(volcanoesList)
ActiEvi.sort()
Regions = FindRegions(volcanoesList)
Regions.sort()
TectSettings = FindTectonicSetting(volcanoesList)


#Side bar
st.sidebar.header('Search Navigation')
st.sidebar.write("Are you looking for valcanoes that:")
VolcanoAttributes = []
for key in volcanoes_info.keys(): VolcanoAttributes.append(key)
VolcanoAttributes.remove('Subregion')
VolcanoAttributes.remove('Link')
VolcanoAttributes.remove('Latitude')
VolcanoAttributes.remove('Longitude')
VolcanoAttributes.remove('Last Known Eruption')
#the code below from: https://stackoverflow.com/questions/65026852/set-default-value-for-selectbox
default_ix = VolcanoAttributes.index("Volcano Name")
selectedAttributes = st.sidebar.radio('Volcano Attribute', VolcanoAttributes, index=default_ix)
Col = 0
if selectedAttributes == "Volcano Number":
    volnum = st.sidebar.text_input(label="Please enter the volcano number you want to search:")
    Col = 1
elif selectedAttributes == "Volcano Name":
    volname = st.sidebar.text_input(label="Please enter the volcano name you want to search:")
    Col = 2
elif selectedAttributes == "Country":
    st.sidebar.markdown('Please select the country you want to search:')
    selectedCountry = st.sidebar.radio('Countries', Countries)
    Col = 3
elif selectedAttributes == "Primary Volcano Type":
    st.sidebar.markdown('Please select the volcano type you want to search:')
    selectedType = st.sidebar.radio('Primary Volcano Type:',VolcanoTypes)
    Col = 4
elif selectedAttributes == "Activity Evidence":
    st.sidebar.markdown('Please select the activity evidence you want to search:')
    selectedActiEvi = st.sidebar.radio('Activity Evidence', ActiEvi)
    Col = 5
elif selectedAttributes == "Region":
    st.sidebar.markdown('Please select the region you want to search:')
    selectedRegion = st.sidebar.radio('Regions', Regions)
    st.sidebar.markdown('Please select the subregion you want to search:')
    selectedSubRegion = st.sidebar.radio('Subregion',RegionwithSubregion[selectedRegion])
    Col = 7
elif selectedAttributes == "Elevation (m)":
    ElevationHeight = st.sidebar.slider('Please select the elevation you want to search:',-5700,6879)
    Col = 8
elif selectedAttributes == "Dominant Rock Type":
    st.sidebar.markdown('Please select the dominant rock type you want to search:')
    selectedRockType = st.sidebar.radio('Rock Types',RockTypes)
    Col = 9
elif selectedAttributes == "Tectonic Setting":
    st.sidebar.markdown('Please select the tectonic setting you want to search:')
    selectedTectSetting = st.sidebar.radio('Tectonic Setting',TectSettings)
    Col = 10



#Title
st.title("Welcome to Jani CS230 Final Project!")
st.markdown("The project is finished on July 1, 2021\n")
########################################################################I think it is cool to use python to insert image on the webpage.
#Main Page
#image = Image.open('volcanoclipart.png')
#st.image(image,width=700)

st.write('\n')
########################################################################it is cool to use css style at here !!!
st.write(f'<p style="color:#FF8000;text-align:center;font-size:30px;font-weight:bold;font-family: \'Bauhaus 93\';">Project Manual</p>', unsafe_allow_html=True)
st.markdown(f'<p style="color:#663300;font-weight:bold">-In this streamlit page, you can search any volcano information in our database by its attributes. By simply click the key words in the navigation bar, '
            f'it will display the unique way to search the volcano you are looking for. Then, a map will show the location of the volcano. ',
            unsafe_allow_html=True)

st.write(f"""
### Volcano's Attributes:
- <p style="color:#FF0000;">Volcano Number</p>
- <p style="color:#FF8000;">Volcano Name</p>
- <p style="color:#FFFF00;">Country</p>
- <p style="color:#80FF00;">Primary Volcano Type</p>
- <p style="color:#00FF00;">Activity Evidence</p>
- <p style="color:#00FF80;">Last Known Eruption</p>
- <p style="color:#00FFFF;">Region (Subregion)</p>
- <p style="color:#0080FF;">Latitude</p>
- <p style="color:#0000FF;">Longitude</p>
- <p style="color:#7F00FF;">Elevation (m)</p>
- <p style="color:#FF00FF;">Dominant Rock Type</p>
- <p style="color:#FF007F;">Tectonic Setting</p>
- <p style="color:#808080;">Link</p>
""", unsafe_allow_html=True)

st.markdown("### Volcanoes Statistical Values:")
#bar chart about the country that has the most volcanoes
mostcountryname = ""
mostvolincountries = 0
#Find the most volcanoes and the country of it.
for key, value in FindMostVolCountry(volcanoesList).items():
    if value > mostvolincountries:
        mostcountryname = key
        mostvolincountries = value
st.markdown(f"We have a total number of {len(volcanoesList)} in our database.")
st.markdown(60*'=')
st.markdown(f"The country that has the most volcano is {mostcountryname}, and it has a total number of {mostvolincountries} volcanoes.")
st.pyplot(piechart(volcanoesList,"VolinCountries"))
st.markdown(f"Above shows a pie chart that top 10 countries that have the most valcanoes in the world.")
st.markdown(60*'=')

#Find the most volcanoes type quantity and the type of it
FindMostVolTypeDic = FindMostVolType(volcanoesList)
st.pyplot(barchart(FindMostVolTypeDic,"VolType"))
st.markdown(f"Above is the distribution table of different volcanoes' type.")
mosttypename = ""
mosttypequantity = 0
for key, value in FindMostVolTypeDic.items():
    if value > mosttypequantity:
        mosttypequantity = value
        mosttypename = key
st.markdown(f"Obviously, in our volcano database, {mosttypename} type has the most quantity of volcanoes, and it has a total number of {mosttypequantity} volcanoes.")


st.markdown(70*'=')
st.write(f'<p style="color:#0000FF;text-align:center;font-size:30px;font-weight:bold;">Search Result </p>', unsafe_allow_html=True)
st.write(f'<p style="color:#0000FF;text-align:center;font-size:30px;font-weight:bold;">----------------------</p>', unsafe_allow_html=True)

#Based on the user search selection, the script will use FindVol function. Transfer the third argument from the user input.
searchresult={}#a dic deposits primary key in csv file
searchresult = DicReset(searchresult)
result = []
if Col == 1:
    result = FindVol(1,volcanoesList,volnum)
elif Col == 2:
    result = FindVol(2,volcanoesList,volname)
elif Col == 3:
    result = FindVol(3,volcanoesList,selectedCountry)
elif Col == 4:
    result = FindVol(4,volcanoesList,selectedType)
elif Col == 5:
    result = FindVol(5,volcanoesList,selectedActiEvi)
elif Col == 7:
    result = FindVol(7,volcanoesList,selectedRegion,selectedSubRegion)
elif Col == 8:
    result = FindVol(8,volcanoesList,ElevationHeight)
elif Col == 9:
    result = FindVol(9,volcanoesList,selectedRockType)
elif Col == 10:
    result = FindVol(10,volcanoesList,selectedTectSetting)

#search result output area
searchresults = 0
for dic in volcanoesList:
    for theresult in result:
        if dic["Volcano Number"] == theresult:
            st.write(f'<p style="color:#0000FF;text-align:left;font-size:20px;">Volcano Number: {dic["Volcano Number"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Volcano Name: {dic["Volcano Name"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Country: {dic["Country"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Primary Volcano Type: {dic["Primary Volcano Type"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Activity Evidence: {dic["Activity Evidence"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Last Known Eruption: {dic["Last Known Eruption"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Region: {dic["Region"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Subregion: {dic["Subregion"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Latitude: {dic["Latitude"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Longitude: {dic["Longitude"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Elevation (m): {dic["Elevation (m)"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Dominant Rock Type: {dic["Dominant Rock Type"]}</p>',
                    f'<p style="color:#0000FF;text-align:left;font-size:20px;">Tectonic Setting: {dic["Tectonic Setting"]}</p>',
                    f'<a style="color:#0000FF;text-align:left;font-size:20px;" href = "{dic["Link"]}" target="_blank">Link: {dic["Link"]}</p>',
                    f'<p style="color:#0000FF;text-align:center;font-size:30px;font-weight:bold;">-----------------------------</p>'
                    , unsafe_allow_html=True)
            searchresults +=1

st.markdown(70*'=')
st.write(f'<p style="color:#0000FF;text-align:center;font-size:30px;font-weight:bold;">Total search result(s): {searchresults} </p>', unsafe_allow_html=True)
#Coordinate Map
latitudes = []
longitudes = []
names = []
tup = ()
Vollocations = []
for dic in volcanoesList:
    tup = (dic["Volcano Name"],dic["Latitude"],dic["Longitude"])
    Vollocations.append(tup)
    tup = ()

Vollocdf = pd.DataFrame(Vollocations, columns=["Volcano Name", "lat", "lon"])
st.write("Volcanoes Map")
view_state = pdk.ViewState(
    latitude=22.553465,
    longitude=114.058778,
    zoom = 11,
    pitch = 20)
layer1 = pdk.Layer('ScatterplotLayer',
                  data = Vollocdf,
                  get_position = '[lon, lat]',
                  get_radius = 10000,
                  get_color = [255,128,0],
                  pickable = True)
tool_tip = {"html": "Volcano Name:<br> <b>{Volcano Name}</b><br> Latitude:<br> <b>{lat}</b><br> Longitude:<br> <b>{lon}</b>",
            "style": { "backgroundColor": "steelblue","color": "white"}}

map = pdk.Deck(
    initial_view_state=view_state,
    layers=[layer1],
    tooltip= tool_tip
)
print(Vollocdf)
st.pydeck_chart(map)

df = pd.DataFrame(volcanoesList)
st.header('Some Statistical Data：')
st.write(df.describe())

table = pd.pivot_table(df, values=['Elevation (m)'], index=['Dominant Rock Type'])
st.header('A pivot table shows the relationship between \'Dominant Rock Type\' and \'Elevation (m)\'. ')
st.write(table)

print(view_state)
print(layer1)
print(tool_tip)
#Thanks Professor Xu for teaching CS230 in this summer trimester! Really appreciate it!







