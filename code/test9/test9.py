# make predictions
import pandas as pd
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import joblib


# get features of a string
def get_features(string):
    features_nb = 9
    features = [0] * features_nb
    features[0] = len(string)
    for char in string:
        if char.isupper(): features[1] += 1
        if char in ["%", "*", "/", "+", "-", "=", "<", ">"]: features[2] += 1
        if char == ' ': features[3] += 1
        if char in ' !\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~': features[4] += 1
        if char == '|': features[6] += 1
        if char == '^': features[7] += 1
    features[5] = string.count("cmd") + string.count("power")
    features[8] = string.count("-f") + string.count("-F")
    for i in range(1, features_nb):
        features[i] /= features[0]
    #print(features)
    return features


model_file = '../test8/lda_trained.sav'

# Examples non-obfuscated
cmd_line = 'ping 172.16.3.2'
#cmd_line = '"C:\Program Files (x86)\Google\Chrome\Application\81.0.4044.129\Installer\setup.exe" --type=crashpad-handler /prefetch:7 --monitor-self-annotation=ptype=crashpad-handler --database=C:\Windows\TEMP\Crashpad --url=https://clients2.google.com/cr/report --annotation=channel= --annotation=plat=Win64 --annotation=prod=Chrome --annotation=ver=81.0.4044.129 --initial-client-data=0x210,0x214,0x218,0x1ec,0x21c,0x7ff7471176a0,0x7ff7471176b0,0x7ff7471176c0'
# Examples obfuscated
#cmd_line = '&("{0}{1}"-f \'pin\',\'g\') ("{2}{0}{1}" -f \'1\',\'00\',\'192.168.5.\')'
#cmd_line = '${c`OMp}=[adsi]"WinNT://$($env:ComputerName)"'

# Examples from the fireeye article (obfuscated)
#cmd_line = 'cmd.exe /v/r "set 9S=e3zo Hi Vi3tor and Vikray!&setZq=!9S:3=c!&set ZYk9=!Za:y=m!&set rQ2=!ZYk9:z=h&&cmd /r %rQ2%'
#cmd_line = 'cmd /r "set a=tat -ano&set b=nets&cmd /r %b%%a%'
#cmd_line = 'cmd /v /r "set a=ona- tatsten&for /L %b in (11 -1 0) do set c=!c!!a:~%b,1!&if %b equ 0 call %c:~3%'
## Examples from the fireeye article (seems obfuscated but are not)
#cmd_line = "cmd.exe /c 'C:\\windows\\system32\\3636363bsdshshshshsGF@#&()_____.737.473783873.bat"
#cmd_line = 'cmd \c echo nbt_local > C:\\windows\\temp\\nessus_L571HG8Q.txt & netstat -n >> C:\\windows\\temp\\nessus_L571HG8Q.txt & eho nbt_cache >> C:\\windows\\temp\\nessus_L571HG8Q.txt & nbtstat -c >> C:\\windows\\temp\\nessusL_571HG8Q.txt & echo nbt_session_ip >> C:\\windows\\temp\\nessusL_571HG8Q.txt & nbtstat -S >> C:\\windows\\temp\\nessusL_571HG8Q.txt & nbt_session_name >> C:\\windows\\temp\\nessusL_571HG8Q.txt & nbtstat -s >> C:\\windows\\temp\\nessusL_571HG8Q.txt'


###############################################################################
# feature extraction
features = []
features.append(get_features(cmd_line))

###############################################################################
# create dataset
names = ['length', 'upper', 'operator', 'white', 'special', 'cmdpower', 'pipe', 
        'carets', 'fF']
dataset = pd.DataFrame.from_records(features, columns=names)

###############################################################################
# Load trained model
model = joblib.load(model_file)

###############################################################################
# make predictions
predictions = model.predict(dataset)
proba = model.predict_proba(dataset)


###############################################################################
# print results
if predictions == 1: 
    print('prediction: obfuscated')
    print('confidence: ' + str(proba[0][1]*100) + '%')
else: 
    print('prediction: non-obfuscated')
    print('confidence: ' + str(proba[0][0]*100) + '%')
