# Instructions
1. Install the latest version of Docker Desktop into your workstation
1. Clone this repository to your documents
1. Open a terminal and navigate to the folder where the project is
1. Run the command `docker compose -d --build up`

# Notes
### Database
- Database ER Diagram can be found in the "db_model.pdf" file at root level
- 'Active' column added to all tables for soft delete. No trigger created for this because I want to be able to actually 
  delete files, but be able to perform soft delete through data layer.
- Update trigger added to the database. This could potentially be expanded to include a column to register the user that
made the last change



### Kafka Worker
- Limited to 1 worker due to usage of sqlite.
- Architecture is designed with a production database (like PostgreSQL) in mind.