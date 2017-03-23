

Approach:

After I got the task, I first start to think about ways to solve the problem. The problem is to extract the browser name and main version number from the user agent string. As the input is completely text, not numerical features, it is not appropriate to directly apply machine learning models. Then I am thinking that one possible way is to parse the user agent string and apply regular expression pattern matching to decide what the browser name and main version is from the user agent string. So I search on line and check if there are some existing implementations. I find the following two tools for user agent parsing.

Httpagentparser
http://shon.github.io/httpagentparser/

ua-parser
https://github.com/ua-parser/uap-python

After I evaluate the two tools on the given data_coding_exercise.txt input, and compare the parsed result with the ground truth, I find the ua-parser tool has higher accuracy. ua-parser uses the YAML file with long-time collected regular expression patterns from the core of BrowserScope's original user agent string parser. For the 421215 input user agent strings, the tool predicted 418627 records correctly. The accuracy rate is 99.39%. 

Then I try to find the patterns for the wrong prediction and write code to correct these special cases. To avoid the risk of over-fitting, I use the first 30000 user agent string as my training set, and try to improve the accuracy on the training set by applying the special pattern post-processing. The patterns are as below. On the left side of the arrow is the tool-predicted result, and on the right side of the arrow is the ground truth result. The possible conditions for these special case conversion is in the parenthesis. My program post-process and correct these special cases when the conditions are satisfied. The post-processing can definitely improve the accuracy on the training set. Moreover, when I run the program on the remaining user agent data (as validation set), I find the accuracy is also improved. This convinces me that the post-processing is useful. After I run the program with the post-processing for these special cases on the entire data set, my program can predict 421124 records correctly and the accuracy rate becomes 99.98%. 


Apple Mail -> AppleMail   (easy to do)
Safari None -> Safari None  (None object to string 'None')
Mobile Safari None -> Mobile Safari None  (None object to string 'None')
UC Browser 10  ->  Chrome Mobile iOS 23  (there is CriOS,  Mobile keyword, UCBrowser in the end)
UC Browser 4 -> Chrome 38  (there is no Mobile keyword)
UC Browser 5 -> IE 9  (there is MSIE keyword)
UC Browser 10 -> Opera Mini 7  (there is Opera Mini keyword)
Outlook 2010 -> IE 7  (there is MSIE keyword)
Samsung Internet 3 -> Chrome Mobile 38   (has Mobile keyword)
Samsung Internet 4 -> Chrome 44  (no Mobile keyword)
Crosswalk 18 -> Chrome 48   (both with or without Mobile keyword)
Iron 50 -> Chrome 50
Dragon 36 -> Chrome 36
Baidu Browser 7 -> Chrome Mobile 35
MobileIron 1 -> Chrome Mobile 47
Chrome Mobile -> Chrome   (Chrome appears at last position, )
Chrome 16 -> Chrome Mobile 16  （there is CrMo keyword)
UC Browser 1 -> Android 5    (there is UCNewsApp, U3 keyword, and Android keyword)
Chrome Mobile 51 -> Chrome 51   (there is coc_coc_browser keyword)


Discussion:
The post-processing can increase the accuracy for the input data set. But this post-processing optimization takes time, so the downside of it is that the efficiency of the program is decreased. Furthermore, the accuracy increase from 99.39% to 99.98% is not significant, so if the accuracy of 99.39% is acceptable, then the post-processing is not needed. To disable post-processing in the program, just comment the line 33, and not call correct_special_cases function.


How to run:

First, you need to install the ua-parser tool (use sudo if permission denied) 
$ pip install ua-parser

Then run the program by:
$ python run.py --input-data <inputfilepath> --output-data <outputfilepath>

You can also use -i flag for input file, -o flag for output file. To see the details, you can enter
$ python run.py -h

I test my program using Python 3.5.2

The program also works for test_data_coding_exercise.txt or other input files with the same format.


