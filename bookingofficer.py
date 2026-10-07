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
         admin_menu()
      elif choice == "2":
         booking_menu()
      elif choice == "3":
         pass   # whoever owns Customer Management's menu function goes here
      elif choice == "4":
         pass   # whoever owns Accountant's menu function goes here
      elif choice == "5":
         print("Goodbye!")
         break
      else:
         print("\nInvalid option, please try again.\n")


if __name__ == "__main__":
   main_menu()

if __name__ == "__main__":
   booking_menu()
