from requests import get
from bs4 import BeautifulSoup
from genanki import Deck, Model, Note, Package

# Request the page
url = "https://www.bigocheatsheet.com/"
response = get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table
tables = soup.find(id="tablesWrapper").find_all("table")
data_structures_table, array_sorting_algorithms = tables

# Create a new Anki deck
deck = Deck(
  1407883641,
  'Big-O Complexity')

# Create a new Anki model
model = Model(
  1955948737,
  'Simple Model Big-O',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

# Iterate over each row in the data_structures_table (skipping the first two header rows)
for row in data_structures_table.find_all('tr')[2:]:
    cells = row.find_all('td')
    
    # Check if the row has the correct number of cells
    if len(cells) == 10:
        data_structure = cells[0].text.strip()
        
        # Iterate over each operation (access, search, insert, delete)
        for i, operation in enumerate(['accessing', 'searching', 'inserting', 'deleting']):
            avg_time_complexity = cells[i + 1].text.strip()
            worst_time_complexity = cells[i + 5].text.strip()
            print(f"{data_structure} {operation} average {avg_time_complexity}")
            print(f"{data_structure} {operation} worst {worst_time_complexity}")

            ib = "a"
            match operation:
              case "inserting":
                ib = "into a"
              case "deleting":
                ib = "from a"
            # Create the questions and answers
            avg_question = f"What is the average time complexity of {operation} {ib} {data_structure}?"
            avg_answer = avg_time_complexity
            worst_question = f"What is the worst time complexity of {operation} {ib} {data_structure}?"
            worst_answer = worst_time_complexity
            
            # Create new Anki notes and add them to the deck
            avg_note = Note(
              model=model,
              fields=[avg_question, avg_answer])
            deck.add_note(avg_note)
            worst_note = Note(
              model=model,
              fields=[worst_question, worst_answer])
            deck.add_note(worst_note)

# Write the deck to a file
Package(deck).write_to_file('big_o_complexity.apkg')
