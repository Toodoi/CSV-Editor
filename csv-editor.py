import pandas as pd
import numpy as np
from tabulate import tabulate
import sys

class CSVReader():

    def __init__(self):
        while True:
            csv_file = input('Please enter the CSV file name including the csv extension (.csv): ')
            try:
                with open(csv_file, 'r') as file:
                    self.df = pd.read_csv(file, encoding='utf-8-sig')
                    self.df = self.df.rename(columns=dict((col, col.strip('ï»¿')) for col in self.df.columns))
            except:
                print('File does not exist. Please make sure the file you wish to open is in your current directory '
                 'and you have included the csv extension in the file name\n')
                continue
            else:
                break
        self.cols = list(self.df.columns)

    def edits(self):
        print(f'The spreadsheet columns are: {self.cols}')
        print('\n')

        while True:
            col_to_filter = input('Enter the column you wish to filter by: ')
            if col_to_filter in self.cols:
                break
            else:
                print('The column you entered is not in the csv file, please try again.')

        while True:
            value_to_filter = input('Enter the value to filter on (type "#" to see possible values): ')
            if value_to_filter in list(self.df[col_to_filter]):
                break
            elif value_to_filter == '#':
                print(list(self.df[col_to_filter].unique()))
            else:
                print(f'The value you entered is not in the {col_to_filter} column, please try again.')
        print('Your filtered results are displayed below.')
        print(tabulate(self.df.loc[self.df[col_to_filter] == value_to_filter], headers='keys'))

        while True:
            edit_col = input('\nWhich column would you like to edit: ')
            if edit_col in self.cols:
                dtype = type(self.df[edit_col][0])
                break
            else:
                print('The column you entered is not in the csv file, please try again.')

        possible_values = self.df.loc[self.df[col_to_filter] == value_to_filter, edit_col].unique().astype(str)
        print(f'Filtering {col_to_filter} by {value_to_filter}, the possible values to edit in the {edit_col} column are: {possible_values}')
        while True:
            edit_value = input('Which value would you like to edit?: ')
            if edit_value in possible_values:
                break
            else:
                print('The value you entered is not valid based on your filter criteria, please try again.')

        if dtype == np.int64:
            edit_value = int(edit_value)
            replacement_value = int(input('Enter a replacement value: '))
        else:
            replacement_value = input('Enter a replacement value: ')

        self.df.loc[((self.df[col_to_filter] == value_to_filter) & (self.df[edit_col] == edit_value)), edit_col] = replacement_value
        print('\nYour changes have been made.')
        print(tabulate(self.df.loc[((self.df[col_to_filter] == value_to_filter) & (self.df[edit_col] == replacement_value))], headers='keys'))

        while True:
            is_additional_changes = input('Would you like to make any additional changes to the CSV file? (Y/N): ')
            if is_additional_changes == 'N':
                self.save_changes()
            elif is_additional_changes == 'Y':
                break

    def save_changes(self):
        while True:
            f_name = input('\nPlease enter new file name to save changes and include csv extension (.csv)\n'
                           'You may also specify the old file name to overwrite file: ')
            try:
                self.df.to_csv(f_name, mode='w+', index=False)
                print(f'Your file was written to {f_name} in your current directory.')
                sys.exit()
            except PermissionError:
                print('\nPermissionError: You may need to close the file before attempting to overwrite.')

    def main(self):
        while True:
            self.edits()

read = CSVReader().main()