# Student Name: Keegan Melton
# Student ID: 010237977

import csv
import datetime

# Chaining Hash Table referenced from Zybooks figure 7.8.2
# HashTable class using chaining.
# Big O notation: O(N)
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=40):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def insert(self, key, item):
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv = item
                return True

        keyValue = [key, item]
        bucket_list.append(keyValue)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        if key in bucket_list:
            bucket_list.remove(key)

# creates a Package class
# Big O notation: O(1)
class Package:
    def __init__(self, id, address, city, state, zip, deadLine, weight, notes, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryTime = None # Updates when the package is delivered
        self.deadLine = deadLine
        self.weight = weight
        self.notes = notes
        self.status = status # at hub, in route, delivered

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (self.id, self.address, self.city, self.state, self.zip,
                                                  self.deadLine, self.deliveryTime, self.weight, self.notes, self.status)
    # outputs the status of each package compared to the timestamp input by the user
    def print_status_time(self, checkTimeStatus, truck_starting_time):
        delivery_status = "at Hub"
        if checkTimeStatus > self.deliveryTime:
            delivery_status = "Delivered"
        elif checkTimeStatus > truck_starting_time:
            delivery_status = "en Route"
        return "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (self.id, self.address, self.city, self.state, self.zip,
                                                  self.deadLine, self.deliveryTime, self.weight, self.notes, delivery_status)

# creates a DeliveryTruck class
# Big O notation: O(1)
class DeliveryTruck:
    def __init__(self, truck_id, package_list, starting_time, mileage):
        self.truck_id = truck_id
        self.package_list = package_list
        self.original_package_list = package_list.copy() # keeps a list of packages that were on the truck for the report
        self.starting_time = starting_time
        self.mileage = mileage

    # converts to string
    def __str__(self):
        return "%s,%s,%s,%s" % (self.truck_id, self.package_list, self.starting_time, self.mileage)

# loads the package information from CSV
# inputs contents in to the constructors of the package class
# sets the status to "At Hub" by default
# Big O notation: O(N)
def loadPackageData(fileName):
    with open(fileName) as packageFile:
        packageData = csv.reader(packageFile)

        for package in packageData:
            pId = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pdeadLine = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = "At Hub"

            # package object
            package = Package(pId, pAddress, pCity, pState, pZip, pdeadLine, pWeight, pNotes, pStatus)

            # inserts the information in to hash table
            packageHash.insert(pId, package)

# calculates the distance between two addresses
# using information that originated from the Distance Table csv file
# returns distance
# Big O notation: O(1)
def distanceTraveled(fromLocation, toLocation):
    x = distanceData[0].index(fromLocation)
    y = distanceData[0].index(toLocation)
    distance = distanceData[x][y]
    return float(distance)

# Gets the shortest distance between the truck's location and remaining deliveries
# (nearest neighbor algorithm)
# returns the index number of the smallest element in "delivery_distance"
# returns the shortest distance
# Big O notation: O(N)
def get_shortest_distance(truck, fromLocation):
    delivery_distance = []
    for package in range(len(truck.package_list)):
        if package < (len(truck.package_list)):
            distance = distanceTraveled(fromLocation, packageHash.search(truck.package_list[package]).address)
            delivery_distance.append(distance)
        else:
           break
    truck.mileage = truck.mileage + min(delivery_distance)
    return delivery_distance.index(min(delivery_distance)), min(delivery_distance)

# the truck leaves the hub and all packages in the truck are updated to "Out For Delivery"
# "fromLocation" updated to the trucks current location after each delivery
# updates timestamps for delivery times of each package
# removes packages as they are delivered
# updates status to "Delivered" upon delivery
# returns current time
# Big O notation: O(N^2)
def delivering_packages(truck, fromLocation):
    current_time = truck.starting_time
    for package in range(len(truck.package_list)):
        packageHash.search(truck.package_list[package]).status = "Out For Delivery"
    while len(truck.package_list) > 0:
        packageDelivered, delivery_distance = get_shortest_distance(truck, fromLocation)
        current_time = current_time + datetime.timedelta(hours=delivery_distance / 18)
        fromLocation = packageHash.search(truck.package_list[packageDelivered]).address
        packageHash.search(truck.package_list[packageDelivered]).status = "Delivered"
        packageHash.search(truck.package_list[packageDelivered]).deliveryTime = current_time
        del truck.package_list[packageDelivered]

    # Brings the truck back after the last package has been delivered
    truck.mileage = truck.mileage + distanceTraveled(fromLocation, "4001 South 700 E")
    return (current_time)

# Checks to see what package was with which truck for the report
# Big O notation: O(1)
def get_truck_start_time_for_package(packageID):
    if packageID in truck_1.original_package_list:
        return truck_1.starting_time
    elif packageID in truck_2.original_package_list:
        return truck_2.starting_time
    elif packageID in truck_3.original_package_list:
        return truck_3.starting_time

# Loops the interface until the user exits
def interfaceMenu(usersChoice):
    while usersChoice not in ['1','2','3','4']:
        if usersChoice == 1:
            print("Please enter the package ID")
            checkPackageStatus = int(input("Package ID: "))
            print(packageHash.search(checkPackageStatus))
            print("\nPlease select an option: \n"
                  "1.) Check the status of an individual package \n"
                  "2.) Check the status of all packages at a specific time\n"
                  "3.) View truck mileage\n"
                  "4.) Exit the program")
            usersChoice = int(input("I'd like to select option: "))

        elif usersChoice == 2:
            print("Please enter a time to check the status of all the packages")
            userTimeCheck = input("time: (HH:MM)")
            timecomponents = userTimeCheck.split(":")
            checkTimeStamp = datetime.timedelta(hours=int(timecomponents[0]), minutes=int(timecomponents[1]))
            for packageID in range(1, 41):
                package = packageHash.search(packageID)
                truck_start_time = get_truck_start_time_for_package(packageID)
                print(package.print_status_time(checkTimeStamp, truck_start_time))

            print("\nPlease select an option: \n"
                  "1.) Check the status of an individual package \n"
                  "2.) Check the status of all packages at a specific time\n"
                  "3.) View truck mileage\n"
                  "4.) Exit the program")
            usersChoice = int(input("I'd like to select option: "))

        elif usersChoice == 3:
            print("\nTruck 1 has traveled " + str(truck_1.mileage))
            print("Truck 2 has traveled " + str(truck_2.mileage))
            print("Truck 3 has traveled " + str(truck_3.mileage))
            print("Total Mileage: " + str(totalMileage))

            print("\nPlease select an option: \n"
                  "1.) Check the status of an individual package \n"
                  "2.) Check the status of all packages at a specific time\n"
                  "3.) View truck mileage\n"
                  "4.) Exit the program")
            usersChoice = int(input("I'd like to select option: "))

        elif usersChoice == 4:
            print("Goodbye!")
            return
        else:
            print("\nPlease select an option: \n"
                  "1.) Check the status of an individual package \n"
                  "2.) Check the status of all packages at a specific time\n"
                  "3.) View truck mileage\n"
                  "4.) Exit the program")
            usersChoice = int(input("I'd like to select option: "))

# assigns packageHash to ChainingHashTable
packageHash = ChainingHashTable()

# loads data from 'WGUPS Package File.csv'
loadPackageData('WGUPS Package File.csv')

# loads data from 'WGUPS Distance Table.csv'
with open('WGUPS Distance Table.csv', 'r') as distanceTable:
   distanceData = list(csv.reader(distanceTable))

# manually loads Trucks using the DeliveryTruck Class
# Truck 1 leaves at the start of the day
truck_1 = DeliveryTruck(1, [1, 13, 14, 15, 16, 19, 20, 21, 29, 30, 31, 34, 37, 40], datetime.timedelta(hours=8, minutes=0), 0.0)
# Truck 2 leaves after the late packages arrive
truck_2 = DeliveryTruck(2, [3, 6, 10, 11, 18, 23, 25, 26, 28, 32, 36, 38], datetime.timedelta(hours=9, minutes=5), 0.0)
# Truck 3's starting time will be updated to when truck 1 and 2 return
truck_3 = DeliveryTruck(3, [2, 4, 5, 7, 8, 9, 12, 17, 22, 24, 27, 33, 35, 39], datetime.timedelta(hours=8, minutes=0), 0.0)

# starts delivering packages from the hub
fromLocation = '4001 South 700 E'

# Sends truck 1 & 2 out for delivery
# Sets the departure time of truck 3 to later in the day to make sure a driver is available
truck_1_returnTime = delivering_packages(truck_1, fromLocation)
truck_2_returnTime = delivering_packages(truck_2, fromLocation)
truck_3.starting_time = max(truck_2_returnTime, truck_1_returnTime)

# updates address information for package 9 before truck 3 leaves
pkg9 = packageHash.search(9)
pkg9.address = "410 S State St"
pkg9.zip = "84111"

# Sends truck 3 out for delivery
delivering_packages(truck_3, fromLocation)

# adds the mileage of all 3 trucks
totalMileage = truck_1.mileage + truck_2.mileage + truck_3.mileage

# Begins user interface
# gives user the option to check on a single package, or
# all packages at a specific time
print("Welcome!\n"
      "Please select an option: \n"
      "1.) Check the status of an individual package \n"
      "2.) Check the status of all packages at a specific time\n"
      "3.) View truck mileage\n"
      "4.) Exit the program")
usersChoice = int(input("I'd like to select option: "))
# calls interfaceMenu
interfaceMenu(usersChoice)

