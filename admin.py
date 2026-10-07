classes_file = "classes.txt"
booking_file = "booking.txt"
payment_file = "payment.txt"

def read_classes():
    classes = [] 
    open(classes_file, "a").close()

    with open(classes_file, "r") as f:
        for line in f:
           line = line.strip()
           if line:
            classes.append(line.split(","))
    return classes

def write_classes(classes):
   with open(classes_file, "w") as f:
      for c in classes:
         f.write(",".join(c) + "\n")

def create_class_code(classes):
   if not classes:
      return "001"

   highest = 0
   for c in classes:
      if c[0].isdigit():
         number = int(c[0])
         if number > highest:
            highest = number
   return f"{highest + 1:03d}"

   
def add_class():
   classes = read_classes()
   name = input("Enter class name: ")
   trainer = input("Enter trainer name: ")
   time_slot = input("Enter time slot: ")

   while True:
      total_pax = input("Enter total pax: ")
      if total_pax.isdigit() and int(total_pax) > 0:
         break
      print("Please enter a valid number. Don't fool us like how you fool your gains.")

   new_code = create_class_code(classes)
   new_class = [new_code, name, trainer, time_slot, total_pax, "0"]
   classes.append(new_class)
   write_classes(classes)

   print(f"\nClass added successfully. Class code: {new_code}\n")


def view_classes():
   classes = read_classes()
   if not classes:
      print("\nNo classes found. \n")
      return 

   print(f"\n{'Code':<6}{'Name':<15}{'Trainer':<15}{'Time Slot':<12}{'Total Pax':<10}{'Booked':<8}")
   print("-" * 66)
   for c in classes: 
      class_code, name, trainer, time_slot, total_pax, booked = c 
      print(f"{class_code:<6}{name:<15}{trainer:<15}{time_slot:<12}{total_pax:<10}{booked:<8}")
   print()

def update_class():
   classes = read_classes()
   view_classes()
   class_code = input("Enter Class ID for update: ")

def find_class_by_code (classes, class_code):
      for c in classes:
         if c[0] == class_code:
            return c
         return None

def update_class():
   classes = read_classes()
   view_classes()
   class_code = input("Enter the Class Code to update: ")

   target = find_class_by_code(classes, class_code)
   if target is None:
      print("\nClass ID not found. \n")
      return 

   print("Leave a field blank to keep current value. ")
   name = input(f"New name [{target[1]}]: ")
   trainer = input(f"New trainer [{target[2]}]: ")
   time_slot = input(f"New time slot [{target[3]}]: ")
   total_pax = input(f"New total pax [{target[4]}]: ")

   if name:
      target[1] = name
   if trainer:
         target[2] = trainer
   if time_slot:
         target[3] = time_slot
   if total_pax:
      booked = int(target[5])
      if total_pax.isdigit() and int(total_pax) >= booked:
         target[4] = total_pax
      else:
         print ("That won't do. Must be a num >= current bookings 9{booked}. Old value saved.")

   write_classes(classes)
   print("\nClass updated successfully. \n")

def delete_class():
   classes = read_classes()
   view_classes()
   class_code = input ("Enter the Class ID to remove: ")

   target = find_class_by_code(classes, class_code)
   if target is None:
            print("\nClass ID not found. \n")
            return 

   if target[5] != "0":
      print(f"\n Cannot delete: this class has {target[5]} active booking(s). Cancel your active bookings before deleting. \n")
      return

   confirm = input(f"Do you want to remove '{target[1]}'? (y/n:): ")
   if confirm.lower() == "y":
      classes.remove(target)
      write_classes(classes)
      print("\nClass removed. \n")
   else:
      print("\nDeletion cancelled. \n")


def read_bookings():
   bookings = [] 
   open(booking_file, "a").close()

   with open(booking_file, "r") as f:
      for line in f:
         line = line.strip()
         if line:
            bookings.append(line.split(","))
   return bookings

def read_payments():
   payments = [] 
   open(payment_file, "a").close()

   with open(payment_file, "r") as f:
      for line in f:
         line = line.strip()
         if line:
            payments.append(line.split(","))
   return payments

def generate_report():
   classes = read_classes()
   bookings = read_bookings()
   payments = read_payments()

   print("\n===== OVERALL STUDIO REPORT =====")
   print(f"Total classes offered: {len(classes)}")
   print(f"Total bookings made: {len(bookings)}")

   if classes:
      most_popular = max(classes, key=lambda c: int(c[5]))
      print(f"Most popular class: {most_popular[1]} ({most_popular[5]} bookings)")

      all_pax = sum(int(c[4]) for c in classes)
      total_booked = sum(int(c[5]) for c in classes)
      if all_pax > 0:
         utilization = (total_booked / all_pax) * 100
         print(f"Overall capacity utilization: {utilization:.2f}%")

   if payments:
      total_income = sum(float(p[2]) for p in payments if p[3].lower() == "paid")
      print(f"Total income collected: RM{total_income:.2f}")
   else:
      print("Total income collected: (payment.txt not available yet)")

   print("==================================\n")




def admin_menu():
   while True:
      print("===== ADMIN MENU =====")
      print("1. Add Class")
      print("2. View Classes")
      print("3. Update Classes")
      print("4. Remove Classes")
      print("5. Generate Overall Report")
      print("6. Main Menu")

      option = input("Enter option: ")

      if option == "1":
         add_class()
      elif option == "2":
         view_classes()
      elif option == "3":
         update_class()
      elif option == "4":
         delete_class()
      elif option == "5":
         generate_report()
      elif option == "6":
         break
      else:
         print("\nInvalid option, please try again.\n")



if __name__ == "__main__":
   admin_menu()


members_file = "members.txt"
booking_file2 = "bookings.txt"

MAX_CLASS_CAPACITY = 20


def read_members():
   members = []
   open(members_file, "a").close()

   with open(members_file, "r") as f:
      for line in f:
         line = line.strip()
         if line:
            members.append(line.split(","))
   return members


def read_bookings():
   bookings = []
   open(booking_file2, "a").close()

   with open(booking_file2, "r") as f:
      for line in f:
         line = line.strip()
         if line:
            bookings.append(line.split(","))
   return bookings


def make_booking_id(bookings):
   if len(bookings) == 0:
      return "B001"
   nums = []
   for b in bookings:
      nums.append(int(b[0][1:]))
   biggest = max(nums)
   return "B" + str(biggest + 1).zfill(3)


def write_bookings(bookings):
   f = open(booking_file2, "w")
   for b in bookings:
      f.write(",".join(b) + "\n")
   f.close()


def make_member_id(members):
   if len(members) == 0:
      return "M001"
   nums = []
   for m in members:
      nums.append(int(m[0][1:]))
   biggest = max(nums)
   return "M" + str(biggest + 1).zfill(3)

def write_members(members):
   f = open(members_file, "w")
   for m in members:
      f.write(",".join(m) + "\n")
   f.close()

def register_member():
   members = read_members()
   name = input("Enter member name: ")
   contact = input("Enter contact number: ")

   while True:
      join_date = input("Enter join date (YYYY-MM-DD): ")
      if len(join_date) == 10 and join_date[4] == "-" and join_date[7] == "-":
         break
      print("That doesn't look like a real date bronion ring, try again. (use the dashes)")

   new_id = make_member_id(members)
   new_member = [new_id, name, contact, join_date]
   members.append(new_member)
   write_members(members)

   print(f"\nMember registered. Member ID: {new_id}\n")

def book_class():
   members = read_members()
   classes = read_classes()
   bookings = read_bookings()

   member_id = input("Enter your Member ID: ")
   found_member = None
   for m in members:
      if m[0] == member_id:
         found_member = m
   if found_member is None:
      print("\nNo such member. Register first.\n")
      return

   view_classes()
   class_code = input("Enter the Class Code to book: ")

   target_class = None
   for c in classes:
      if c[0] == class_code:
         target_class = c
   if target_class is None:
      print("\nClass ID not found.\n")
      return

   total_pax = int(target_class[4])
   booked_count = int(target_class[5])

   if total_pax > MAX_CLASS_CAPACITY:
      total_pax = MAX_CLASS_CAPACITY   # hard studio-wide cap, even if classes.txt says otherwise

   if booked_count >= total_pax:
      print(f"\nSorry, '{target_class[1]}' is full ({booked_count}/{total_pax}).\n")
      return

   new_booking_id = make_booking_id(bookings)
   new_booking = [new_booking_id, member_id, class_code, "2026-10-06", "BOOKED"]
   bookings.append(new_booking)
   write_bookings(bookings)

   target_class[5] = str(booked_count + 1)
   write_classes(classes)

   print(f"\nBooked! Booking ID: {new_booking_id}\n")


def reschedule_booking():
   bookings = read_bookings()
   booking_id = input("Enter the Booking ID to reschedule: ")

   target_booking = None
   for b in bookings:
      if b[0] == booking_id:
         target_booking = b

   if target_booking is None:
      print("\nBooking ID not found.\n")
      return

   if target_booking[4] != "BOOKED":
      print("\nOnly active bookings can be rescheduled.\n")
      return

   member_id = target_booking[1]

   print(f"\nCancelling old booking for Member {member_id}...")
   cancel_booking_internal(booking_id)

   print("Now pick your new class.\n")
   book_class_for_member(member_id)


def cancel_booking_internal(booking_id):
   bookings = read_bookings()
   classes = read_classes()

   target_booking = None
   for b in bookings:
      if b[0] == booking_id:
         target_booking = b

   target_booking[4] = "CANCELLED"
   write_bookings(bookings)

   class_code = target_booking[2]
   target_class = None
   for c in classes:
      if c[0] == class_code:
         target_class = c

   if target_class is not None:
      booked_count = int(target_class[5])
      if booked_count > 0:
         target_class[5] = str(booked_count - 1)
      write_classes(classes)


def book_class_for_member(member_id):
   classes = read_classes()
   bookings = read_bookings()

   view_classes()
   class_code = input("Enter the Class Code to book: ")

   target_class = None
   for c in classes:
      if c[0] == class_code:
         target_class = c
   if target_class is None:
      print("\nClass ID not found.\n")
      return

   total_pax = int(target_class[4])
   booked_count = int(target_class[5])
   if total_pax > MAX_CLASS_CAPACITY:
      total_pax = MAX_CLASS_CAPACITY

   if booked_count >= total_pax:
      print(f"\nSorry, '{target_class[1]}' is full ({booked_count}/{total_pax}).\n")
      return

   new_booking_id = make_booking_id(bookings)
   new_booking = [new_booking_id, member_id, class_code, "2026-10-06", "BOOKED"]
   bookings.append(new_booking)
   write_bookings(bookings)

   target_class[5] = str(booked_count + 1)
   write_classes(classes)

   print(f"\nBooked! New Booking ID: {new_booking_id}\n")

def view_bookings():
   bookings = read_bookings()
   members = read_members()
   classes = read_classes()

   if not bookings:
      print("\nNo bookings found.\n")
      return

   print(f"\n{'Booking ID':<12}{'Member':<15}{'Class':<15}{'Date':<12}{'Status':<10}")
   print("-" * 64)

   for b in bookings:
      booking_id, member_id, class_code, date, status = b

      member_name = member_id
      for m in members:
         if m[0] == member_id:
            member_name = m[1]

      class_name = class_code
      for c in classes:
         if c[0] == class_code:
            class_name = c[1]

      print(f"{booking_id:<12}{member_name:<15}{class_name:<15}{date:<12}{status:<10}")
   print()


def view_attendance_history():
   member_id = input("Enter Member ID to view history: ")
   bookings = read_bookings()
   classes = read_classes()

   members = read_members()
   found = False
   for m in members:
      if m[0] == member_id:
         found = True

   if not found:
      print("\nNo such member.\n")
      return

   history = []
   for b in bookings:
      if b[1] == member_id:
         history.append(b)

   if not history:
      print(f"\nNo booking history for {member_id}.\n")
      return

   print(f"\n===== HISTORY FOR {member_id} =====")
   for b in history:
      booking_id, mem_id, class_code, date, status = b

      class_name = class_code
      for c in classes:
         if c[0] == class_code:
            class_name = c[1]

      print(f"{date}  |  {class_name:<15}  |  Status: {status}")
   print()


def booking_menu():
   while True:
      print("===== BOOKING OFFICER MENU =====")
      print("1. Register New Member")
      print("2. Book a Class")
      print("3. Cancel a Booking")
      print("4. Reschedule a Booking")
      print("5. View Current Bookings")
      print("6. View Member Attendance History")
      print("7. Main Menu")

      option = input("Enter option: ")

      if option == "1":
         register_member()
      elif option == "2":
         book_class()
      elif option == "3":
         cancel_booking()
      elif option == "4":
         reschedule_booking()
      elif option == "5":
         view_bookings()
      elif option == "6":
         view_attendance_history()
      elif option == "7":
         break
      else:
         print("\nInvalid option, please try again.\n")

def cancel_booking():
   bookings = read_bookings()
   classes = read_classes()

   booking_id = input("Enter the Booking ID to cancel: ")

   target_booking = None
   for b in bookings:
      if b[0] == booking_id:
         target_booking = b

   if target_booking is None:
      print("\nBooking ID not found.\n")
      return

   if target_booking[4] == "CANCELLED":
      print("\nThat booking is already cancelled.\n")
      return

   class_code = target_booking[2]
   target_booking[4] = "CANCELLED"
   write_bookings(bookings)

   target_class = None
   for c in classes:
      if c[0] == class_code:
         target_class = c

   if target_class is not None:
      booked_count = int(target_class[5])
      if booked_count > 0:
         target_class[5] = str(booked_count - 1)
      write_classes(classes)

   print(f"\nBooking {booking_id} cancelled.\n")



if __name__ == "__main__":
   booking_menu()      



   
   


            



      
         
   

  

 





      
   



      

