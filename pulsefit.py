import admin
import bookingofficer
import customer_manager
import accountant



def main_menu():
    while True:
        print("=========== PULSEFIT STUDIO STAFF PANEL ===========")
        print("1. Admin menu")
        print("2. Booking officer menu")
        print("3. Customer management menu")
        print("4. Accountant menu")
        print("5. Clock out")

        option = input("What ya up to: ")

        if option == "1":
            admin.admin_menu()
        elif option == "2":
            bookingofficer.booking_menu()
        elif option == "3":
            customer_manager.customer_menu()
        elif option == "4":
            accountant.accountant_menu()
        elif option == "5":
            print("\n Work's done, go lepak at the mamak my friend!")
            break
        else:
            print("\n You can't choose that.\n")

if __name__ == "__main__":
    main_menu()
     
        
              