import random
import project.objects as obj

class GameState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.player = obj.Player()
        self.day = 1
        self.orders = [None] * 10
        self.acceptedOrders = [None] * 10
        self.orderNum = 1
        self.inProgress = None
        self.trucks = obj.Fleet()

        self.products = ProductList()
        self.destinations = Destinations()
        self.productFactory = ProductFactory()
        self.messageLog = Log()

        self._initialized = True

    def nextDay(self):
        self.day += 1

        for truck in self.trucks.trucks:
            if truck is not None and truck.destination is not None:

                m = truck.nextDay()

                match m:
                    case 1:
                        message = f"{truck.truckID} Finished Delivery"
                        self.messageLog.add_message(message)
                    case 2:
                        message = f"{truck.truckID} Returning to base"
                        self.messageLog.add_message(message)
                    case 3:
                        message = f"{truck.truckID} On Standby"
                        self.messageLog.add_message(message)
        
        self.completeOrder()
                
        self.produceProduct()
        
        if (self.day % 2 == 0):
            self.addOrder()


    def acceptOrder(self, order_to_accept: obj.Order):
    
        for i, order in enumerate(self.orders):
            if order == order_to_accept:
                # Find a slot in acceptedOrders
                for j in range(len(self.acceptedOrders)):
                    if self.acceptedOrders[j] is None:
                        self.acceptedOrders[j] = order_to_accept
                        self.orders[i] = None  # Remove from original orders list
                        order_to_accept.accepted = True
                        print(f"Order accepted: {order_to_accept.name}")
                        return True
                print("No space in acceptedOrders list.")
                return False

        print("Order not found in current orders.")
        return False           

    def addOrder(self):
        level = self.player.getLevel()

        # Filter products based on level
        products = []
        for product in self.products.get_all_products():
            if product.name == "Low Quality Oil":
                products.append(product)
            elif product.name == "Mid Quality Oil" and level >= 10:
                products.append(product)
            elif product.name == "High Quality Oil" and level >= 20:
                products.append(product)

        destinations = list(self.destinations.get_all_destinations())

        # safety check
        if not products or not destinations:
            print("Cannot create an order: No products or destinations available.")
            return

        # Create the Order with random destination and product
        random_product = random.choice(products)
        random_destination = random.choice(destinations)
        
        new_order = obj.Order(
            name = f"Order {self.orderNum}", 
            product = random_product,
            amount = 100,
            destination = random_destination,
            exp = 100 * 10 
        )

        self.orderNum+=1

        # Add it to the first empty slot
        for i, order in enumerate(self.orders):
            if order is None:
                self.orders[i] = new_order
                print(f"New order added: {new_order.name} for {100} of {random_product.name} to {random_destination}")
                return

        print("Orders array is full. Cannot add a new order.")

    def completeOrder(self):
        for i, order in enumerate(self.acceptedOrders):
            if order is not None and order.assignedTruck is not None:
                truck = order.assignedTruck
                if truck.confirmation:
                    # Grant rewards
                    self.player.addExp(order.expReward)
                    self.player.addBalance(order.orderPrice)

                    message = f"{order} [Completed]"
                    self.messageLog.add_message(message)

                    # Clear order slot
                    print(f"Order completed: {order.name}")
                    self.acceptedOrders[i] = None


    def getOrders(self):
        return self.orders
    
    def getAcceptedOrders(self):
        return self.acceptedOrders
    
    def produceProduct(self):
        produce = self.productFactory.popProduct()
        if produce:
            produce[0].purchase(produce[1], self.player.balance)
            message = f"Product: {produce[0].name} | Quantity: {produce[1]} | Successfully produced"
            self.messageLog.add_message(message)
            
    def __del__(self):
        print("GameState instance destroyed.")
        GameState._instance = None


class ProductList:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProductList, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.low_quality_oil = obj.Product("Low Quality Oil", 10.00, 5.00, 100, "Standard engine oil.")
        self.mid_quality_oil = obj.Product("Mid Quality Oil", 25.00, 15.00, 100, "Improved synthetic blend.")
        self.high_quality_oil = obj.Product("High Quality Oil", 50.00, 30.00, 100, "Premium full-synthetic oil.")

        self._all_products = [
            self.low_quality_oil,
            self.mid_quality_oil,
            self.high_quality_oil,
        ]

    def get_all_products(self):
        return self._all_products
    
    def get_product_by_name(self, name: str):
        for product in self._all_products:
            if product.name == name:
                return product
        return None

class Destinations:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Destinations, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.travelTimes = {"Business 1": 5, 
                            "Business 2": 2,
                            "Business 3": 1}
        
    def get_all_destinations(self):
        return self.travelTimes.keys()


class ProductFactory:
    _instance = None

    class Queue:

        def __init__(self):
            self.productQueue = []
            self.quantityQueue = []
            self.count = 0
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProductFactory, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.queue = self.Queue()
        

    def appendProduct(self, product: obj.Product, quantity: int):
        if self.queue.count <= 15:
            self.queue.productQueue.append(product)
            self.queue.quantityQueue.append(quantity)
            self.queue.count+=1

            print(f"Product: {product.name} for Quantity: {quantity} queued for production")
            return 1
        else:
            return -1

    def popProduct(self):
        if self.queue.productQueue:
            prod = self.queue.productQueue.pop(0)
            quant = self.queue.quantityQueue.pop(0)
            self.queue.count-=1
            
            return prod, quant

    def getProductList(self):

        return self.queue

class Log:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.messageLog = []
        self.messageCount = 0

    def add_message(self, message: str):
        if self.messageCount != 15:
            self.messageLog.insert(0, message)
            self.messageCount+=1
        else:
            self.messageLog.pop(14)
            self.messageLog.insert(0, message)

    def get_message_log(self):
        return self.messageLog