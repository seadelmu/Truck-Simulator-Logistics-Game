class Player:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Player, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.level = 1
        self.exp = 0
        self.expLimit = 100
        self.balance = 10000
        self._initialized = True

        print("Player initialized")

    def __str__(self):
        return (
            f"Player(Level: {self.level}, "
            f"EXP: {self.exp}/{self.expLimit}, "
            f"Balance: ${self.balance})")


    def addExp(self, amount):
        self.exp += amount
        if self.level <= 100 and self.exp >= self.expLimit:
            self.exp = self.exp - self.expLimit
            self.expLimit += 20
            self.level += 1
            self.balance += 1000

            print("Leveled Up!")
    
    def addBalance(self, amount):
        self.balance += amount
    
    def makePurchase(self, amount):
        self.balance-=amount

    def getLevel(self):
        return self.level
    
    def zeroBalance(self):
        if self.balance < 0:
            print(self.balance)
            return True
        else:
            return False
    
    
    def __del__(self):
        print("Player instance deleted")
        Player._instance = None
    



    
class Product:
    def __init__(self, name: str, price: float, prodCost: float, quantity=0, description=None):
        self.name = name
        self.productionCost = prodCost
        self.price = price
        self.quantity = quantity
        self.description = description

    def __str__(self):
        return f"{self.name} - ${self.price:.2f} ({self.quantity} in stock)"
    
    def makeInvoice(self, amount: int):
        return self.price * amount

    def purchase(self, amount: int, balance: float):
        totalPrice = self.price * amount
        if totalPrice >= balance:
            print("Total spent exceeds balance")
            return -1
        
        if amount > 0:
            self.quantity += amount
            print(f"{self.name} restocked by {amount}. New quantity: {self.quantity}")
            return 1
        else:
            print("Restock amount must be positive.")
            return -1

    def sell(self, amount):
        if amount <= 0:
            print("Purchase amount must be positive.")
            return -1
        elif amount > self.quantity:
            print(f"Not enough {self.name} in stock.")
            return -1
        else:
            self.quantity -= amount
            print(f"Purchased {amount} of {self.name}. Remaining: {self.quantity}")
            return 1


class Truck:
    def __init__(self, ID):
        self.truckID = ID
        self.product = None
        self.quantity = 0
        self.status = 0
        self.destination = None
        self.capacity = 100
        self.confirmation = False
        self.travelTime = 0
        self.daysRemaining = 0

    def __str__(self):
        status_labels = {
            0: "standby",
            1: "in delivery",
            2: "unloading",
            3: "returning",
            4: "In incident"
        }

        return (
            f"ID: {self.truckID}\n"
            f"    Product: {self.product}\n"
            f"    Quantity: {self.quantity}\n"
            f"    Destination: {self.destination}\n"
            f"    Capacity: {self.capacity}\n"
            f"    Confirmation: {self.confirmation}\n"
            f"    Status: {status_labels.get(self.status, 'Unknown')}\n"
            f"    Travel Time: {self.travelTime}\n"
            f"    Days Remaining: {self.daysRemaining}\n"
        )


    def loadTruck(self, product: Product, quantity: int):
        if (product != None):
            self.product = product
        else:
            print("Product can't be none")
            return -1

        if quantity <= 0:
            print("Quantity must be positive")
            return -1
        elif quantity > self.capacity:
            print("Can't exceed truck's load limit")
            return -1
        else:
            self.quantity = quantity

        return 1
    
    def nextDay(self):
        if self.status != 0:
            if self.status == 1 or self.status == 3:
                self.daysRemaining -= 1

            if self.daysRemaining == 0:
                match self.status:
                    case 1:
                        self.unloadTruck()
                        return 1
                    case 2:
                        self.returnTruck()
                        return 2
                    case 3:
                        self.standbyTruck()
                        return 3
            return 0

    def startDelivery(self, destination, travelTime):
        self.status = 1
        self.destination = destination
        self.travelTime = travelTime
        self.daysRemaining = travelTime

    def unloadTruck(self):
        self.status = 2
        self.product = None
        self.quantity = 0
        self.confirmation = True

    def returnTruck(self):
        self.status = 3
        self.destination = "home"
        self.daysRemaining = self.travelTime

    def standbyTruck(self):
        self.status = 0
        self.destination = None
        self.confirmation = False
        self.travelTime = 0


class Order:
    def __init__(self, name: str, product: Product, amount: int, destination: str, exp: int):
        self.name = name
        self.purchaseProduct = product
        self.purchasedAmount = amount
        self.orderDestination = destination
        self.orderTime = 0
        self.orderPrice = product.makeInvoice(amount)
        self.expReward = exp
        self.accepted = False
        self.assignedTruck = None
        self.complete = False

    def __str__(self):
        return (f"Order: {self.name}, "
                f"Product: {self.purchaseProduct.name}, "
                f"Amount: {self.purchasedAmount}, "
                f"Destination: {self.orderDestination}")

    def dropPrice(self):
        self.orderPrice -= self.purchaseProduct.price


class Fleet:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Fleet, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.trucks = [None] * 10
        self.truckCount = 0
        self._initialized = True

    def addTruck(self, ID):
        if (self.truckCount != 10):
            print(f"{ID} added")
            self.trucks[self.truckCount] = Truck(ID)
            self.truckCount+=1
        else:
            print("Maximum amount of trucks unlocked")

    def getTruck(self, i):
        if i < 10:
            return self.trucks[i]
        
        return None
    
    def printTrucks(self):
        if self.truckCount == 0:
            print("\nNo Trucks Exist Yet\n")
            return
        print("Trucks: ")
        for truck in self.trucks:
            if truck != None:
                print(truck)
        print()
    
    def __del__(self):
        print("Fleet instance destroyed.")
        Fleet._instance = None

