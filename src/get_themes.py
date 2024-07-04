
# confirm the passed in csv files have all the above theme labels as well as make sure there are 10, and only 10, theme labels 
# the theme labels are (specifications, remote, connections, coordinates, moving, actuator, programming, error, timing, incoming)
def getAllMajorThemeLabels(robotCodedData):
    allMajorThemes = set()
    allSubThemes = getAllSubThemeLabels(robotCodedData)
    themesAndSubThemesDict = {'Specifications': ['api', 'hr', 'os', 'lu'], 
                              'Remote': ['wireless', 'cpmr'],
                              'Connections': ['internet', 'wpi', 'sc'],
                              'Coordinates': ['position', 'orientation'],
                              'Moving': ['mp', 'obstacles', 'mapping', 'SLAM'],
                              'Actuator': ['ik', 'hc', 'wc', 'mc', 'balance'],
                              'Programming': ['pointers', 'dt', 'overflow', 'list'],
                              'Error': ['li', 'bf'],
                              'Timing': ['timing', 'multithreading', 'rg'],
                              'Incoming': ['cameras', 'vision', 'line tracking', 'sensors'],
                              'Other' : ['fp', 'gs', 'bp', 'repeat', 'decoupling', 'install', 'ra', 'ros', 'rn', 'dl', 'rl', 'dc', 'distance']}
    
    # make sure all subThemes from Appendix A are in the dataset
    for theme in themesAndSubThemesDict.keys():
        allMajorThemes.add(theme)
        for subTheme in themesAndSubThemesDict[theme]:
            if subTheme not in allSubThemes.values():
                print(f"Subtheme `{subTheme}` (from Appendix A) not found in the dataset")

    # make sure all subThemes from dataset are in Appendix A
    for subTheme in allSubThemes.items():
        found = False
        for theme in themesAndSubThemesDict.keys():
            if subTheme[1] in themesAndSubThemesDict[theme]:
                found = True
                break
        if not found:
            print(f"Subtheme (from dataset) `{subTheme[1]}` at index {subTheme[0]} (probably line {subTheme[0] + 2}) not found in the theme dictionary (Appendix A)")
    

def getAllSubThemeLabels(robotCodedData):
    allSubThemes = {}
    for index, row in robotCodedData.iterrows():
        if pd.isna(row["code"]):
            print(f"Cell for codes at index {index} (probably line {index + 2}) is empty")
        else:        
            code = row["code"]
            allSubThemes[index] = code
    return allSubThemes