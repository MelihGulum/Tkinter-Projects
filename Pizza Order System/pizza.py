pizza_dict = {"Classic": 30, "Turk Pizza": 35, "Regular Pizza": 30,
              "Napoletana": 60, "Pizza Capricciosa": 60, "Pizza Quattro Formaggi":60,
              "Sardenara":60, "Pizza Margherita": 40,}

toppings_dict = {"Black Olives": 2, "Mushrooms":6, "Meat": 10,
              "Onion": 2, "Corn":2, "Mozzarella": 8,
              "Tomatoes": 3, "Parmesan": 7, "Basil": 2,
              "San Marzano Tomatoes": 4, "Tomato Sauce":3,
              "Gorgonzola":4, "Parmigiano Reggiano":4,
              "Goat Cheese":4,"Sardines": 10, "Red Onions":3,
              "Prosciutto Cotto (ham)": 6, "Parsley":3}

def cost_pizza(name):
  cost = 0.0
  cost = pizza_dict[name] if name in pizza_dict else "Check Pizza"
  return cost


class Pizza():
    orders = []
    cost = 0.0

    def __init__(self, **kwargs):
        self.name = None
        self.ingredients = None
        self.quantity = None

        for k, v, in kwargs.items():
            if k in self.__dict__:
                setattr(self, k, v)
            else:
                raise KeyError(k)

        Pizza.orders.append(self)

    def __str__(self):
        ings = ', '.join([str(i) for i in self.ingredients])
        return f'''The ingredients of {self.name}: {ings}'''

        # def __repr__(self):

    #  return f'{self.__class__.__name__}({self.name}, {self.quantity}, {self.ingredients!r})'

    def get_description(self):
        if self.name == None:
            return f'{self.__class__.__name__}'
        else:
            return f'{self.name}'

    def get_cost(self):
        if (self.__class__.__name__ == "Pizza"):
            if self.ingredients == None:
                cost = pizza_dict[self.name]
                return (cost * self.quantity)
            elif set(self.ingredients).issubset(toppings_dict):
                cost = pizza_dict[self.name]
                sauce_total = 0
                for key, value in toppings_dict.items():
                    if key in self.ingredients:
                        sauce_total += value
                return ((cost + sauce_total) * self.quantity)

        else:
            return (self.__class__.cost * self.quantity)

class Sardenara(Pizza):
  cost = cost_pizza("Sardenara")
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name="Sardenara"
    self.ingredients = ["Sardines", "Tomatoes Sauce", "Red Onions", "Parsley", "Mozzarella"]

class PizzaNapoletana(Pizza):
  cost = cost_pizza("Napoletana")
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name="Napoletana"
    self.ingredients = ["Mozzarella", "Tomatoes", "Parmesan", "Basil"]

class PizzaCapricciosa(Pizza):
  cost = cost_pizza("Pizza Capricciosa")
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name="Pizza Capricciosa"
    self.ingredients = ["San Marzano Tomatoes", "Mozzarella", "Prosciutto Cotto(ham)", "Black Olives","Mushroom"]

class PizzaQuattroFormaggi(Pizza):
  cost = cost_pizza("Pizza Quattro Formaggi")
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name="Pizza Quattro Formaggi"
    self.ingredients = ["Tomato Sauce", "Mozzarella", "Gorgonzola", "Parmigiano Reggiano","Goat Cheese"]

class PizzaMargherita(Pizza):
  cost = cost_pizza("Pizza Margherita")
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name="Pizza Margherita"
    self.ingredients = ["San Marzano Tomatoes", "Mozzarella", "Basil", "Parmigiano Reggiano"]