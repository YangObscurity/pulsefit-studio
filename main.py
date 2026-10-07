import admin
import customer_manage
import imgonnadie
import accountant

def main_menu():
   while True:
      print("===== PULSEFIT STUDIO =====")
      print("1. Admin")
      print("2. Booking Officer")
      print("3. Customer Management")
      print("4. Accountant")
      print("5. Exit")

      choice = input("Select your role: ")

      if choice == "1":
        admin.admin_menu()
      elif choice == "2":
        imgonnadie.booking_menu()
      elif choice == "3":
        customer_manage.customer_menu()
      elif choice == "4":
        accountant.accountant_menu()
      elif choice == "5":
        print("Goodbye!")
        break
      else:
        print("\nInvalid option, please try again.\n")
         
if __name__ == "__main__":
    while(True):
        try:
            main_menu()
        except Exception as e:
            print(repr(e))