# Instructions
1. Install the latest version of Docker Desktop into your workstation
1. Clone this repository to your documents
1. Open a terminal and navigate to the folder where the project is
1. Run the command `make run`

# Notes
### Database
- Database ER Diagram can be found in the "db_model.pdf" file at root level
- 'Active' column added to all tables for soft delete. No trigger created for this because I want to be able to actually 
  delete files, but be able to perform soft delete through data layer.
- Update trigger added to the database. This could potentially be expanded to include a column to register the user that
made the last change

### Messaging platform
- Kafka was chosen due to its scalability and performance
- Kafka also allows multiple consumer groups to subscribe to the same topic, without having to republish the message
  (like RabbitMQ)

### Kafka Worker
- Limited to 1 worker due to usage of sqlite. SQLite blocks the file when writing, so there's no benefit in adding more
  workers
- There is one worker per container so that it can be scaled by using `--scale` flag and be more transparent than using 
  processes inside the container