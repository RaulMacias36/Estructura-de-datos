class Order:
    """Representa un pedido de un cliente."""
    def __init__(self, qtty, customer):
        self.qtty = qtty
        self.customer = customer

    def print_info(self):
        print(f"     Customer: {self.customer}")
        print(f"     Quantity: {self.qtty}")
        print(f"     ------------")

    def get_qtty(self):
        return self.qtty

    def get_customer(self):
        return self.customer


class Node:
    """Nodo para la lista enlazada."""
    def __init__(self, info):
        self.info = info
        self.next = None


class Queue:
    """Implementación de una cola FIFO usando una lista enlazada."""
    def __init__(self):
        self.top = None   
        self.tail = None  
        self._size = 0

    def size(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def front(self):
        """Devuelve el primer elemento sin borrarlo."""
        if self.is_empty():
            return None
        return self.top.info

    def enqueue(self, info):
        """Añade un nuevo elemento al final (tail)."""
        new_node = Node(info)
        if self.is_empty():
            self.top = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node  
            self.tail = new_node       
        self._size += 1

    def dequeue(self):
        """Extrae y devuelve el primer elemento (top)."""
        if self.is_empty():
            return None
        
        info = self.top.info
        self.top = self.top.next  
        self._size -= 1
        
        if self.is_empty():
            self.tail = None
            
        return info

    def get_nth(self, pos):
        """Obtiene el n-ésimo elemento (empezando en 1) sin borrarlo."""
        if pos < 1 or pos > self._size:
            return None
        
        current = self.top
        for _ in range(1, pos):
            current = current.next
        return current.info

    def print_info(self):
        """Muestra el estado actual de la cola."""
        print("********* QUEUE DUMP *********")
        print(f"   Size: {self._size}")
        
        current = self.top
        count = 1
        while current:
            print(f"   ** Element {count}")
            if isinstance(current.info, Order):
                current.info.print_info()
            else:
                print(f"     Info: {current.info}")
            
            current = current.next
            count += 1
        print("******************************\n")


if __name__ == "__main__":
    my_queue = Queue()

    print("--- Añadiendo pedidos ---")
    my_queue.enqueue(Order(20, "cust1"))
    my_queue.enqueue(Order(30, "cust2"))
    my_queue.enqueue(Order(40, "cust3"))
    my_queue.enqueue(Order(50, "cust4"))
    my_queue.print_info()

    print("--- Obteniendo el 3er elemento ---")
    third = my_queue.get_nth(3)
    if third:
        print(f"El cliente del 3er pedido es: {third.get_customer()}\n")

    print(f"Frente de la cola: {my_queue.front().get_customer()}")
    
    print("\n--- Realizando dequeue (extrayendo el primero) ---")
    processed = my_queue.dequeue()
    print(f"Pedido procesado de: {processed.get_customer()}")
    

    my_queue.print_info()