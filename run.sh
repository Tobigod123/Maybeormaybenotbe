
#!/bin/bash

# Activate virtual environment if applicable
source venv/bin/activate

# Set environment variables if needed
export API_KEY="your_api_key"
export BOT_TOKEN="your_bot_token"

# Run the bot module
python3 -m bot

# Deactivate virtual environment if applicable
deactivate
