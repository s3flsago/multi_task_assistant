# Multi-Task Assistant

The **Multi-Task Assistant** is a versatile tool designed to support users in various tasks through a chat interface. The framework is modular, allowing for the implementation of additional assistants as needed.

## Features
### Currently Implemented Assistants:
- **Flat Finance Helper**: Analyzes and splits expenses from scanned shopping receipts.
- **Language Practice Assistant**: Assists with studying irregular verbs in foreign languages.

## Development
To set up the development environment:
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the application:
   ```bash
   bash startup.sh
   ```

## Continuous Integration & Deployment (CI/CD)
- The Docker image is built and pushed via GitHub Actions.
- The image is deployable to an Azure App Service for seamless cloud execution.

## Testing
Run unit tests using:
```bash
pytest
```

## Running the Assistant Locally
To build and run the assistant locally using Docker:
1. Build the Docker image:
   ```bash
   docker build -t multi_task_assistant:0.1 .
   ```
2. Run the container:
   ```bash
   docker run multi_task_assistant:0.1 /bin/bash
   ```

## How to Use
### Setting Up the Assistant on Telegram
1. Open Telegram on your phone or desktop.
2. Create a bot using Telegram’s **BotFather**.
3. Start a conversation with the assistant by sending a greeting.

### Example Usage
#### Language Practice Assistant
```
User: Hi!

Bot: Hello! How many verbs would you like to quiz today, and in which language?

User: Three verbs in Spanish, please.

Bot: Great choice! Let's start with the first verb.
     What is the form of "ser" for "él/ella" in the "futuro indicativo"?

User: Seré

Bot: That's close, but not quite right!

     The correct form of "ser" for "él/ella" in the "futuro indicativo" is **"será."**

     Here's a quick reference for "ser" in the "futuro indicativo":
     - yo **seré**
     - tú **serás**
     - él/ella **será**
     - nosotros **seremos**
     - vosotros **seréis**
     - ellos/ellas **serán**

     Now, let's move on to the next verb!
     What is the form of "caber" for "nosotros" in the "subjuntivo presente"?
```

## Future Enhancements
- Integration with additional messaging platforms.
- Expansion of available assistants for broader functionality.



