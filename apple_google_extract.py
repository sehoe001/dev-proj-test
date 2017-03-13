import webbrowser
import urllib2
import json
from pprint import pprint
import csv
import string

#Define Categories for android. Excel Header : JSON name
android_categories = {'Application Name' : 'title', 'Application Location' : 'Google Play Store', 'Release Date' : 'created', 'Description' : 'description', 'Version' : 'version', 'Version Release Date' : 'market_update', 'Developer Name' : 'developer', 'Minimum SDK/OS Version' : 'min_sdk', 'Supported Devices' : 'not provided', 'Downloads' : 'downloads', 'Version Release Notes' : 'what_is_new', 'Ratings - Total' : 'number_ratings', 'Ratings - Average' : 'rating', 'Price' : 'price', 'Application Size (Bytes)' : 'size'}

#Define Categories for apple. Excel Header : JSON name
apple_categories = {'Application Name' : 'trackCensoredName', 'Application Location' : 'Apple App Store', 'Release Date' : 'releaseDate', 'Description' : 'description', 'Version' : 'version', 'Version Release Date' : 'currentVersionReleaseDate', 'Developer Name' : 'artistName', 'MinimumSDK/OS Version' : 'minimumOsVersion', 'Supported Devices' : 'supportedDevices', 'Downloads' : 'not provided', 'Version Release Notes' : 'releaseNotes', 'Ratings - Total' : 'userRatingCount', 'Ratings - Average' : 'averageUserRating', 'Price' : 'price', 'Application Size (Bytes)' : 'fileSizeBytes'}

#Add categories to array for write to CSV
categories = []
for key in sorted(android_categories):
    categories.append(key)

#Request from google play api and parse results
#Returns array of android app info in order of category headers
def androidPull():

    #url from 42matters API that searches based on developer name
    # token is API token given by 42matters
    url = 'https://data.42matters.com/api/v2.0/android/apps/search.json?q=PNC+Bank&include_developer=true&access_token=ccd29e63ec048ab955a4ce865cc9a5b3ee42641e'
    response = urllib2.urlopen(url)

    #Write JSON response
    with open('AndroidExtract.json', 'w') as hi_file:
        hi_file.write(response.read())
    
    #Parse and open JSON file
    with open('AndroidExtract.json') as data_file:
        data = json.loads(data_file.read())

    #Add data for each app to array. Drop unicod and white space  where necessary    
    num_apps = len(data['results'])
    app_info = [[] for i in range(num_apps)] #array to return for CVS write
    for key in sorted(android_categories): #iterate over keys in alpha order
        field = android_categories[key] 
        for i in range(num_apps): #iterate over each application
            #If app contains field, store it. Else store N/A
            if field in data['results'][i]:
                #Drop unicode and whitespace
                if isinstance(data['results'][i][field], basestring):
                    temp = data['results'][i][field]
                    temp = "".join(b for b in temp if b in string.printable)
                    temp = ' '.join(temp.split())
                    data['results'][i][field] = temp
                app_info[i].append(data['results'][i][field])
            elif field == 'Google Play Store':
                app_info[i].append(field)
            else:
                app_info[i].append('N/A')
    return app_info

def applePull():

    #url from 42matters API that searches based on developer name
    # token is API token given by 42matters
    url = 'https://data.42matters.com/api/v2.0/ios/apps/search.json?q=PNC+Bank&include_developer=true&access_token=ccd29e63ec048ab955a4ce865cc9a5b3ee42641e'
    
    response = urllib2.urlopen(url)

    #Write JSON response
    with open('AppleExtract.json', 'w') as hi_file:
        hi_file.write(response.read())
    
    #Parse and open JSON file
    with open('AppleExtract.json') as data_file:
        data = json.loads(data_file.read())

    #Add data for each app to array. Drop unicod and white space  where necessary    
    num_apps = len(data['results'])
    app_info = [[] for i in range(num_apps)] #array to return app info
    for key in sorted(apple_categories): #iterate over keys in alpha order
        field = apple_categories[key]
        for i in range(num_apps): 
            if field in data['results'][i]:
                if isinstance(data['results'][i][field], basestring):
                    temp = data['results'][i][field]
                    temp = "".join(b for b in temp if b in string.printable)
                    temp = ' '.join(temp.split())
                    data['results'][i][field] = temp
                app_info[i].append(data['results'][i][field])
            elif field == 'Apple App Store':
                app_info[i].append(field)
            else:
                app_info[i].append('N/A')
    return app_info

def main():
    
    apple_info = applePull()
    android_info = androidPull()

    #write to CSV
    with open('Application_Extract.csv', 'wb') as csvfile:
        w = csv.writer(csvfile, delimiter = '|') #pipe delimited
        w.writerow(categories)
        for i in apple_info:
            w.writerow(i)
        for j in android_info:
            w.writerow(j)

if __name__ == '__main__':
    main()

   
    
