# Assignment 4: Natural Language to SQL Query Generator

## Description

This project implements a system that converts natural language questions about Bitcoin transaction data into SQL queries. The system utilizes the OpenAI API (model="gpt-3.5-turbo") to generate SQL statements based on user input and the schema of a given SQLite database.

- **Natural Language Processing**: Users can input questions in natural language, and the system will generate corresponding SQL queries.
- **Database Interaction**: The system connects to a SQLite database containing Bitcoin transaction data, allowing for dynamic query generation based on the current schema.
- **OpenAI Integration**: Utilizes OpenAI's GPT-3.5-turbo model to interpret user questions and generate SQL statements.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AnjaliK-123/blockchain_project.git
   cd blockchain_project/assignment-4
   ```
2. Run the following installation commands in the terminal:
   - pip install pandas
   - pip install openai

## Run the main script

python3 user_interaction.py

## View Database in terminal

python3 view_db.py
