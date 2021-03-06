# Notes

My notes during the developpement of the script.

## 1. Information Gathering

### FireEye article: Obfuscated Command Line Detection Using Machine Learning

https://www.fireeye.com/blog/threat-research/2018/11/obfuscated-command-line-detection-using-machine-learning.html  

> The traditional pattern matching and rule-based approaches for detecting 
> obfuscation are difficult to develop and generalize, and can pose a huge 
> maintenance headache for defenders

> The purpose of obfuscation is two-fold:
>   1. Make it harder to find patterns in executable code, strings or scripts that can easily be detected by defensive software.
>   2. Make it harder for reverse engineers and analysts to decipher and fully understand what the malware is doing.

Traditionnal approaches for Obfuscation Detection:
  - write a large number of complex regular expressions  
    (match most common syntax: not all)  
    > virtually impossible to develop regular expressions to cover every possible abuse of the command line  
    <!-- -->
    > a determined attacker can make minor modifications to avoid the regular expressiona determined attacker can make minor modifications to avoid the regular expression  
  - writing complex if-then rules  
    > these rules are hard to derive, are complex to verify
  - combine regular expressions and if-then rules  
    > greatly complicates the development and maintenance burden  
    <!-- -->
    > [still possible to] escape detection by such rules  
    <!-- -->
    > still suffers from the same weaknesses that make the first two approaches fragile


The ML Approach: 
> illustrate two ML approaches: a feature-based approach and a feature-less end-to-end approach.

>Data and Experiments
>
>To develop our models, we collected non-obfuscated data from tens of thousands of endpoint events and generated obfuscated data using a variety of methods in Invoke-DOSfuscation. We developed our models using roughly 80 percent of the data as training data, and tested them on the remaining 20 percent. We ensured that our train-test split was stratified. For featureless ML (i.e. neural networks), we simply input Unicode code points into the first layer of the CNN model. The first layer converts the code point into semantically meaningful numerical representations (called embeddings) before feeding it into the rest of the neural network.  
>
>For the Gradient Boosted Tree method, we generated a number of features from the raw command lines. The following are some of them: 
>> Length of the command line  
>> The number of carets in the command line  
>> The count of pipe symbols  
>> The fraction of white space in the command line  
>> The fraction of special characters  
>> Entropy of the string  
>> The frequency of the strings “cmd” and “power” in the command line
>
>While each of these features individually is a weak signal and could not possibly be a good discriminator on its own, a flexible classifier such as a Gradient Boosted Tree – trained on sufficient data with these features – is able to classify obfuscated and non-obfuscated command lines in spite of the aforementioned difficulties.


### Obfuscation Techniques

#### cynet article
https://www.cynet.com/attack-techniques-hands-on/powershell-obfuscation-demystified-series-chapter-1-intro/

> The most common PowerShell obfuscation techniques are:
> 1. Concatenation – split strings into multiple parts which are concatenated through the “+” operator for example.  
>> $a = “http://malware.com/cybad.exe”  
>> $b = (‘h’+’ttp://ma’+’lware.com/cybad.exe’)  
> 2. Reordering– formatting operator (-f), the string is divided in several parts and will reorder by the (-f).  
>> “{1}{0}” -f ‘x’,’IE’
> 3. Escaping character– escape character (\`) will try to trick the analyst to understand the command, they are typically inserted into the middle of the string  
>> http://malware.com/cybad.exe à $a = (“http://mal`ware.c`om.cy`bad.ex`e”)
> 4. Base64 format– (–EncodedCommand) accepts a base-64 encoded string.  
>> Start-Process “dir “c:\passwords”” à ZABpAHIAIAAiAGMAOgBcAHAAYQBzAHMAdwBvAHIAZABzACIAIAA=0g  
>> powershell.exe -encodedCommand ZABpAHIAIAAiAGMAOgBcAHAAYQBzAHMAdwBvAHIAZABzACIAIAA=  
> 5. Up\Low case– random uppercase or lowercase in the script.  
> 6. white spaces– random white spaces are inserted between words.

#### Research article: PowerDrive: Accurate De-Obfuscation andAnalysis of PowerShell Malware
https://pralab.diee.unica.it/sites/default/files/dimva19-paper76-final.pdf

Three  types  of  obfuscation  layers  are  typically  employed  byPowerShellmalware:
  - String-related. In this case, the term string refers not only to constantstrings on which method calls operate, but also to cmdlets, function param-eters, and so forth. Strings are manipulated so that their reading is madesignificantly more complex.  
  - Encoding. This  strategy  typically  featuresBase64or  binary  encodings,which are typically applied to the whole script.  
  - Compression. As the name says, it applies compression to the whole script(or to part of it).  
Particular attention deserves the various obfuscation techniques related tothe String-based layer. They can be easily found in exploitation toolkits such as Metasploit or off-the-shelf tools, such asInvoke Obfuscation by Bohannon. In the following, we provide a list of the prominent ones.
  - Concatenation.A string is split into multiple parts which are concatenatedthrough the operator+.  
  - Reordering. A string is divided into several parts, which are subsequentlyreassembled through theformatoperator. 
  - Tick. Ticks are escape characters which are typically inserted into the middleof a string.
  - Eval. A string is evaluated as a command, in a similar fashion toevalinJavaScript. This strategy allows performing any string manipulation on thecommand.
  - Up-Low Case.Random changes of characters from uppercase to lowercaseor vice versa.
  - White Spaces. Redundant white spaces are inserted between words. 

Regular Expression to detect Base64 ecoded layers:  
```
$InputString -Match "^([ A-Za-z0-9 +/]{4}) *([ A-Za-z0-9 +/]{4}|[A-Za-z0-9 +/]{3}=|[ A-Za-z0-9 +/]{2}==)$")
```

#### Maz Kersten article: PowerShell string formatting deobfuscation
https://maxkersten.nl/binary-analysis-course/analysis-scripts/automatic-string-formatting-deobfuscation/

Found multiple regex to de-obfuscate powershell commands when:
  - using backticks
  - using string concatenation
  - using string formatting


### Machine Learning Specifics
#### Text Data to numbers
https://medium.com/fintechexplained/nlp-text-data-to-numbers-d28d32294d2e

## 2. Input Data Observations
Obfuscation techniques used (quick visual scan):  
  - backticks
  - up/low case
  - string formatting
  - string concatenation
  - did not spot redundant white spaces
  - did not spot base64 encoding

## 3. Problem with the data and possible solutions
Problem: ML algorithms work on numeric data.  
String analysis: need a way to translate strings into numeric format, and find a 
way work on this data (keep semantic, and so on)

### Feature Machin Learning
Define a number of features and work on them (see fireeye article).  
Features that can be used:
  - Length of the command line  
  - The number of carets in the command line  
  - The count of pipe symbols  
  - The fraction of white space in the command line  
  - The fraction of special characters  
  - Entropy of the string  
  - The frequency of the strings “cmd” and “power” in the command line
  - Inclusion of -f or -F

### Hack?
Use a deobfuscation tool on every command line  
Compute the distance between the source and result string  
Use the lenght of source, lenght of result and distance with ML algorithms

### Translate strings into numeric data
1. Hash the strings  
   https://medium.com/value-stream-design/introducing-one-of-the-best-hacks-in-machine-learning-the-hashing-trick-bf6a9c8af18f
2. Dimensionality Reduction:  
   https://towardsdatascience.com/still-parsing-user-agent-strings-for-your-machine-learning-models-use-this-instead-8928c0e7e74f  
   Use algorithm to translte string into a vector of fixed size (hopefully)
   keeping features of the strings, and minimizing the loss of information  
   used in article: fastText algorithm
3. Multiple solutions named in this article  
   https://dzone.com/articles/handling-character-data-for-machine-learninghttps://dzone.com/articles/handling-character-data-for-machine-learning  
   Label encoding  
   One hot encoding  
   Frequency-based encoding  
   Target mean encoding  
   Binary encoding  
   Hash encoding  
   link to other techniques: http://www.willmcginnis.com/2015/11/29/beyond-one-hot-an-exploration-of-categorical-variables/


## 4. Implementation tests
### a. character based
Used article: https://machinelearningmastery.com/develop-character-based-neural-language-model-keras/
to encode strings (test3) and https://machinelearningmastery.com/machine-learning-in-python-step-by-step/
to test multiple featureless machin learning models.  
The best tested model was DecisionTreeClassifier with an accuracy >92%.  
Some model got really low (~50%) accuracy: i think i missed something, or maybe 
the models were not adapted to this kind of problem...  

Notes:
  - vector size might be an issue
  - found techniques to reduce vector size
  - embedding
  - dimensionality reduction

Might want to use reduction techniques for further tesing

### b. Feature Based
https://aaltodoc.aalto.fi/bitstream/handle/123456789/43575/master_Pogosova_Mariam_2020.pdf?sequence=1&isAllowed=y

Manual feature extraction:
  - extracted features presented in the fireeye article
  - tested multiple models with encouraging results
  - 97%+ accuracy for a couple of models
  - code in test5

### c. Confidence intervals
https://machinelearningmastery.com/machine-learning-in-python-step-by-step/
https://towardsdatascience.com/how-to-add-confidence-intervals-to-any-model-7bbb9f80fd9c

test6

### d. Prediction intervals
test7 -> abandonned for more urgent matters: implemented in test9

### e. Save and Load models
https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/  
implemeted in test8 (using joblib instead of pickle presented in the article)


## 5. Analysis
### Models
### Feature vs Featureless
### Features

