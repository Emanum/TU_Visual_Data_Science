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
    1) one Query per
    2) CSV formated, 3 Columns,  seperator=";", quotechar="'"
        filterType;Column;[item1,item2,...]
filterTypes:
    for List columns:
        and => all items must be in the game
        or => one of the item must be in the game
        not => none of the items must be in the game
        equals => excat these items items must be in the game (order does not matter)
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
    try:
        csvResource = StringIO(text)
        filterDF = pd.read_csv(csvResource, sep=";",quotechar="'",header=None,names=['filterType','column','filterItems'])
        #handleMultipleItemColumn2(filterDF,'filterItems',',')
        erg = []
        for index, row in filterDF.iterrows():
            if(row['filterType'] == 'or'):
                erg.append(lambda x1: orFilter(x1,row['column'],convertToList(row['filterItems'])))
            elif (row['filterType'] == 'and'):
                erg.append(lambda x2: andFilter(x2,row['column'],convertToList(row['filterItems'])))
            elif (row['filterType'] == 'not'):
                erg.append(lambda x3: notFilter(x3,row['column'],convertToList(row['filterItems'])))
            elif (row['filterType'] == 'equals'):
                erg.append(lambda x4: equalsFilter(x4,row['column'],convertToList(row['filterItems'])))

            elif (row['filterType'] == 'smaller'):
                erg.append(lambda x5: smallerFilter(x5,row['column'],convertToNumber(row['filterItems'])))
            elif (row['filterType'] == 'bigger'):
                erg.append(lambda x6: biggerFilter(x6,row['column'],convertToNumber(row['filterItems'])))

            elif (row['filterType'] == 'same'):
                erg.append(lambda x7: sameFilter(x7,row['column'],convertToNumber(row['filterItems'])))
            elif (row['filterType'] == 'notSame'):
                erg.append(lambda x8: notFilter(x8,row['column'],convertToNumber(row['filterItems'])))
        
        return erg
    except:
        return []

def handleMultipleItemColumn2(df,column,sep):
    df[column+"_list"] = df[column].apply(lambda x: x[1:-1].split(sep))

def convertToList(str):
    return str[1:-1].split(",")

def convertToNumber(str):
    try:
        if("." in str):
            return float(str)
        else:
            return int(str)
    except:
        return str