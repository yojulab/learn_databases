# Directory Overview

This directory contains a collection of SQL scripts and related files for learning and practicing database concepts. It is organized into two main folders: `cases` and `queries`.

## Key Files and Directories

### `cases/`

This directory contains various database schemas, each in its own subdirectory. Each subdirectory typically includes:

*   **`.vuerd` file:** A Visual ERD file that describes the database schema.
*   **`DDL.sql`:** Data Definition Language script for creating the tables and relationships.
*   **`DML.sql` or `DML/`:** Data Manipulation Language script(s) for inserting, updating, or deleting data.

Examples of database schemas in this directory include:

*   `db_authority`
*   `db_cars`
*   `db_members`
*   `db_memberwithauthority`
*   `db_pollswithresponsers`

### `queries/`

This directory contains various SQL queries, ranging from simple `SELECT` statements to more complex `JOIN` operations. Key files and subdirectories include:

*   **`information.sql`:** Basic SQL queries for table creation, insertion, selection, and deletion.
*   **`members.sql`:** Queries related to the `members` database schema.
*   **`organization_selfquery.sql`:** Queries demonstrating self-joins on an organization table.
*   **`Users_Auths_query.sql`:** Queries for a database schema involving users and authorizations.
*   **`codes/`:** Contains a Python script (`excel_sheet_to_sqlite.py`) for converting Excel sheets to a SQLite database.
*   **`quests/`:** Contains text files with SQL challenges or "quests" related to `JOIN` and `SELECT` statements.

## Usage

This directory is intended for educational purposes to learn and practice SQL. Users can:

1.  **Explore Database Schemas:** Examine the `.vuerd` files and `DDL.sql` scripts in the `cases` directory to understand different database designs.
2.  **Execute SQL Scripts:** Use the `DDL.sql` and `DML.sql` files to create and populate databases.
3.  **Practice SQL Queries:** Run the queries in the `queries` directory to practice various SQL commands.
4.  **Complete SQL Quests:** Use the files in `queries/quests` to challenge their SQL knowledge.
5.  **Convert Excel to SQLite:** Use the Python script in `queries/codes` to import data from Excel into a SQLite database.
