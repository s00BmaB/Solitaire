import arcade
from random import shuffle, randint

#base card sprite sizes
BASE_WIDTH, BASE_HEIGHT = 150, 200

#pile spacing const
PILE_SPACING = 1.1


class Card(arcade.Sprite):
    def __init__(self, suit, rank, scale=1.0, back=2):
        self.suit = suit  #0-3 S H C D
        self.rank = rank  #1-13 A 2-10 J Q K
        self.faceUp = False
        self.backArt = f"graphics/backs/back{back}.png"
        self.faceArt = f"graphics/cards/card{suit}{rank}.png"
        super().__init__(self.backArt, scale=scale, hit_box_algorithm="None")
        self.verticalOffset = self.height * 0.2

    def replace_back_art(self, newArt):
        self.backArt = newArt
        self.texture = arcade.load_texture(self.backArt)

    def flip(self):
        if self.faceUp:
            self.texture = arcade.load_texture(self.backArt)
            self.faceUp = not self.faceUp
        else:
            self.texture = arcade.load_texture(self.faceArt)
            self.faceUp = not self.faceUp

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def get_color(self):
        if self.suit == 0 or self.suit == 2:
            return 'B'
        else:
            return 'R'


class CardPile:
    def __init__(self, centerX=0, centerY=0):
        self.posX = centerX
        self.posY = centerY
        self.nextY = centerY
        self.pile = []

    def pile_height(self):
        return len(self.pile)

    def is_empty(self):
        return self.pile_height() == 0

    def add_card(self, card):
        card.set_position(self.posX, self.nextY)
        self.nextY -= card.verticalOffset
        self.pile.append(card)

    def top_card(self):
        return self.pile[-1]

    def nth_card(self, n):
        if self.pile_height() >= abs(n):
            return self.pile[n]

    def draw(self):
        if not self.is_empty():
            self.nextY += self.top_card().verticalOffset
            return self.pile.pop()


class SuitPile(CardPile):
    def __init__(self, centerX, centerY):
        super().__init__(centerX, centerY)
        self.rankToGet = 1
        self.suit = 0

    def add_card(self, card):
        card.set_position(self.posX, self.nextY)
        self.rankToGet += 1
        self.pile.append(card)

    def set_suit(self, s):
        self.suit = s

    def check_suit_completion(self):
        return self.rankToGet == 14


class ClassicDeck(CardPile):

    def add_card(self, card):
        card.set_position(self.posX, self.nextY)
        self.pile.append(card)

    def draw(self):
        if not self.is_empty():
            return self.pile.pop()

    def shuffle_pile(self):
        shuffle(self.pile)

    def __init__(self, centerX, centerY, scale, back=2):
        super().__init__(centerX, centerY)
        for i in range(4):
            for j in range(1, 14):
                self.add_card(Card(i, j, scale, back))


class DrawnPile(CardPile):
    def add_card(self, card):
        card.set_position(self.posX, self.nextY)
        self.pile.append(card)

    def draw(self):
        if not self.is_empty():
            return self.pile.pop()

    def __init__(self, centerX, centerY):
        super().__init__(centerX, centerY)


class BaseBoard:
    def __init__(self, screenWidth, screenHeight, scale=1.0, colNum=4):
        self.pileSpotMarkerList = None
        self.cardList = None
        self.theDeck = None
        self.allPiles = None  # 0:deck, 1:drawm, 2-5:suits, 6-12:board
        self.scale = scale
        self.xSpacing = BASE_WIDTH * PILE_SPACING * scale
        self.firstX = (screenWidth - (colNum-1) * self.xSpacing) / 2
        self.firstY = screenHeight - BASE_HEIGHT * scale * 0.6

    def setup(self):
        #holds all the sprites to be drawn in order
        self.pileSpotMarkerList = arcade.SpriteList()
        self.cardList = arcade.SpriteList()
        self.allPiles = []

        for i in range(1, 5):
            theDeck = ClassicDeck(self.firstX, self.firstY, self.scale, i)
            marker = (arcade.SpriteSolidColor
                      (round(BASE_WIDTH * self.scale), round(BASE_HEIGHT * self.scale),
                       arcade.csscolor.DARK_OLIVE_GREEN))
            marker.position = self.firstX + self.xSpacing * (i - 1), self.firstY
            self.pileSpotMarkerList.append(marker)
            self.allPiles.append(theDeck)

            for card in theDeck.pile:
                self.cardList.append(card)
                self.pull_to_top(card)

    def pre_move_card_check(self, origin, cardIndex, key=None):
        # to be implemented in child classes
        pass

    def marker_check(self, markerIndex):
        # to be implemented in child classes
        pass

    def adjust_positions(self, difWidth, difHeight):
        self.firstX -= difWidth/2
        self.firstY -= difHeight
        for card in self.cardList:
            card.center_x -= difWidth/2
            card.center_y -= difHeight
        for marker in self.pileSpotMarkerList:
            marker.center_x -= difWidth/2
            marker.center_y -= difHeight
        for pile in self.allPiles:
            pile.posX -= difWidth/2
            pile.posY -= difHeight
            pile.nextY -= difHeight

    def pull_to_top(self, card):
        self.cardList.remove(card)
        self.cardList.append(card)

    def move_cards(self, origin, dest, quantity):
        if origin == dest or quantity == 0:
            return True
        originPile = self.allPiles[origin]
        destPile = self.allPiles[dest]

        if quantity == 1:
            card = originPile.draw()
            self.pull_to_top(card)
            destPile.add_card(card)
        else:
            tempPile = CardPile()
            for i in range(quantity):
                tempPile.add_card(originPile.draw())
            while not tempPile.is_empty():
                card = tempPile.draw()
                self.pull_to_top(card)
                destPile.add_card(card)
        if not originPile.is_empty() and not originPile.top_card().faceUp:
            originPile.top_card().flip()
        return True

    def move_on_board(self, origin, dest, quantity=1):
        # implement movement rules in child classes here
        return self.move_cards(origin, dest, quantity)

    def change_back(self, x=None):
        if x and 0 <= x <= 4:
            replacementBack = f"graphics/backs/back{x}.png"
        else:
            replacementBack = f"graphics/backs/back{randint(1, 4)}.png"
        for pile in self.allPiles:
            for card in pile.pile:
                card.replace_back_art(replacementBack)

    def get_pile_for_card(self, card):
        for index, pile in enumerate(self.allPiles):
            if card in pile.pile:
                return index

    def game_win_check(self):
        # implement win condition here in child classes
        pass


class ClassicBoard(BaseBoard):
    def __init__(self, screenWidth, screenHeight, scale=1.0):
        super().__init__(screenWidth, screenHeight, scale, 7)
        self.drawnCards = None
        self.allSuits = None
        self.allBoardPiles = None

    def setup(self):
        self.pileSpotMarkerList = arcade.SpriteList()
        self.cardList = arcade.SpriteList()
        self.allPiles = []  # 0:deck, 1:drawm, 2-5:suits, 6-12:board

        self.theDeck = ClassicDeck(self.firstX, self.firstY, self.scale)
        marker1 = (arcade.SpriteSolidColor
                   (round(BASE_WIDTH * self.scale), round(BASE_HEIGHT * self.scale), arcade.csscolor.DARK_OLIVE_GREEN))
        marker1.position = self.firstX, self.firstY
        self.pileSpotMarkerList.append(marker1)
        self.allPiles.append(self.theDeck)

        self.drawnCards = DrawnPile(self.firstX + self.xSpacing, self.firstY)
        marker2 = (arcade.SpriteSolidColor
                   (round(BASE_WIDTH * self.scale), round(BASE_HEIGHT * self.scale), arcade.csscolor.DARK_OLIVE_GREEN))
        marker2.position = self.firstX + self.xSpacing, self.firstY
        self.pileSpotMarkerList.append(marker2)
        self.allPiles.append(self.drawnCards)

        self.allSuits = []
        for i in range(4):
            pile = SuitPile(self.firstX + self.xSpacing * (i + 3), self.firstY)
            self.allSuits.append(pile)
            self.allPiles.append(pile)
            marker = (arcade.SpriteSolidColor
                      (round(BASE_WIDTH * self.scale), round(BASE_HEIGHT * self.scale),
                       arcade.csscolor.DARK_OLIVE_GREEN))
            marker.position = self.firstX + self.xSpacing * (i + 3), self.firstY
            self.pileSpotMarkerList.append(marker)

        self.allBoardPiles = []
        for i in range(7):
            pile = CardPile(self.firstX + self.xSpacing * i, self.firstY - BASE_HEIGHT * 1.1 * self.scale)
            self.allBoardPiles.append(pile)
            self.allPiles.append(pile)
            marker = (arcade.SpriteSolidColor
                      (round(BASE_WIDTH * self.scale), round(BASE_HEIGHT * self.scale),
                       arcade.csscolor.DARK_OLIVE_GREEN))
            marker.position = self.firstX + self.xSpacing * i, self.firstY - BASE_HEIGHT * 1.1 * self.scale
            self.pileSpotMarkerList.append(marker)

        self.change_back()
        self.theDeck.shuffle_pile()

        for card in self.theDeck.pile:
            self.cardList.append(card)
            self.pull_to_top(card)

        for i in range(7):
            for j in range(i + 1):
                card = self.theDeck.draw()
                self.pull_to_top(card)
                self.allBoardPiles[(6 - j)].add_card(card)

        for pile in self.allBoardPiles:
            pile.top_card().flip()

    def pre_move_card_check(self, origin, cardIndex, key=None):
        originPile = self.allPiles[origin]
        if (key & arcade.key.MOD_CTRL
                and (originPile == self.drawnCards
                     or originPile in self.allBoardPiles)):
            self.claim_suit(origin)
            return True
        elif originPile == self.theDeck:
            self.draw_next()
            return True
        elif (not originPile.nth_card(cardIndex).faceUp
              or originPile in self.allSuits):
            return True
        else:
            return False

    def marker_check(self, markerIndex):
        if self.allPiles[markerIndex] == self.theDeck and self.theDeck.is_empty:
            self.refill()

    def draw_next(self):
        if self.theDeck.is_empty():
            self.refill()
        card = self.theDeck.draw()
        self.pull_to_top(card)
        card.flip()
        self.drawnCards.add_card(card)

    def refill(self):
        while not self.drawnCards.is_empty():
            card = self.drawnCards.draw()
            self.pull_to_top(card)
            card.flip()
            self.theDeck.add_card(card)

    def move_on_board(self, origin, dest, quantity=1):
        originPile = self.allPiles[origin]
        destPile = self.allPiles[dest]
        if (originPile in self.allSuits
                or originPile == self.theDeck
                or destPile == self.theDeck
                or destPile == self.drawnCards
                or (destPile in self.allSuits and quantity > 1)):

            return False
        elif (destPile in self.allBoardPiles
                and not originPile.is_empty()
                and ((destPile.is_empty() and originPile.nth_card(-quantity).get_rank() == 13)
                     or (not destPile.is_empty()
                         and originPile.nth_card(-quantity).get_rank() + 1 == destPile.top_card().get_rank()
                         and originPile.nth_card(-quantity).get_color() != destPile.top_card().get_color()))):

            return self.move_cards(origin, dest, quantity)
        elif destPile in self.allSuits:

            return self.claim_suit(origin, dest)
        else:
            return False

    def claim_suit(self, origin, dest=None):
        originPile = self.allPiles[origin]
        card = originPile.top_card()
        if dest:
            pile = self.allPiles[dest]
            if pile.is_empty() and card.get_rank() == 1:
                pile.set_suit(card.get_suit())
                self.pull_to_top(card)
                pile.add_card(originPile.draw())
                if not originPile.is_empty() and not originPile.top_card().faceUp:
                    originPile.top_card().flip()
                return True
            elif pile.rankToGet == card.get_rank() and pile.suit == card.get_suit():
                self.pull_to_top(card)
                pile.add_card(originPile.draw())
                if not originPile.is_empty() and not originPile.top_card().faceUp:
                    originPile.top_card().flip()
                return True
        else:
            for pile in self.allSuits:
                if pile.is_empty() and card.get_rank() == 1:
                    pile.set_suit(card.get_suit())
                    self.pull_to_top(card)
                    pile.add_card(originPile.draw())
                    if not originPile.is_empty() and not originPile.top_card().faceUp:
                        originPile.top_card().flip()
                    return True
                elif pile.rankToGet == card.get_rank() and pile.suit == card.get_suit():
                    self.pull_to_top(card)
                    pile.add_card(originPile.draw())
                    if not originPile.is_empty() and not originPile.top_card().faceUp:
                        originPile.top_card().flip()
                    return True
            return False

    def game_win_check(self):
        for pile in self.allSuits:
            if not pile.check_suit_completion():
                return False
        return True


class SpiderDeck(CardPile):

    def add_card(self, card):
        card.set_position(self.posX, self.nextY)
        self.pile.append(card)

    def draw(self):
        if not self.is_empty():
            return self.pile.pop()

    def __init__(self, centerX, centerY, scale):
        super().__init__(centerX, centerY)
        for i in range(1, 105):
            self.add_card(Card(0, (i % 13) + 1, scale))

    def shuffle_pile(self):
        shuffle(self.pile)


class SpiderDonePile(CardPile):
    def add_card(self, card):
        card.set_position(self.posX, self.nextY)
        self.pile.append(card)

    def __init__(self, centerX, centerY):
        super().__init__(centerX, centerY)


class SpiderBoard(BaseBoard):

    def __init__(self, screenWidth, screenHeight, scale=1.0):
        super().__init__(screenWidth, screenHeight, scale, 10)
        self.allBoardPiles = None
        self.allDonePiles = None

    def setup(self):
        self.pileSpotMarkerList = arcade.SpriteList()
        self.cardList = arcade.SpriteList()
        self.allPiles = []

        self.theDeck = SpiderDeck(self.firstX, self.firstY, self.scale)
        self.allPiles.append(self.theDeck)
        deckMarker = (arcade.SpriteSolidColor
                      (round(BASE_WIDTH * self.scale), round(BASE_HEIGHT * self.scale),
                       arcade.csscolor.DARK_OLIVE_GREEN))
        deckMarker.position = self.firstX, self.firstY
        self.pileSpotMarkerList.append(deckMarker)

        self.allBoardPiles = []
        secondY = self.firstY - BASE_HEIGHT * 1.1 * self.scale
        for i in range(10):
            pile = CardPile(self.firstX + self.xSpacing * i, secondY)
            self.allBoardPiles.append(pile)
            self.allPiles.append(pile)
            marker = (arcade.SpriteSolidColor
                      (round(BASE_WIDTH * self.scale), round(BASE_HEIGHT * self.scale),
                       arcade.csscolor.DARK_OLIVE_GREEN))
            marker.position = self.firstX + self.xSpacing * i, secondY
            self.pileSpotMarkerList.append(marker)

        self.allDonePiles = []
        for i in range(2, 10):
            pile = SpiderDonePile(self.firstX + self.xSpacing * i, self.firstY)
            self.allDonePiles.append(pile)
            self.allPiles.append(pile)
            marker = (arcade.SpriteSolidColor
                      (round(BASE_WIDTH * self.scale), round(BASE_HEIGHT * self.scale),
                       arcade.csscolor.DARK_OLIVE_GREEN))
            marker.position = self.firstX + self.xSpacing * i, self.firstY
            self.pileSpotMarkerList.append(marker)

        self.change_back()
        self.theDeck.shuffle_pile()

        for card in self.theDeck.pile:
            self.cardList.append(card)
            self.pull_to_top(card)

        for i in range(54):
            card = self.theDeck.draw()
            self.pull_to_top(card)
            self.allBoardPiles[i % 10].add_card(card)

        for pile in self.allBoardPiles:
            pile.top_card().flip()

    def game_win_check(self):
        for pile in self.allDonePiles:
            if pile.is_empty():
                return False

        return True

    def next_row(self):
        for pile in self.allBoardPiles:
            if pile.is_empty():
                return

        if self.theDeck.is_empty():
            return
        else:
            for pile in self.allBoardPiles:
                card = self.theDeck.draw()
                self.pull_to_top(card)
                card.flip()
                pile.add_card(card)

    def pre_move_card_check(self, origin, cardIndex, key=None):
        originPile = self.allPiles[origin]
        card = self.allPiles[origin].nth_card(cardIndex)
        if originPile == self.theDeck:
            self.next_row()
            return True
        elif (originPile in self.allDonePiles
              or not card.faceUp):
            return True
        else:
            #print(originPile.pile_height() - cardIndex)
            return not self.pile_continuity_check(origin, originPile.pile_height() - cardIndex)

    def marker_check(self, markerIndex):
        pass

    def pile_continuity_check(self, pileIndex, quantity):
        pile = self.allPiles[pileIndex]
        prevRank = pile.top_card().get_rank()

        if quantity > 1:
            for i in range(2, quantity + 1):
                if pile.nth_card(-i).get_rank() == prevRank + 1:
                    prevRank += 1
                else:
                    return False
            return True
        else:
            return True

    def move_on_board(self, origin, dest, quantity=1):
        originPile = self.allPiles[origin]
        destPile = self.allPiles[dest]
        if (originPile in self.allDonePiles
                or originPile == self.theDeck
                or destPile == self.theDeck
                or destPile in self.allDonePiles
                or not self.pile_continuity_check(origin, quantity)):

            return False
        elif (destPile.is_empty()
              or destPile.top_card().get_rank() == originPile.nth_card(-quantity).get_rank() + 1):
            if self.move_cards(origin, dest, quantity):
                self.done_pile_check(dest)
                return True
            else:
                return False
        else:
            return False

    def done_pile_check(self, pileIndex):
        pile = self.allPiles[pileIndex]
        if (pile.top_card().get_rank() != 1
                or pile.pile_height() < 13
                or not pile.nth_card(-13).faceUp):
            return
        elif self.pile_continuity_check(pileIndex, 13):
            for donePile in self.allDonePiles:
                if donePile.is_empty():
                    for i in range(13):
                        card = pile.draw()
                        self.pull_to_top(card)
                        donePile.add_card(card)
                    if not pile.is_empty() and not pile.top_card().faceUp:
                        pile.top_card().flip()
                    return
        else:
            return
