import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget


class BlackjackGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Blackjack Game")
        self.setGeometry(100, 100, 350, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Game state label
        self.game_state_label = QLabel("Welcome to Blackjack!", self)
        self.layout.addWidget(self.game_state_label)

        # Player and dealer hand labels
        self.player_hand_label = QLabel("Player Hand: ", self)
        self.layout.addWidget(self.player_hand_label)
        self.dealer_hand_label = QLabel("Dealer Hand: ", self)
        self.layout.addWidget(self.dealer_hand_label)

        # Buttons
        self.hit_button = QPushButton('Hit', self)
        self.hit_button.clicked.connect(self.hit)
        self.layout.addWidget(self.hit_button)

        self.stand_button = QPushButton('Stand', self)
        self.stand_button.clicked.connect(self.stand)
        self.layout.addWidget(self.stand_button)

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset)
        self.layout.addWidget(self.reset_button)

        self.exit_button = QPushButton('Quit', self)
        self.exit_button.clicked.connect(self.quit)
        self.layout.addWidget(self.exit_button)

        # Initialize game
        self.reset()

    def create_deck(self):
        values = list(range(1, 14)) * 4
        random.shuffle(values)
        return values

    def draw_card(self):
        if self.deck:
            return self.deck.pop()
        self.deck = self.create_deck()
        return self.deck.pop()

    def calculate_hand_value(self, hand):
        value = 0
        ace_count = 0
        for card in hand:
            if card == 1:
                ace_count += 1
                value += 11
            elif card > 10:
                value += 10
            else:
                value += card

        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1

        return value

    def hit(self):
        self.player_hand.append(self.draw_card())
        self.update_ui()
        if self.calculate_hand_value(self.player_hand) > 21:
            self.game_state_label.setText("Player busts! Dealer wins.")
            self.disable_buttons()

    def stand(self):
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.draw_card())

        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)

        if dealer_value > 21 or player_value > dealer_value:
            self.game_state_label.setText("Player wins!")
        elif dealer_value > player_value:
            self.game_state_label.setText("Dealer wins!")
        else:
            self.game_state_label.setText("Push!")

        self.disable_buttons()

    def reset(self):
        self.deck = self.create_deck()
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card()]
        self.enable_buttons()
        self.update_ui()

    def quit(self):
        sys.exit(app.exec_())
    def update_ui(self):
        self.player_hand_label.setText(f"Player Hand: {self.player_hand}")
        self.dealer_hand_label.setText(f"Dealer Hand: {self.dealer_hand}")
        self.game_state_label.setText("Hit or Stand?")

    def disable_buttons(self):
        self.hit_button.setDisabled(True)
        self.stand_button.setDisabled(True)

    def enable_buttons(self):
        self.hit_button.setDisabled(False)
        self.stand_button.setDisabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = BlackjackGame()
    game.show()
    sys.exit(app.exec_())