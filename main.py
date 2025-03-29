import arcade  #shows no module but works probably broken during moving
import arcade.gui
import solitaireElements
import re

WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 1000
CARD_SCALE = 0.8


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.width, self.height = self.window.get_size()

        self.UIManager = arcade.gui.UIManager()

        self.UIManagerMain = arcade.gui.UIManager()
        self.vBox = arcade.gui.UIBoxLayout()

        self.UIManagerModes = arcade.gui.UIManager()
        self.vBoxModes = arcade.gui.UIBoxLayout()
        buttonWidth = 200

        self.UIManager = self.UIManagerMain

        solitaireLabel = arcade.gui.UILabel(text="SOLITAIRE",
                                            font_size=50,
                                            align="center",
                                            text_color=arcade.color.PINK)
        self.vBox.add(solitaireLabel.with_space_around(bottom=150))

        startButton = arcade.gui.UIFlatButton(text="NEW GAME", width=buttonWidth)
        self.vBox.add(startButton.with_space_around(bottom=20))

        @startButton.event("on_click")
        def on_click_start(event):
            if event:
                self.UIManager.disable()
                self.UIManager = self.UIManagerModes
                self.UIManager.enable()

        quitButton = arcade.gui.UIFlatButton(text="QUIT", width=buttonWidth)
        self.vBox.add(quitButton)

        @quitButton.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        self.UIManagerMain.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=70,
                child=self.vBox)
        )

        modeLabel = arcade.gui.UILabel(text="CHOSE THE MODE THAT YOU WANT TO PLAY",
                                       font_size=20,
                                       text_color=arcade.color.PINK,
                                       align="center")
        self.vBoxModes.add(modeLabel.with_space_around(bottom=100))

        classicButton = arcade.gui.UIFlatButton(text="CLASSIC", width=buttonWidth)
        self.vBoxModes.add(classicButton.with_space_around(bottom=20))

        @classicButton.event("on_click")
        def on_click_classic(event):
            if event:
                self.start("classic")

        spiderButton = arcade.gui.UIFlatButton(text="SPIDER", width=buttonWidth)
        self.vBoxModes.add(spiderButton.with_space_around(bottom=20))

        @spiderButton.event("on_click")
        def on_click_classic(event):
            if event:
                self.start("spider")

        backButton = arcade.gui.UIFlatButton(text="BACK", width=buttonWidth)
        self.vBoxModes.add(backButton)

        @backButton.event("on_click")
        def on_click_back(event):
            if event:
                self.UIManager.disable()
                self.UIManager = self.UIManagerMain
                self.UIManager.enable()

        self.UIManagerModes.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=70,
                child=self.vBoxModes)
        )

    def start(self, mode):
        gameView = BoardControlView(mode)
        gameView.setup()
        self.window.show_view(gameView)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.UIManager.enable()

    def on_hide_view(self):
        self.UIManager.disable()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            width, height = self.window.get_size()
            self.window.set_viewport(0, width, 0, height)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.width = width
        self.height = height

    def on_draw(self):
        self.clear()

        self.UIManager.draw()


class BoardControlView(arcade.View):
    def __init__(self, mode):
        self.mode = mode
        if mode == "classic":
            self.board = solitaireElements.ClassicBoard(WINDOW_WIDTH, WINDOW_HEIGHT, CARD_SCALE)
        elif mode == "spider":
            self.board = solitaireElements.SpiderBoard(WINDOW_WIDTH, WINDOW_HEIGHT, CARD_SCALE)
        else:
            self.board = solitaireElements.ClassicBoard(WINDOW_WIDTH, WINDOW_HEIGHT, CARD_SCALE)
        super().__init__()
        self.heldCards = None
        self.heldCardsOriginalPosition = None
        self.currentWidth = WINDOW_WIDTH
        self.currentHeight = WINDOW_HEIGHT
        self.scoreTime = None

        self.UIManager = arcade.gui.UIManager()

        cogScale = 0.8
        pauseButton = arcade.gui.UITextureButton(x=self.currentWidth - 100 * cogScale, y=20 * cogScale,
                                                 texture=arcade.load_texture("graphics/cog.png"),
                                                 scale=cogScale)

        @pauseButton.event("on_click")
        def on_pause_click(event):
            self.pause()

        self.UIManager.add(pauseButton)

        self.totalTime = 0.0
        self.timerText = arcade.Text(
            text="00:00:00",
            anchor_x="right",
            anchor_y="top",
            start_x=self.currentWidth-5,
            start_y=self.currentHeight-5,
            color=arcade.color.WHITE,
            font_size=12,
        )

    def on_show_view(self):
        self.UIManager.enable()

    def on_hide_view(self):
        self.UIManager.disable()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.board.adjust_positions(self.currentWidth - width, self.currentHeight - height)
        self.currentWidth = width
        self.currentHeight = height

    def setup(self):
        self.totalTime = 0.0
        self.heldCards = []
        self.heldCardsOriginalPosition = []

        self.board.setup()

    def on_draw(self):
        self.clear()
        self.board.pileSpotMarkerList.draw()
        self.board.cardList.draw()
        self.UIManager.draw()
        self.timerText.draw()

    def on_update(self, delta_time):
        self.totalTime += delta_time

        minutes = int(self.totalTime) // 60

        seconds = int(self.totalTime) % 60

        seconds100s = int((self.totalTime - seconds - minutes * 60) * 100)

        self.timerText.text = f"{minutes:02d}:{seconds:02d}:{seconds100s:02d}"

    def on_mouse_press(self, x, y, button, key_modifiers):
        cards = arcade.get_sprites_at_point((x, y), self.board.cardList)

        if len(cards) > 0:
            primeCard = cards[-1]
            pileIndex = self.board.get_pile_for_card(primeCard)
            cardIndex = self.board.allPiles[pileIndex].pile.index(primeCard)
            if self.board.pre_move_card_check(pileIndex, cardIndex, key_modifiers):
                return

            self.heldCards = [primeCard]
            self.heldCardsOriginalPosition = [primeCard.position]
            self.board.pull_to_top(primeCard)

            for i in range(cardIndex + 1, self.board.allPiles[pileIndex].pile_height()):
                card = self.board.allPiles[pileIndex].nth_card(i)
                self.board.pull_to_top(card)
                self.heldCards.append(card)
                self.heldCardsOriginalPosition.append(card.position)

        else:
            markers = arcade.get_sprites_at_point((x, y), self.board.pileSpotMarkerList)

            if len(markers) > 0:
                markerIndex = self.board.pileSpotMarkerList.index(markers[0])
                self.board.marker_check(markerIndex)

    def on_mouse_motion(self, x, y, dx, dy):
        for card in self.heldCards:
            card.center_x += dx
            card.center_y += dy

    def on_mouse_release(self, x, y, button, modifiers):
        if len(self.heldCards) == 0:
            if self.board.game_win_check():
                winView = GameWinView(self)
                self.scoreTime = self.timerText.text
                self.window.show_view(winView)
            return

        reset_position = True

        primeHeld = self.heldCards[0]
        marker, distance = arcade.get_closest_sprite(primeHeld, self.board.pileSpotMarkerList)
        pileIndex = self.board.pileSpotMarkerList.index(marker)

        if (arcade.check_for_collision(primeHeld, marker)
                or (not self.board.allPiles[pileIndex].is_empty()
                    and arcade.check_for_collision(primeHeld, self.board.allPiles[pileIndex].top_card()))):
            oldPileIndex = self.board.get_pile_for_card(primeHeld)
            reset_position = not self.board.move_on_board(oldPileIndex, pileIndex, len(self.heldCards))
        if reset_position:
            for index, card in enumerate(self.heldCards):
                card.position = self.heldCardsOriginalPosition[index]

        self.heldCards = []

        if self.board.game_win_check():
            winView = GameWinView(self)
            self.scoreTime = self.timerText.text
            self.window.show_view(winView)

    def pause(self):
        pauseView = PauseView(self)
        self.window.show_view(pauseView)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.R:  #Restart
            self.setup()

        if symbol == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            width, height = self.window.get_size()
            self.window.set_viewport(0, width, 0, height)

        if symbol == arcade.key.ESCAPE:
            self.pause()


class GameWinView(arcade.View):
    def __init__(self, gameView):
        super().__init__()
        self.gameView = gameView
        self.width, self.height = self.window.get_size()

        self.UIManagerButtons = arcade.gui.UIManager()
        self.UIManagerScore = arcade.gui.UIManager()
        self.UIManager = None

        self.vBox = arcade.gui.UIBoxLayout()
        self.vBoxScore = arcade.gui.UIBoxLayout()
        buttonWidth = 200

        infoLabel = arcade.gui.UILabel(text="Please insert the name under which your score will be saved",
                                       align="center",
                                       font_size=20,
                                       text_color=arcade.color.PINK)
        self.vBoxScore.add(infoLabel)

        ruleLabel = arcade.gui.UILabel(text="valid length: 1 to 30 characters | "
                                            "valid characters: letters, numbers, \'_\'",
                                       align="center",
                                       font_size=14,
                                       text_color=arcade.color.PINK)
        self.vBoxScore.add(ruleLabel.with_space_around(bottom=10))

        self.textField = arcade.gui.UIInputText(width=buttonWidth,
                                                height=30,
                                                font_size=16)
        #self.vBoxScore.add(self.textField)
        #something bugged here don't know why don't know how

        textBorder = arcade.gui.UIBorder(child=self.textField,
                                         border_color=arcade.color.PINK)
        self.vBoxScore.add(textBorder)

        okButton = arcade.gui.UIFlatButton(text="OK", width=buttonWidth/3,
                                           style={"bg_color": arcade.color.PINK,
                                                  "font_color": arcade.color.BLACK})
        self.vBoxScore.add(okButton)

        label = arcade.gui.UILabel(text="!please enter correct name!",
                                   align="center",
                                   font_size=14,
                                   text_color=arcade.color.RED)

        @okButton.event("on_click")
        def on_click_ok(event):
            name = self.textField.text
            if not self.name_check(name):
                if label not in self.vBoxScore:
                    self.vBoxScore.add(label)
                    self.vBoxScore.remove(okButton)
                    self.vBoxScore.add(okButton)
            else:
                self.save_score(name)
                self.UIManager.disable()
                self.UIManager = self.UIManagerButtons
                self.UIManager.enable()

        startButton = arcade.gui.UIFlatButton(text="NEW GAME", width=buttonWidth)
        self.vBox.add(startButton.with_space_around(bottom=20))

        @startButton.event("on_click")
        def on_click_start(event):
            self.new_game()

        menuButton = arcade.gui.UIFlatButton(text="MAIN MENU", width=buttonWidth)
        self.vBox.add(menuButton.with_space_around(bottom=20))

        @menuButton.event("on_click")
        def on_click_menu(event):
            menuView = MenuView()
            self.window.show_view(menuView)

        quitButton = arcade.gui.UIFlatButton(text="QUIT", width=buttonWidth)
        self.vBox.add(quitButton)

        @quitButton.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        self.UIManagerButtons.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.vBox)
        )

        self.UIManagerScore.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.vBoxScore)
        )

    def save_score(self, name):
        #print(f"{name} time: {self.gameView.scoreTime}")
        with open(f"scores/scores{self.gameView.mode.upper()}.txt", 'a') as f:
            f.write(f"{name} time: {self.gameView.scoreTime}\n")

    @staticmethod
    def name_check(name):
        pattern = r'^\w+$'
        return bool(re.match(pattern, name))

    def new_game(self):
        self.gameView.setup()
        self.window.show_view(self.gameView)

    def on_show_view(self):
        self.UIManager = self.UIManagerScore
        self.UIManager.enable()

    def on_hide_view(self):
        self.UIManager.disable()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.gameView.board.adjust_positions(self.width - width, self.height - height)
        self.width = width
        self.height = height

    def on_draw(self):
        self.clear()

        cards = self.gameView.board.cardList
        markers = self.gameView.board.pileSpotMarkerList

        for marker in markers:
            arcade.draw_lrtb_rectangle_filled(marker.left, marker.right, marker.top, marker.bottom,
                                              arcade.color.AMAZON + (20,))

        for card in cards:
            arcade.draw_lrtb_rectangle_filled(card.left, card.right, card.top, card.bottom,
                                              arcade.color.AMAZON + (20,))

        arcade.draw_text("CONGRATULATIONS!", self.width / 2, self.height * 0.75,
                         arcade.color.PINK, font_size=50, anchor_x="center")
        arcade.draw_text("YOU WON!", self.width / 2, self.height * 0.75 - 70,
                         arcade.color.PINK, font_size=50, anchor_x="center")

        self.UIManager.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            width, height = self.window.get_size()
            self.window.set_viewport(0, width, 0, height)


class PauseView(arcade.View):
    def __init__(self, gameView):
        super().__init__()
        self.gameView = gameView
        self.width, self.height = self.window.get_size()

        self.UIManager = arcade.gui.UIManager()

        self.vBox = arcade.gui.UIBoxLayout()
        buttonWidth = 200

        pauseLabel = arcade.gui.UILabel(text="PAUSE",
                                        align="center",
                                        font_size=50,
                                        bold=True,
                                        width=300,
                                        text_color=arcade.color.PINK)
        self.vBox.add(pauseLabel.with_space_around(bottom=20))

        resumeButton = arcade.gui.UIFlatButton(text="RESUME", width=buttonWidth)
        self.vBox.add(resumeButton.with_space_around(bottom=20))

        @resumeButton.event("on_click")
        def on_click_resume(event):
            self.resume()

        startButton = arcade.gui.UIFlatButton(text="NEW GAME", width=buttonWidth)
        self.vBox.add(startButton.with_space_around(bottom=20))

        @startButton.event("on_click")
        def on_click_start(event):
            self.new_game()

        menuButton = arcade.gui.UIFlatButton(text="MAIN MENU", width=buttonWidth)
        self.vBox.add(menuButton.with_space_around(bottom=20))

        @menuButton.event("on_click")
        def on_click_menu(event):
            menuView = MenuView()
            self.window.show_view(menuView)

        quitButton = arcade.gui.UIFlatButton(text="QUIT", width=buttonWidth)
        self.vBox.add(quitButton)

        @quitButton.event("on_click")
        def on_click_quit(event):
            arcade.exit()

        self.UIManager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.vBox)
        )

    def on_show_view(self):
        self.UIManager.enable()

    def on_hide_view(self):
        self.UIManager.disable()

    def on_draw(self):
        self.clear()

        cards = self.gameView.board.cardList
        markers = self.gameView.board.pileSpotMarkerList
        piles = self.gameView.board.allPiles

        markers.draw()
        cards.draw()

        for index, pile in enumerate(piles):
            if not pile.is_empty():
                arcade.draw_lrtb_rectangle_filled(pile.top_card().left, pile.top_card().right,
                                                  pile.pile[0].top, pile.top_card().bottom,
                                                  arcade.color.AMAZON + (220,))
            else:
                marker = markers[index]
                arcade.draw_lrtb_rectangle_filled(marker.left, marker.right,
                                                  marker.top, marker.bottom,
                                                  arcade.color.AMAZON + (200,))

        self.UIManager.draw()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.gameView.board.adjust_positions(self.width - width, self.height - height)
        self.width = width
        self.height = height

    def resume(self):
        self.window.show_view(self.gameView)

    def new_game(self):
        self.gameView.setup()
        self.window.show_view(self.gameView)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.resume()

        if symbol == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            width, height = self.window.get_size()
            self.window.set_viewport(0, width, 0, height)

        if symbol == arcade.key.R:
            self.new_game()


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "cards", resizable=False)
    menuView = MenuView()
    window.show_view(menuView)
    arcade.run()


if __name__ == "__main__":
    main()
