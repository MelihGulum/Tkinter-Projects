from pizza import *

sauce_dict = {"Ketchup": 1, "Mayonnaise": 2,
              "Mustard": 3, "Ranch": 3}

def cost_sauce(name):
  cost = 0.0
  cost = sauce_dict[name] if name in sauce_dict else "Check Sauce"
  return cost


class Decorator(Pizza):
    def __init__(self, pizza):
        self.component = pizza

    def get_cost(self):
        return (self.component.get_cost()) + (Pizza.get_cost(self))

    def get_description(self):
        return self.component.get_description() + \
               ' ' + Pizza.get_description(self)

class Ketchup(Decorator):
  cost = cost_sauce("Ketchup")
  def __init__(self, pizza, **kwargs):
        Decorator.__init__(self, pizza)
        Pizza.__init__(self,**kwargs)

class Mayonnaise(Decorator):
  cost = cost_sauce("Mayonnaise")
  def __init__(self, pizza, **kwargs):
        Decorator.__init__(self, pizza)
        Pizza.__init__(self,**kwargs)

class Mustard(Decorator):
  cost = cost_sauce("Mustard")
  def __init__(self, pizza, **kwargs):
        Decorator.__init__(self, pizza)
        Pizza.__init__(self,**kwargs)

class Ranch(Decorator):
  cost = cost_sauce("Ranch")
  def __init__(self, pizza, **kwargs):
        Decorator.__init__(self, pizza)
        Pizza.__init__(self,**kwargs)