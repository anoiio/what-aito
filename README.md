# What-aito is a WhatsApp AI automation

## Overview
This repository provides a solution for automated summarization of WhatsApp chat messages using OpenAI's GPT model. It fetches messages from specified channels, generates concise summaries of critical information, and sends these summaries to designated recipients. Configurable input, scheduling options, and integration with APIs make it an efficient way to manage and process chat data.

---

## Key Features
- **Customizable Summaries**: Focuses on essential updates like decisions, events, and topics while omitting casual or irrelevant conversations.
- **Integration with APIs**:
  - Fetches messages from a messaging platform via `whapi_api`.
  - Summarizes messages using OpenAI's GPT models.
  - Sends summarized messages back to specified recipients.
- **YAML-Based Configuration**: Fully customizable YAML config for source chat, target chat, summary parameters, and scheduling.
- **Automated Scheduling**: Leveraging cron syntax, summaries can be automatically generated at specified intervals.
---

## Prerequisites
- Python 3.9+
- Installed dependencies (see `requirements.txt`):
  - `requests`
  - `dotenv`
  - `PyYAML`
  - `flask`
  - `requests-toolbelt`

---

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```dotenv
     API_URL=<whapi_api_base_url>
     TOKEN=<whapi_api_auth_token>
     OPENAI_API_KEY=<openai_api_key>
     BOT_URL=<bot_webhook_url>  # Optional
     PORT=<port_number>         # Optional, default is 80/443
     ```

---

## Configuration
The behavior of the tool is configured in the `chats_summary_template.yml` file. Key configurable elements include:

1. **Source Chat**: Define the chat to summarize.
2. **Target Chat**: Specify where to send the summary.
3. **Summarization Parameters**: Set the model, token limit, and prompt for summarization.
4. **Scheduling**: Use cron-like syntax to automate periodic summarizations.

Example `chats_summary_template.yml`:
```yaml
chats:
  - source:
      chat_id: source_chat_id
      chat_name: Source Chat Nickname
      max_messages: 499
      summary_period_hours: 24
    target:
      chat_id: target_chat_id_or_phone
    summary:
      model: gpt-4o-mini
      max_output_tokens: 400
      prompt: chat_summary_daily
    scheduler:
      cron: "0 22 * * *"  # Runs daily at 10:00 PM
```

---

## Usage

### 1. Manual Execution
Run the summarization tool manually:
```bash
python index.py
```
This will generate a summary immediately based on the current configuration.

### 2. Scheduled Execution
To enable scheduled summarization, uncomment the following line in `index.py`:
```python
# start_summary_schedule(CHATS_CONFIG)
```
This uses the `summary_worker.py` to periodically perform summaries based on the configuration.

### 3. Webhook Server
Start the Flask server for handling Webhooks:
```bash
python whapi_server.py
```
The server will process incoming messages and can respond with specified actions.

---

## File Details
### Key Files
- `chat_summary_daily.txt`: Default GPT prompt template for summarization tasks.
- `chats_summary_template.yml`: Configuration file for defining source/target chats, scheduling, and summarization parameters.
- `prompts.py`: Retrieves and manages custom summarization prompts.
- `openAI_api.py`: Interface for interacting with OpenAI's GPT API.
- `whapi_api.py`: Handles interaction with the messaging platform's API for retrieval and summary delivery.
- `chanel_summary.py`: Core logic for fetching, summarizing, and sending chat updates.
- `summary_worker.py`: Implements scheduling functionality and triggers summarization as per configuration.
---

## Environment Variables
Set the following environmental variables in a `.env` file:
- **`API_URL`**: Base URL for the Whapi messaging platform API.
- **`TOKEN`**: Authorization token for Whapi API access.
- **`OPENAI_API_KEY`**: API key for OpenAI GPT integration.
- **`BOT_URL`**: (Optional) Webhook URL for message handling.
- **`PORT`**: (Optional) Port for running the webhook server.

---

## Example Workflow
1. **Fetch Messages**: Retrieve a predefined number of messages from a source chat using the `whapi_api`.
2. **Summarize Messages**: Pass the messages and prompt to an OpenAI GPT model to generate a concise summary.
3. **Send Messages**: Push the generated summary back to a target recipient using the messaging platform's API.
4. **Schedule Summarization**: Automate the summary generation and posting using cron-like scheduling.

---

## Notes
- Custom prompts for summarization can be created in `api/openAI/prompts/` and referenced in the configuration file.
- Ensure appropriate permissions for the environment variables and API usage.
- Adjust OpenAI parameters (like model and token limits) in the configuration or directly in the `openAI_api.py` implementation.

---

## Contributing
1. Fork this repository.
2. Create your feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## License
This repository is licensed under the MIT License. See the `LICENSE` file for details.

---

## Support
For questions or help with this repository, feel free to open an issue.