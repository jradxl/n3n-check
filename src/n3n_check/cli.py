import os, sys, argparse, configparser
from littletable import Table

config_dir = "/etc/n3n"
filename1 = "edge.conf"
filename2 = "supernode.conf"
error_list = []

config_data = """\
ckey,category,datatype,required,default
tuntap.metric,tuntap,number,no,0
tuntap.mtu,tuntap,number,no,1290
tuntap.name,tuntap,alnum,yes,n3n0
community.name,community,alnum,yes,changeme
"""

catalog = Table("catalog")
catalog.create_index("ckey", unique=True)
catalog.csv_import(config_data)

def show_catalog():
    #print(catalog.info())
    catalog.present()

def doit(file):
    #print("In DOIT")
    error_list = []
    fullpath = os.path.join(config_dir,file)
    config_object = None
    config_object = configparser.ConfigParser(strict = True, inline_comment_prefixes=("#",";"))
    try:
        mylist = config_object.read(fullpath)
    except Exception as e:
        print("Config Exception: ", e)
        sys.exit(1)

    ## Returns an empty list if file can't be read,
    ## which causes old data to be reused.
    #print("MYLIST: " , mylist)
    if not mylist:
         return
    else:
         print(f"Processing {fullpath}")

    for section in config_object:
        #print("SECTION: ", section)
        for item in config_object[section]:
            ivalue = config_object[section][item]
            #print ("    AAA: ", item, ivalue)
            isNotNumber = False
            isBlank = False
            isNotAlphaNumeric = False

            if "\"" in ivalue:
                    error_list.append(f"{section} {item}: Value contains double inverted comma(s)")
            if "'" in ivalue:
                    error_list.append(f"{section} {item}: Value contains single inverted comma(s)") 

            row = catalog.where(ckey = section + "." + item )
            for i in row:
                #print("        BBB: ", i.ckey, i.datatype, i.required, ivalue)      
                match i.datatype:
                        case "number":
                            #print("NN", item, ivalue)
                            if not ivalue.isnumeric() and ivalue and not ivalue.isspace():
                                isNotNumber = True
                                error_list.append(f"{section} {item}: Value is not a Number")
                            if not ivalue:
                                isBlank = True
                        case "alnum":
                            #print("AN", item, ivalue)
                            if not ivalue.isalnum():
                                isNotAlphaNumeric = True
                                error_list.append(f"{section} {item}: Value is not Alphanumeric")
                            if not ivalue:
                                isBlank = True
                        case _:
                            error_list.append(f"{section} {item}: Uknown entry for Datatype field")
                match i.required:
                        case "yes":
                            if isBlank:
                                error_list.append(f"{section} {item}: Required but Value is blank")
                        case "no":
                            pass
                        case _ :
                            error_list.append(f"{section} {item}: Uknown entry for Required field")
            #For Loop End
        #For Loop End            
    if error_list:
        print(f"ERRORS for {file}:")
        for i in error_list:
            print(f"    {i}")
        print()
    else:
         print("PASS:")
         print("    No errors found.")
         print()

def main():

    parser = argparse.ArgumentParser(description="n3n VPN config file syntax checker")
    parser.add_argument('-s', '--show_catalog', action='store_true', required=False, help='show the Configuration Calalog hard coded into the program code.')
    args = parser.parse_args()

    print("Checking n3n config files...")
    print("Hard coded for '/etc/n3n/edge.conf' and '/etc/n3n/supernode.conf'")

    print()
    if args.show_catalog:
        show_catalog()

    isExist = os.path.exists(config_dir)   
    if not isExist:
        error_list.append(f"ERROR: Config directory, '{config_dir}' does not exist.")

    path = os.path.join(config_dir,filename1)
    isExist = os.path.isfile(path)
    if not isExist:
        error_list.append(f"ERROR: Config file, '{path}' does not exist.")

    path = os.path.join(config_dir,filename2)
    isExist = os.path.isfile(path)
    if not isExist:
        error_list.append(f"ERROR: Config file, '{path}' does not exist.")

    if error_list:
        print()
        print("ERRORS:")
        for i in error_list:
            print(f"    {i}")
        print()
        #sys.exit(1)

    print()
    doit(filename1)
    doit(filename2)

    print("Finished.")

if __name__ == "__main__":
    main()

