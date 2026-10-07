"""
Customer Manage Python Part↓
"""
CID_INIT="M26"
customer_init="members.txt"
def customer_load(customer_path:str)->list:
    while(True):
        customer_list=[]
        try:
            with open(customer_path,"r") as readed_file:
                for i in readed_file:
                    i=i.strip()
                    customer_list.append(i.split(","))
                    #print(customer_list)
            return customer_list
        except FileNotFoundError as e:
            with open(customer_path,"w") as created_file:
                print("File not found, created automatically:",created_file)
        except Exception as e:
            print(repr(e))
            raise Exception
            #print(e)
def customer_add():
    existing_customer=customer_load(customer_init)
    while(True):
        #INIT
        preparing_list=[]
        #Workflow
        Full_CID=CID_workflow()
        preparing_list.append(Full_CID)
        #CID ENDED
        NAME=NAME_workflow()
        preparing_list.append(NAME)
        #NAME ENDED
        PhoneNumber=PhoneNumber_workflow()
        preparing_list.append(PhoneNumber)
        #PHONE NUMBER ENDED
        email_merge=email_workflow()
        preparing_list.append(email_merge)
        print("All information collected")
        append_file(preparing_list,customer_init)
        result=input("Still input new customer?(y\\n)"+"\n").strip()
        if result == "N" or result == "n":
            break
def customer_update():
    while(True):
        try:
            existing_customer=customer_load(customer_init)
            select=input("what info you're trying to update?(ID, NAME, PHONE, EMAIL)"+"\n")
            #if select not in ["ID","NAME","PHONE","EMAIL"]:
            if select == "ID":
                Find_CID=input("Input the ID you want to find"+"\n")
                if not information_check(Find_CID,existing_customer):
                    continue
                CID=input("Input the ID you want to update(8 len only)"+"\n")
                if not CID_Check(CID,CID_INIT+CID,existing_customer):
                    print("Something wrong with the ID, please try again")
                    continue
                information_update(Find_CID,CID_INIT+CID,existing_customer)
            elif select == "NAME":
                Find_NAME=input("Input the name you want to find"+"\n")
                if not information_check(Find_NAME,existing_customer):
                    continue
                NAME=input("Input the name you want to update"+"\n")
                if not NAME_Check(NAME):
                    print("Something wrong with the name, please try again")
                    continue
                information_update(Find_NAME,NAME,existing_customer)
            elif select == "PHONE":
                Find_PHONE=input("Input the phone number you want to find"+"\n")
                if not information_check(Find_PHONE,existing_customer):
                    continue
                PHONE=input("Input the phone number you want to update(10 lens number)"+"\n")
                if not PhoneNumber_Check(PHONE):
                    print("Something wrong with the phone number, please try again")
                    continue
                information_update(Find_PHONE,PHONE,existing_customer)
            elif select == "EMAIL":
                Find_EMAIL=input("Input the email you want to find"+"\n")
                if not information_check(Find_EMAIL,existing_customer):
                    continue
                EMAIL=email_workflow()
                information_update(Find_EMAIL,EMAIL,existing_customer)
            else:
                print("Wrong input, please try again")
                continue
            rewrite_file(existing_customer,customer_init)
            result=input("Still update new customer?(y\\n)"+"\n").strip()
            if result == "N" or result == "n":
                break
        except Exception as e:
            print(repr(e))
def information_check(information:str,existing_customer:list):
    for list_customer in existing_customer:
        if information in list_customer:
            print("information existed")
            return True
    print("Information not existed")
    return False
def information_update(old_information:str,new_information:str,existing_customer:list):
    for list_customer in existing_customer:
        if old_information in list_customer:
            list_customer[list_customer.index(old_information)] = new_information
            break
def CID_workflow():
    while(True):
        try:
            CID=input("Input any number(8 len only)"+"\n")
            Full_CID=CID_INIT+CID
            if CID_Check(CID,Full_CID,customer_load(customer_init)):
                return Full_CID
            else:
                continue
        except Exception as e:
            print(repr(e))

def CID_Check(CID,Full_CID,existing_customer)->bool:
    if not len(CID) == 8:
        print("OVER or LESS 8 len number!")
        return False
    if not CID.isdecimal():
        print("Not fully number!")
        return False
    if check_exist(existing_customer,Full_CID,"ID"):
        return False
    return True

def NAME_workflow():
    while(True):
        try:
            NAME=input("Input any name"+"\n").strip()
            if NAME_Check(NAME):
                return NAME
            else:
                continue
        except Exception as e:
            print(repr(e))

def NAME_Check(name)->bool:
    if not name.isalpha():
        print("Something wrong with the name!")
        return False
    return True

def PhoneNumber_workflow():
    while(True):
        try:
            PhoneNumber=input("Input phone number(10 lens number)"+"\n").strip()
            if PhoneNumber_Check(PhoneNumber):
                return PhoneNumber
            else:
                continue
        except Exception as e:
            print(repr(e))

def PhoneNumber_Check(phone_number)->bool:
    if not len(phone_number) == 10:
        print("OVER or LESS 10 len number!")
        return False
    if not phone_number.isdecimal():
        print("Not fully number!")
        return False
    return True

def email_workflow():
    while(True):
        try:
            email_prefix = input("Input email prefix(Only the string ahead of @xx.com)"+"\n").strip()
            email_provider = input("Input email provider(Only the string between @ and .com)"+"\n").strip()
            email_merge = email_prefix.strip()+"@"+email_provider.strip()+".com"
            return email_merge
        except Exception as e:
            print(repr(e))

def check_exist(list,input_data,duplicated_name:str)->bool:
    for one_d in list:
        if one_d[0] == input_data:
            print(duplicated_name+" is existed!")
            return True
    return False

def append_file(new_customer_data:list,customer_path:str):
    with open(customer_path,"a") as readed_file:
        number=readed_file.write(",".join(new_customer_data)+"\n")
        print(f"write {number} numbers of data into file")

def rewrite_file(customer_data:list,customer_path:str):
    with open(customer_path,"w") as readed_file:
        for list in customer_data:
            print(list)
            readed_file.write(",".join(list)+"\n")

def customer_menu():
    while(True):
        print("===== CUSTOMER MANAGEMENT =====")
        print("1. Add Customer")
        print("2. Update Customer")
        print("3. Back to Main Menu")

        choice = input("Select your option: ")

        if choice == "1":
            customer_add()
        elif choice == "2":
            customer_update()
        elif choice == "3":
            break
        else:
            print("\nInvalid option, please try again.\n")


#debug↓
if __name__ == "__main__":
    #testlist = customer_load(customer_init)
    #rewrite_file(testlist,customer_init)
    #customer_add()
    customer_update()

