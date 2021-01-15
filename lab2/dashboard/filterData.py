import itertools
import pandas as pd

import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO


def andFilter(row,column,values):
    return set(values).issubset(set(row[column])) 

def orFilter(row,column,values):
    return any(item in row[column] for item in values)

def notFilter(row,column,values):
    return not (any(item in row[column] for item in values))
  
def equalsFilter(row,column,values):
    return sorted(row[column]) == sorted(values)

def smallerFilter(row,column,value):
    return row[column] < value

def biggerFilter(row,column,value):
    return row[column] > value

def sameFilter(row,column,value):
    return row[column] == value

def notSameFilter(row,column,values):
    return row[column] != values

def multipleFilter(df, funcArr):
    erg = df
    #print(str(funcArr))
    for func in funcArr:
        erg = erg[erg.apply(lambda row: func(row), axis=1)]
    return erg

def sortAndLimit(df,dataSortBy,dataAscDesc,dataPercent):
    asc = dataAscDesc == 'asc'
    rowNr = int(len(df)*(dataPercent/100))
    return df.sort_values(by=dataSortBy,ascending=asc).head(rowNr)

def sortAndLimit2(df,dataSortBy,dataAscDesc,data,type):
    asc = dataAscDesc == 'asc'
    if(type == "%"):
        rowNr = int(len(df)*(data/100))
    else:
         rowNr = data
    return df.sort_values(by=dataSortBy,ascending=asc).head(rowNr)

############################

def getAllCombinations(stuff):
    erg = []
    for L in range(0, len(stuff)+1):
        for subset in itertools.combinations(stuff, L):
            erg.insert(0,list(subset))
    erg.pop()
    return erg


def splitList(list):
    erg = []
    for elem in list:
        erg.insert(len(erg),[elem])
    return erg

def getStatsDataFrame(df,columnname,combinations,filterType,ergType,statsColumns):
    series = []
    names = []
    for combination in combinations:
        if(filterType=='equals'):
            filterErg = multipleFilter(df,[
                              lambda row: equalsFilter(row,columnname,combination)
                          ])
        elif(filterType=='or'):
            filterErg = multipleFilter(df,[
                              lambda row: orFilter(row,columnname,combination)
                          ])
        elif(filterType=='and'):
            filterErg = multipleFilter(df,[
                              lambda row: andFilter(row,columnname,combination)
                          ])
        if(ergType=='mean'):  
            ser = filterErg[statsColumns].mean(numeric_only=False)
        elif(ergType=='median'):  
            ser = filterErg.median(numeric_only=True)
        elif(ergType=='sum'):  
            ser = filterErg[statsColumns].sum(numeric_only=True)
        elif(ergType=='var'):  
            ser = filterErg[statsColumns].var(numeric_only=True)
        ser['count'] = filterErg['appid'].count()
        names.insert(len(names)-1,(','.join(combination))+" ("+str(ser['count'])+")")
        series.insert(len(series)-1,ser)

    erg = pd.concat(series, axis=1,keys=names).transpose().fillna(0)
    return erg


'''
Query Syntax: 
    1) one Query per row
    2) CSV formated, 3 Columns,  seperator=";", quotechar="'"
        filterType;Column;[item1,item2,...]
filterTypes:
    for List columns:
        and => all items must be in the game
        or => one of the item must be in the game
        not => none of the items must be in the game
        equals => excat these items items must be in the game 
                  (order does not matter)
    for single Value columns:
        smaller => game must be smaller than item
        bigger => game must be bigger than item#
        same => item and game must match
        notSame => item and game must be different
Examples:
or;'platforms';[linux,mac]
or;'categories';[Single-player]

return list of lambda
'''
def parseFilterTextField(text):
    #('parseFilterTextField')
    try:
        csvResource = StringIO(text)
        filterDF = pd.read_csv(csvResource, sep=";",quotechar="'",header=None,names=['filterType','column','filterItems'])
        #handleMultipleItemColumn2(filterDF,'filterItems',',')
        erg = []
        for index, dfrow in filterDF.iterrows():
            filterType = dfrow['filterType']
            column = dfrow['column']
            filterItems = dfrow['filterItems']
            #print(filterType+" " + column + " " +str(filterItems))
            if(filterType == 'or'):
                erg.append(lambda r,column=column,filterItems=filterItems: orFilter(r,column,convertToList(filterItems)))
            elif (filterType == 'and'):
                erg.append(lambda r,column=column,filterItems=filterItems: andFilter(r,column,convertToList(filterItems)))
            elif (filterType == 'not'):
                erg.append(lambda r,column=column,filterItems=filterItems: notFilter(r,column,convertToList(filterItems)))
            elif (filterType == 'equals'):
                erg.append(lambda r,column=column,filterItems=filterItems: equalsFilter(r,column,convertToList(filterItems)))

            elif (filterType == 'smaller'):
                erg.append(lambda r,column=column,filterItems=filterItems: smallerFilter(r,column,convertToNumber(filterItems)))
            elif (filterType == 'bigger'):
                erg.append(lambda r,column=column,filterItems=filterItems: biggerFilter(r,column,convertToNumber(filterItems)))

            elif (filterType == 'same'):
                erg.append(lambda r,column=column,filterItems=filterItems: sameFilter(r,column,convertToNumber(filterItems)))
            elif (filterType == 'notSame'):
                erg.append(lambda r,column=column,filterItems=filterItems: notSameFilter(r,column,convertToNumber(filterItems)))
        
        return erg
    except:
        return []

def handleMultipleItemColumn2(df,column,sep):
    df[column+"_list"] = df[column].apply(lambda x: x[1:-1].split(sep))

def convertToList(str):
    return str[1:-1].split(",")

def convertToNumber(str):
    try:
        if(str[0] == "'" and str[-0] == "'"):
            return str[1:-1]
        if("." in str):
            return float(str)
        else:
            return int(str)
    except:
        return str