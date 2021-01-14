import itertools
import pandas as pd


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
