# Requirements
1. The Latest version of Docker
1. At least 16 GB of RAM
1. At least 4 CPU cores

#### For Windows:
1. Download and install Chocolatey
1. Install Make via Chocolatey `choco install make`
1. I'm not too familiar with Windows, but I've read online that you might need to use PowerShell for this

#### For Mac
1. Make sure to provide Docker with at least 4 GB of RAM and 4 CPU cores.

# Instructions
1. Clone this repository to your documents
1. Open a terminal and navigate to the folder where the project is
1. Run the command `make run`
1. Run the command `make clean` to stop and remove all the containers

# Notes

### .env File
- Feel free to modify the ports in case you are already using any of them

### Database
- Database ER Diagram can be found in the "db_model.pdf" file at root level
- 'Active' column added to all tables for soft delete. No trigger created for this because I want to be able to actually 
  delete files, but be able to perform soft delete through data layer.
- Update trigger added to the database. This could potentially be expanded to include a column to register the user that
made the last change

### Kafka
- Kafka was chosen due to its scalability and performance
- Messages are stored in disk, so there's no loss of data
- Kafka also allows multiple consumer groups to subscribe to the same topic, without having to republish the message
  (like RabbitMQ)
  
### Kafka UI
- You can visualize topics and consumers by using the UI. 
- It's open at port 8080 by default, and can be changed through the .env file

### Kafka Worker
- Limited to 1 worker due to usage of sqlite. SQLite blocks the file when writing, so there's no benefit in adding more
  workers
- There is one worker per container so that it can be scaled by using `--scale` flag and be more transparent than using 
  processes inside the container
  
### Redis
- Redis was added to cache sqlalchemy objects and accelerate the processing of the messages. This helps when the latency
  between the database and the worker is greater than between the worker and the cache.
- The cache is flushed up periodically so that it doesn't consume too much RAM.

### FTP Client
- I chose Vaex to read the csv file because it reads it in chunks and stores it into a temp hdf5 file on disk, trading
  RAM for physical storage. This allows it to potentially handle files larger than RAM size. Vaex also offers performance 
  gains over pandas, so it's better suited for this task overall. 
- I scheduled only 1 message for the client to download the CSV file. It can be transformed to a periodical task by adding 
  another agent, but it would make the Kafka to consume a lot of resources.
