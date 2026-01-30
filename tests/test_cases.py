import project.database as database
import project.objects as obj
import project.game as g


# def test_db_connection():
#     db = database.PostgresHandler()
#     db.connect()

#     assert db.conn is not None, "Database connection failed: conn is None"
#     assert db.cursor is not None, "Database connection failed: cursor is None"

#     db.close()

# def test_db_singleton():
#     db1 = database.PostgresHandler()
#     db2 = database.PostgresHandler()

#     assert db1 is db2, "Database class not singleton"

def test_log_one():
    G = g.GameState()
    l = G.messageLog

    assert len(l.messageLog) is 0, "Message log not empty at initialization"
    assert l.messageCount is 0, "Message log counter not 0"

def test_log_singleton():
    l1 = g.Log()
    l2 = g.Log()

    assert l1 is l2, "Message Log class not singleton"


def test_player_one():
    p = obj.Player()

    p.addExp(120)

    assert p.level is 2, "Player did not level properly"
    assert p.exp is 20, "Player excess exp not returned properly"
    assert p.expLimit is 120, "Player exp limit not incremented properly"

def test_player_singleton():
    p1 = obj.Player()
    p2 = obj.Player()

    assert p1 is p2, "Player class not singleton"

def test_product_one():
    p = obj.Product(name="test", price=1, prodCost=1, quantity=0, description="A test product")

    x = p.purchase(10, 20)
    assert x is 1, "Purchase not successful"
    assert p.quantity is 10, "Purchase did not add appropriate amount to quantity"
    
    y = p.sell(5)
    assert y is 1, "Sell not sucessful"
    assert p.quantity is 5, "Sell did not decrease quantity"

    assert p.purchase(10, 5) is -1, "Purchase did not handle insufficient balance"
    assert p.purchase(-1, 10) is -1, "Purchase did not handle invalid amount"

    y = p.sell(-1)
    assert y is -1, "Sell did not handle invalid amount"
    y = p.sell(400)
    assert y is -1, "Sell did not handle amount exceeding quantity"

def test_truck_one():
    t = obj.Truck(11111)

    assert t.status is 0, "Truck not on standby by default"

    assert t.loadTruck(None, None) is -1, "loadTruck allowed no product"
    assert t.loadTruck("test", -1) is -1, "loadTruck allowed invalid product amount"
    assert t.loadTruck("test", 200) is -1, "loadTruck allowed amount exceeding capacity"
    assert t.loadTruck("test", 10) is 1, "loadTruck not successful"
    assert t.quantity is 10, "loadTruck did not load correct amount"
    assert t.product is "test", "loadTruck did not set product"

    t.startDelivery("test place", 0)

    assert t.status is 1, "startDelivery: Truck status not changed correctly, 'not in delivery'"
    assert t.destination is "test place", "startDelivery: Truck destination not set properly"

    t.unloadTruck()

    assert t.status is 2, "unloadTruck: Truck status not changed correctly, 'not unloading'"
    assert t.product is None, "unloadTruck: Truck product not set to none"
    assert t.quantity is 0, "unloadTruck: Truck quantity not set to 0"
    assert t.confirmation is True, "unloadTruck: Truck confirmation of product unload not true"

    t.returnTruck()

    assert t.status is 3, "returnTruck: Truck status not changed correctly, 'not returning'"
    assert t.destination is "home", "returnTruck: Truck destination not set properly"

    t.standbyTruck()

    assert t.status is 0, "standbyTruck: Truck not properly set to standby"
    assert t.destination is None, "standbyTruck: Truck destination not reset"
    assert t.confirmation is False, "standbyTruck: Truck delivery confirmation not reset"

def test_order_one():
    p = obj.Product("test", 1, 1)
    p.purchase(20, 40)

    assert p.quantity is 20, "Product purchase unsuccessful"

    o = obj.Order("test client", p, 10, "test destination", 100)
    assert o.orderPrice is 10, "Invoice price incorrect"

def test_gameState_singleton():
    game1 = g.GameState()
    game2 = g.GameState()

    assert game1 is game2, "GamesState Not Singleton"

def test_gameState_nextTurn():
    game = g.GameState()

    game.nextDay()

    assert game.day is 2, "Day did not incremement"

def test_fleet_one():
    f = obj.Fleet()

    assert f.trucks[0] is None, "Trucks array not set properly"
    assert f.truckCount is 0, "Truck count not initially 0"

    f.addTruck(1)

    t1 = f.getTruck(0)

    assert t1.truckID is 1, "Truck not initialized properly in array"
    assert f.truckCount is 1, "TruckCount not incrememnted properly"

def test_fleet_singleton():
    f1 = obj.Fleet()
    f2 = obj.Fleet()

    assert f1 is f2, "Fleet class not singleton"

def test_order_one():
    G = g.GameState()

    assert G.orders[0] is None, "Orders not none"

    G.addOrder()

    assert G.orders[0] is not None, "Orders not added properly"
    print (G.orders[0])

def test_product_factory_one():
    G = g.GameState()

    p = G.productFactory
    assert len(p.queue.productQueue) is 0, "productQueue not empty"
    assert len(p.queue.quantityQueue) is 0, "quantityQueue not empty"
    assert p.queue.count is 0, "Queue counter not 0"

def test_product_factory_singleton():
    pf1 = g.ProductFactory()
    pf2 = g.ProductFactory()

    assert pf1 is pf2, "Product Factory not singleton"

def test_product_factory_queue():
    G = g.GameState()
    prod = obj.Product(name="test", price=1, prodCost=1, quantity=0, description="A test product")


    p = G.productFactory
    p.appendProduct(prod, 100)

    assert len(p.queue.productQueue) is 1, "Product not appended to productQueue"
    assert len(p.queue.quantityQueue) is 1, "Product quantity not appended to quantityQueue"
    assert p.queue.count is 1, "Queue count not incremented properly"

def test_product_factory_pop():
    G = g.GameState()
    prod = obj.Product(name="test", price=1, prodCost=1, quantity=0, description="A test product")


    p = G.productFactory
    p.appendProduct(prod, 100)

    # in this instance of test, the product appended from previous test still exists due to singleton
    # Therefore, after appending another product, the count will be 2
    assert len(p.queue.productQueue) is 2, "Product not appended to productQueue"
    assert len(p.queue.quantityQueue) is 2, "Product quantity not appended to quantityQueue"
    assert p.queue.count is 2, "Queue count not incremented properly"

    pop = p.popProduct()

    assert pop[0].name is prod.name, "Product popped not returned"
    assert pop[1] is 100, "Product quantity popped not returned"
    assert p.queue.count is 1, "Queue count not decremented properly"

def test_product_list_singleton():
    pl1 = g.ProductList()
    pl2 = g.ProductList()

    assert pl1 is pl2, "ProductList class ot singleton"

def test_product_list_get_product():
    pl = g.ProductList()

    p1 = pl.get_product_by_name("Low Quality Oil")
    p2 = pl.get_product_by_name("Mid Quality Oil")
    p3 = pl.get_product_by_name("High Quality Oil")

    assert p1 is pl.low_quality_oil, "Did not return product correctly"
    assert p2 is pl.mid_quality_oil, "Did not return product correctly"
    assert p3 is pl.high_quality_oil, "Did not return product correctly"



