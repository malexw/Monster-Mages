import json
import random

def make_deck(deck_json):
  deck = Deck()
  
  for card in deck_json["cards"]:
    name = card["name"]
    action = card["type"]
    qty = card["qty"]
    text = card["text"]
    
    for i in xrange(qty):
      deck.add_card(Card(name, action, text))
      
  return deck
    
class Deck:
  def __init__(self):
    self.cards = []
  
  def add_card(self, card):
    self.cards.append(card)
    
  def shuffle(self):
    self.cards = sorted(self.cards, key=lambda card: card.id)
  
  def deal(self, player, count):
    if count == 0:
      return

    for i in xrange(count):
      player.give(self.cards.pop(0))
      
  def peek(self, count=10):
    for i in xrange(count):
      self.cards[i].display()

class Player:
  num = 1
  
  def __init__(self, char):
    self.hand = []
    self.id = Player.num
    Player.num += 1
    self.char = char
    self.energy = self.char.energy
    self.health = self.char.health

  def s(self):
    print "Player %s (%s) HP:%s/%s E:%s/%s" % (self.id, self.char.name, self.health, self.char.health, self.energy, self.char.energy)
    print self.char.ability
    i = 1
    for card in self.hand:
      card.display(i)
      i += 1
    print
  
  def turn(self):
    self.energy = self.char.energy
    cards_needed = 5 - len(self.hand)
    # Draw up to 5 at the end of the turn
    if cards_needed > 0:
      deck.deal(self, cards_needed)
  
  def give(self, card):
    self.hand.append(card)
  
  def d(self, index):
    if index == 0:
      return
    self.hand.pop(index-1)
  
  def h(self, hp):
    self.health += hp
    
  def e(self, e):
    self.energy += e
  
  def p(self, card, cost=0, add_energy=0, add_cards=0):
    if self.energy < cost:
      print "You don't have the energy"
      return
    
    play_stack.append(("P%s" % self.id, self.hand[card-1].name, self.hand[card-1].text))
    self.d(card)
    deck.deal(self, add_cards)
    self.e(add_energy - cost)

class Card:
  def __init__(self, name, action, text):
    self.id = random.randint(0, 65536)
    self.name = name
    self.action = action
    self.text = text
  
  def display(self, pre=0):
    if pre != 0:
      print "(%s)\t%s:\t%s\t%s" % (pre, self.name, self.action, self.text)
    else:
      print "(%s)\t%s:\t%s\t%s" % (self.id, self.name, self.action, self.text)

class Character:
  def __init__(self, name, ability, health, energy):
    self.id = random.randint(0, 65536)
    self.name = name
    self.ability = ability
    self.health = health
    self.energy = energy

def stack():
  for play in play_stack:
    print "%s (%s): %s" % (play[0], play[1], play[2])

def turn():
  p1.turn()
  p2.turn()
  global play_stack
  play_stack = []

def s():
  print "Deck: %s cards" % len(deck.cards)
  p1.s()
  p2.s()

#if __name__ == "__main__":
#random.seed(31337)
deck_file = open("deck.json")
deck_json = json.load(deck_file)

# Make the players -----------------------
char_list = []
for i in xrange(len(deck_json["characters"])):
  char = deck_json["characters"][i]
  char_list.append(Character(char["name"], char["ability"], char["health"], char["energy"]))
char_list = sorted(char_list, key=lambda char: char.id)

players = []
for p in xrange(deck_json["game"]["players"]):
  players.append(Player(char_list.pop(0)))

# assign to globals for handy reference
p1 = players[0]
p2 = players[1]

# Build the deck -------------------------
play_stack = []
deck = make_deck(deck_json)
#print "Loaded %s cards" % len(deck.cards)

deck.shuffle()

# initial deal
deck.deal(p1, 5)
deck.deal(p2, 5)
s()
