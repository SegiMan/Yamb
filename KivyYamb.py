import random
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.anchorlayout import AnchorLayout
import multiexpressionbutton as meb
from kivy.clock import Clock

Builder.load_file('Yamb.kv')


class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)

        # Set columns
        self.cols = 7
        self.entry_variables = []  # List to store variables corresponding to labels
        self.sum_variables = []
        self.left_rolls = 3
        row_label_list = ["1", "2", "3", "4", "5", "6", "\u03A3", "MAX", "MIN", "\u03A3",
                          "2 PAIR", "STR", "FULL", "POKER", "YAMB", "\u03A3"]
        column_label_list = ["\u2193", "\u2191", "\u2191\u2193", "CALL", "", ""]
        self.text_hover = False
        self.results = Spinner(text="Scores", values=(), background_color="black")
        self.add_widget(self.results)

        for text in column_label_list:
            self.label = Label(text=text)
            self.add_widget(self.label)

        for i in range(0, len(row_label_list)):
            self.entry_variables.append([])
            self.label_temp_1 = Label(text=row_label_list[i])
            self.add_widget(self.label_temp_1)
            if (i != 6) and (i != 9) and (i != 15):
                for j in range(0, 4):
                    self.text_input = meb.MultiExpressionButton(text="")
                    self.text_input.bind(on_single_press=lambda instance, idx1=i, idx2=j: self.single_click(idx1, idx2))
                    self.text_input.bind(on_double_press=lambda instance, idx1=i, idx2=j: self.double_click(idx1, idx2))
                    self.text_input.bind(on_long_press=lambda instance, idx1=i, idx2=j: self.long_press(idx1, idx2))
                    self.add_widget(self.text_input)
                    self.entry_variables[i].append(self.text_input)  # Append entry to the list of variables
                self.label_temp_2 = Label(text="")
                self.add_widget(self.label_temp_2)
                self.label_temp_3 = Label(text="")
                self.add_widget(self.label_temp_3)
            else:
                for j in range(0, 4):
                    self.text_input = Button(text="0", background_color="green")
                    self.add_widget(self.text_input)
                    self.entry_variables[i].append(self.text_input)  # Append entry to the list of variables
                self.label_temp_4 = Label(text="\u03A3")
                self.add_widget(self.label_temp_4)
                self.text_input_temp = Button(text="0", background_color="green")
                self.sum_variables.append(self.text_input_temp)
                self.add_widget(self.text_input_temp)

        self.label_rand = Button(text="Start: " + str(random.randint(5, 30)), background_color="red")
        self.label_rand.bind(on_press=self.random_generate)
        self.add_widget(self.label_rand)

        self.reset = Button(text="Reset!", background_color="red")
        self.reset.bind(on_press=self.reset_game)
        self.add_widget(self.reset)

        self.new_game = Button(text="New!", background_color="red")
        self.new_game.bind(on_press=self.new_game_function)
        self.add_widget(self.new_game)

        self.roll = Button(text="Roll!", background_color="red")
        self.roll.bind(on_press=self.roll_dice)
        self.add_widget(self.roll)

        self.sum = Button(text="Sum: 15", background_color="red")
        self.add_widget(self.sum)

        self.label_sum = Label(text="\u03A3")
        self.add_widget(self.label_sum)
        self.final_score = Button(text="0", background_color="green")
        self.add_widget(self.final_score)

        for i in range(0, 7):
            self.label_temp_6 = Label(text="", size_hint_y=None, height=40, size_hint_x=None, width=40)
            self.add_widget(self.label_temp_6)

        self.dice_buttons = []

        for i in range(1, 7):
            # Create a Button with an AsyncImage as its background
            self.dice_button = Button(background_normal=f"{i}_roll.png", background_down=f"{i}_roll.png",
                                      size=(100, 100), size_hint_y=None, height=100, size_hint_x=None, width=100)

            # dice_button.bind(on_press=on_button_click)
            if i != 6:
                self.dice_buttons.append(self.dice_button)
                self.layout_temp = AnchorLayout(anchor_x='center', anchor_y='center')
                self.layout_temp.add_widget(self.dice_button)
                self.add_widget(self.layout_temp)

        for i in range(0, len(self.dice_buttons)):
            self.dice_buttons[i].bind(on_press=lambda instance, idx=i: self.roll_or_keep_dice(idx))

        self.rolls_left = Label(text="ROLLS LEFT:")
        self.add_widget(self.rolls_left)

        self.rolls_left = Label(text=str(self.left_rolls))
        self.add_widget(self.rolls_left)

        for i in range(0, 7):
            self.label_temp_7 = Label(text="", size_hint_y=None, height=40, size_hint_x=None, width=40)
            self.add_widget(self.label_temp_7)

        dice_to_keep = []
        dice_to_roll = []

        for i in range(1, 7):
            dice_keep_path = f"{i}_keep.png"
            dice_to_keep.append(dice_keep_path)

            dice_roll_path = f"{i}_roll.png"
            dice_to_roll.append(dice_roll_path)

        self.keep_or_roll = [False] * 5
        self.dice_values = list(range(1, 6))

        self.timer = 0

    def random_generate(self, instance):
        self.label_rand.text = "Start: " + str(random.randint(5, 30))

    def reset_game(self, instance):
        if self.reset.text == "Reset!":
            self.reset.text = "Sure?"
            time.sleep(1)
            # Schedule the revert function after 5 seconds
            Clock.schedule_once(self.reset_reset_text, 5)
        else:
            for row in range(0, len(self.entry_variables)):
                for col in range(0, len(self.entry_variables[row])):
                    self.entry_variables[row][col].color = "black"
                    self.entry_variables[row][col].text = ""

            self.reset_dice()
            self.sum_things_up()
            self.reset.text = "Reset!"
            self.left_rolls = 3
            self.rolls_left.text = "3"

    def reset_reset_text(self, instance):
        self.reset.text = "Reset!"

    def new_game_function(self, instance):
        if self.new_game.text == "New!":
            self.new_game.text = "Sure?"
            time.sleep(1)
            # Schedule the revert function after 5 seconds
            Clock.schedule_once(self.reset_new_text, 5)
        else:
            self.results.values.append(str(self.final_score.text))

            for row in range(0, len(self.entry_variables)):
                for col in range(0, len(self.entry_variables[row])):
                    self.entry_variables[row][col].color = "black"
                    self.entry_variables[row][col].text = ""

            self.reset_dice()
            self.sum_things_up()
            self.new_game.text = "New!"
            self.left_rolls = 3
            self.rolls_left.text = "3"

    def reset_new_text(self, instance):
        self.new_game.text = "New!"

    def revert_text_single(self, dt):
        # Revert the text to ""
        for row in range(0, len(self.entry_variables)):
            for col in range(0, len(self.entry_variables[row])):
                if self.entry_variables[row][col].color == [1, 1, 1, 0.5]:
                    self.entry_variables[row][col].color = "black"
                    self.entry_variables[row][col].text = ""

    def revert_text(self):
        # Revert the text to ""
        for row in range(0, len(self.entry_variables)):
            for col in range(0, len(self.entry_variables[row])):
                if self.entry_variables[row][col].color == [1, 1, 1, 0.5]:
                    self.entry_variables[row][col].color = "black"
                    self.entry_variables[row][col].text = ""

    def single_click(self, row, col):
        if self.text_hover is False:
            self.text_hover = True
        else:
            self.revert_text()
            self.text_hover = False

        if self.text_hover is True:
            CanThisEntryBeFilledNow = True

            # Check if the current entry can be filled for column 1
            if col == 0:
                for t in range(0, row):
                    if (self.entry_variables[t][col].text == "") and (t != 6) and (t != 9) and (t != 15):
                        CanThisEntryBeFilledNow = False

            if col == 1:
                for t in range(row, 15):
                    if (self.entry_variables[t][col].text == "") and (t != 6) and (t != 9) and (t != row):
                        CanThisEntryBeFilledNow = False

            if (self.entry_variables[row][col].text == "") and (CanThisEntryBeFilledNow is True):

                # Check for digits
                for t in range(0, 6):
                    if row == t:
                        in_val = self.check_for_digit(t + 1) * (t + 1)
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)

                if (row == 7) or (row == 8):
                    in_val = sum(self.dice_values)
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)

                if row == 10:
                    in_val = self.check_for_two_pairs()
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)

                if row == 11:
                    in_val = self.check_for_straight()
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)

                if row == 12:
                    in_val = self.check_for_full_house()
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)

                if row == 13:
                    in_val = self.check_for_poker()
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)

                if row == 14:
                    in_val = self.check_for_yamb()
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 0.5)

            # Schedule the revert function after 5 seconds
            Clock.schedule_once(self.revert_text_single, 3)

    def double_click(self, row, col):
        if self.left_rolls != 3:
            CanThisEntryBeFilledNow = True

            # Check if the current entry can be filled for column 1
            if col == 0:
                for t in range(0, row):
                    if (self.entry_variables[t][col].text == "") and (t != 6) and (t != 9) and (t != 15):
                        CanThisEntryBeFilledNow = False

            if col == 1:
                for t in range(row, 15):
                    if (self.entry_variables[t][col].text == "") and (t != 6) and (t != 9) and (t != row):
                        CanThisEntryBeFilledNow = False

            if (self.entry_variables[row][col].text == "") and (CanThisEntryBeFilledNow is True):

                # Check for digits
                for t in range(0, 6):
                    if row == t:
                        in_val = self.check_for_digit(t + 1) * (t + 1)
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 1)

                if (row == 7) or (row == 8):
                    in_val = sum(self.dice_values)
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 1)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 1)

                if row == 10:
                    in_val = self.check_for_two_pairs()
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 1)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 1)

                if row == 11:
                    in_val = self.check_for_straight()
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 1)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 1)

                if row == 12:
                    in_val = self.check_for_full_house()
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 1)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 1)

                if row == 13:
                    in_val = self.check_for_poker()
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 1)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 1)

                if row == 14:
                    in_val = self.check_for_yamb()
                    if in_val != 0:
                        self.entry_variables[row][col].text = str(in_val)
                        self.entry_variables[row][col].color = (1, 1, 1, 1)
                    else:
                        self.entry_variables[row][col].text = "/"
                        self.entry_variables[row][col].color = (1, 1, 1, 1)

            self.reset_dice()
            self.sum_things_up()
            self.left_rolls = 3
            self.rolls_left.text = "3"
            self.roll.disabled = False

    def long_press(self, row, col):
        CanThisEntryBeFilledNow = True

        # Check if the current entry can be filled for column 1
        if col == 0:
            for t in range(0, row):
                if (self.entry_variables[t][col].text == "") and (t != 6) and (t != 9) and (t != 15):
                    CanThisEntryBeFilledNow = False

        if col == 1:
            for t in range(row, 15):
                if (self.entry_variables[t][col].text == "") and (t != 6) and (t != 9) and (t != row):
                    CanThisEntryBeFilledNow = False

        if (self.entry_variables[row][col].text == "") and (CanThisEntryBeFilledNow is True):

            self.entry_variables[row][col].text = "/"
            self.reset_dice()
            self.sum_things_up()
            self.left_rolls = 3
            self.rolls_left.text = "3"
            self.roll.disabled = False

    def update_roll_dice(self, dt):
        for ii in range(0, 5):
            # Keep die = True, red; Roll die = False, black
            if self.keep_or_roll[ii] is False:
                roll_val = random.randint(1, 6)
                self.dice_values[ii] = roll_val

        for ii in range(0, 5):
            if self.keep_or_roll[ii] is False:
                self.dice_buttons[ii].background_normal = f"{self.dice_values[ii]}_roll.png"
                self.dice_buttons[ii].background_down = f"{self.dice_values[ii]}_roll.png"
            else:
                self.dice_buttons[ii].background_normal = f"{self.dice_values[ii]}_keep.png"
                self.dice_buttons[ii].background_down = f"{self.dice_values[ii]}_keep.png"
        # Stop the rolling process after 1.5 seconds (15 iterations with 0.1-second interval)
        self.timer = self.timer + dt
        if self.timer > 0.5:
            Clock.unschedule(self.update_roll_dice)
            self.sum.text = "Sum: " + str(sum(self.dice_values))
            self.timer = 0

    def roll_dice(self, instance):
        if self.left_rolls > 0:
            self.left_rolls = self.left_rolls - 1
            self.rolls_left.text = str(self.left_rolls)
            self.revert_text()
            self.sum_things_up()
            Clock.schedule_interval(self.update_roll_dice, 0.1)
            if self.left_rolls == 0:
                self.roll.disabled = True
        else:
            self.roll.disabled = True

    def roll_or_keep_dice(self, index):
        # Keep die = True, red; Roll die = False, black
        if self.keep_or_roll[index] is False:
            self.keep_or_roll[index] = True
            self.dice_buttons[index].background_normal = f"{self.dice_values[index]}_keep.png"
            self.dice_buttons[index].background_down = f"{self.dice_values[index]}_keep.png"
        else:
            self.keep_or_roll[index] = False
            self.dice_buttons[index].background_normal = f"{self.dice_values[index]}_roll.png"
            self.dice_buttons[index].background_down = f"{self.dice_values[index]}_roll.png"

    def reset_dice(self):
        for kk in range(0, 5):
            self.keep_or_roll[kk] = False
            self.dice_buttons[kk].background_normal = f"{self.dice_values[kk]}_roll.png"
            self.dice_buttons[kk].background_down = f"{self.dice_values[kk]}_roll.png"
    
    def check_for_digit(self, num):
        val_list = [value for value in self.dice_values]
        return val_list.count(num)

    def check_for_two_pairs(self):
        val_list = [value for value in self.dice_values]
        # Initialize a dictionary to keep track of the counts of each value
        counts = {}
        for val in val_list:
            counts[val] = counts.get(val, 0) + 1

        # Check if there are two pairs or a full house in the counts dictionary
        pairs = [key for key, value in counts.items() if value == 2]
        threes = [key for key, value in counts.items() if value == 3]
        result = 0
        if len(pairs) == 2:
            result = sum(pairs) * 2 + 10
        if (len(pairs) == 1) and (len(threes) == 1):
            result = sum(pairs) * 2 + sum(threes) * 2 + 10
        return result

    def check_for_full_house(self):
        val_list = [value for value in self.dice_values]
        # Initialize a dictionary to keep track of the counts of each value
        counts = {}
        for val in val_list:
            counts[val] = counts.get(val, 0) + 1

        # Check if there is a full house in the counts dictionary
        values = list(counts.values())
        if 2 in values and 3 in values:
            return sum(val_list) + 30  # Return the sum of all values in the list
        else:
            return 0  # Return 0 if there is no full house

    def check_for_poker(self):
        the_val = 0
        for t in range(1, 7):
            if self.check_for_digit(t) >= 4:
                the_val = 4 * t + 40

        return the_val  # Return the sum of all values in the list

    def check_for_yamb(self):
        the_val = 0
        for t in range(1, 7):
            if self.check_for_digit(t) == 5:
                the_val = 5 * t + 50

        return the_val  # Return the sum of all values in the list

    def check_for_straight(self):
        val_list = [value for value in self.dice_values]
        # Sort the list of values in ascending order
        val_list = sorted(val_list)

        # Check if the values form a straight
        if val_list == [1, 2, 3, 4, 5]:
            return 35
        elif val_list == [2, 3, 4, 5, 6]:
            return 45
        else:
            return 0

    def get_entry_value(self, variable):
        if (variable.text == "") or (variable.text == "/") or (variable.color == [1, 1, 1, 0.5]):
            value = 0
        else:
            value = int(variable.text)

        return value

    def sum_things_up(self):
        for k in range(0, 4):
            sum_num = sum(self.get_entry_value(self.entry_variables[i][k]) for i in range(6))
            if sum_num < 60:
                self.entry_variables[6][k].text = str(sum_num)
            else:
                self.entry_variables[6][k].text = str(sum_num + 30)

        self.sum_variables[0].text = str(sum(self.get_entry_value(self.entry_variables[6][i]) for i in range(4)))

        for k in range(0, 4):
            self.entry_variables[9][k].text = str(((self.get_entry_value(self.entry_variables[7][k]) -
                                                    self.get_entry_value(self.entry_variables[8][k])) *
                                                   self.get_entry_value(self.entry_variables[0][k])))

        self.sum_variables[1].text = str(sum(self.get_entry_value(self.entry_variables[9][i]) for i in range(4)))

        for k in range(0, 4):
            sum_num = sum(self.get_entry_value(self.entry_variables[i][k]) for i in range(10, 15))
            self.entry_variables[15][k].text = str(sum_num)

        self.sum_variables[2].text = str(sum(self.get_entry_value(self.entry_variables[15][i]) for i in range(4)))

        self.final_score.text = str(sum(self.get_entry_value(self.sum_variables[i]) for i in range(3)))


class YambMarkoApp(App):
    def build(self):
        return MyGridLayout()


if __name__ == "__main__":
    YambMarkoApp().run()
