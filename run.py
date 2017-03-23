import sys
import getopt
import csv
from ua_parser import user_agent_parser


def parse_file(input_file_path, output_file_path):
    """ read input file and parse each user agent string to get browser name and main version

    Args:
      input_file_path: the path of the input file
        
    """
    with open(input_file_path, 'r') as f1, open(output_file_path, 'a') as f2:
        reader = csv.reader(f1, delimiter='\t')
        writer = csv.writer(f2, delimiter='\t')
        count = 0
        correct_count = 0
        incorrect_count = 0
        error_count = 0
        for row in reader:
            count += 1        

            user_agent_string = row[0]
            true_browser_name = row[1]
            true_main_version = row[2]
            try:                        
                result_dict = user_agent_parser.ParseUserAgent(user_agent_string)
                browser_name = result_dict['family']
                main_version = result_dict['major']

                #correct browser name and main version for some special cases
                browser_name, main_version = correct_special_cases(user_agent_string, browser_name, main_version)

                if browser_name == true_browser_name and main_version == true_main_version:
                    correct_count += 1
                else:
                    #print(user_agent_string)
                    #print(true_browser_name, true_main_version, browser_name, main_version)
                    #print(" ")   
                    incorrect_count += 1

                writer.writerow([user_agent_string, true_browser_name, true_main_version, browser_name, main_version])    

            except Exception as e:
                error_count += 1
                print(type(e))
                print(e)
                print(user_agent_string)
                print(result_dict)
                #print(parser.simple_detect(user_agent_string))
                print(true_browser_name, ", ", true_main_version)
                print("  ")


            #if count > 100000:
            #    break    

        #print(count, correct_count, incorrect_count, error_count)   
        print("Total number of user agents processed: ", count)
        print("correct number: ", correct_count)
        print("incorrect number: ", incorrect_count)
        print("number of records unable to handle: ", error_count)     

def correct_special_cases(user_agent_string, browser_name, main_version):
    """ process some special conditions that are not correct from user_agent_parser

    Args:
      user_agent_string: user agent string
      browser_name: the parsed browser name
      main_version: the parsed main browser version
    Return:
      (revised_browser_name, revised_main_version)  
    """
    if browser_name == "Apple Mail":
        return "AppleMail", main_version
    if (browser_name == "Safari" or browser_name == "Mobile Safari") and main_version is None:
        return browser_name, "None"
    if browser_name == "UC Browser":
        if user_agent_string.find("CriOS") > -1:
            return "Chrome Mobile iOS", user_agent_string.split("CriOS/")[-1].split(".")[0].strip()  
        if user_agent_string.find("Chrome") > -1:
            if user_agent_string.find("Mobile") == -1:
                return "Chrome", user_agent_string.split("Chrome/")[-1].split(".")[0].strip()  
            #else:
            #    return "Chrome Mobile", user_agent_string.split("Chrome/")[-1].split(".")[0].strip()     
        if user_agent_string.find("MSIE") > -1:
            return "IE", user_agent_string.split("MSIE")[-1].split(".")[0].strip()     
        if user_agent_string.find("Opera Mini") > -1:  
            return "Opera Mini", user_agent_string.split("Opera Mini/")[-1].split(".")[0].strip()  
        if user_agent_string.find("UCNewsApp") > -1:  
            return "Android", user_agent_string.split("Android")[-1].split(".")[0].strip()       
    if browser_name == "Outlook" and user_agent_string.find("MSIE") > -1:
        return "IE", user_agent_string.split("MSIE")[-1].split(".")[0].strip()
    if browser_name == "Samsung Internet":
        if user_agent_string.find("Mobile") > -1:    
            return "Chrome Mobile", user_agent_string.split("Chrome/")[-1].split(".")[0].strip()  
        else:
            return "Chrome", user_agent_string.split("Chrome/")[-1].split(".")[0].strip()
    if browser_name == "Crosswalk":
        return "Chrome", user_agent_string.split("Chrome/")[-1].split(".")[0].strip()
    if browser_name == "Iron":
        return "Chrome", user_agent_string.split("Chrome/")[-1].split(".")[0].strip()
    if browser_name == "MobileIron":
        return "Chrome Mobile", user_agent_string.split("Chrome/")[-1].split(".")[0].strip()    
    if browser_name == "Dragon":
        return "Chrome", user_agent_string.split("Chrome/")[-1].split(".")[0].strip() 
    if browser_name == "Baidu Browser":
        return "Chrome Mobile", user_agent_string.split("Chrome/")[-1].split(".")[0].strip()
    if browser_name == "Chrome Mobile":
        if user_agent_string.find("Chrome") > user_agent_string.find("Safari"):
            return "Chrome", main_version
        if user_agent_string.find("coc_coc_browser") > -1:
            return "Chrome", main_version    
    if browser_name == "Chrome" and user_agent_string.find("CrMo/") > -1:   
        return "Chrome Mobile", main_version
    if browser_name == "BacaBerita App":
        return "Android", user_agent_string.split("Android")[-1].split(".")[0].strip() 
    if browser_name == "Electron":
        return "Chrome", user_agent_string.split("Chrome/")[-1].split(".")[0].strip()        
    #if browser_name == "Maxthon" and user_agent_string.find("WOW") == -1:
    #    return "Chrome", user_agent_string.split("Chrome/")[-1].split(".")[0].strip()

    return browser_name, main_version

def usage():
    """  print command line usage information
    
    Appears when user specify -h or incorrect flags when running in command line
    """
    print('python run.py [-i <inputfile> | --input-data <inputfile>] [-o <outputfile> | --output-data <outputfile>] [-h]')
    print("It is required to specify input file path and output file path in the argument list")
    print("-i <inputfile>               : short flag for input file")
    print("--input-data <inputfile>     : long flag for input file")
    print("-o <outputfile>              : short flag for output file")
    print("--output-data <outputfile>   : long flag for output file")
    print("-h                           : print help information")

def main(argv):
    """ main function for the task

    Args:
        argv: a list of arguments from the command line except the first python script name
    
    if the user doesn't provide the correct arguments, the program will print help information and exit
    """
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["input-data=","output-data="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(1)
        elif opt in ("-i", "--input-data"):
            inputfile = arg
        elif opt in ("-o", "--output-data"):
            outputfile = arg
    if not inputfile or not outputfile:
        usage()
        sys.exit(1)

    parse_file(inputfile, outputfile)    

if __name__ == "__main__":
    main(sys.argv[1:])

