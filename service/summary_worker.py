import yaml
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from service.chanel_summary import summarize_and_send
from api.openAI.prompts.prompts import get_prompt


class ChatSummary:
    def __init__(self, config_path):
        """
        Initialize the ChatSummary class with the path to the YAML configuration file.

        :param config_path: Path to the YAML configuration file
        """
        self.config_path = config_path
        self.config = None
        self.scheduler = BackgroundScheduler()

    def load_config(self):
        """
        Load the YAML configuration file.
        """
        try:
            with open(self.config_path, 'r') as file:
                self.config = yaml.safe_load(file)
        except Exception as e:
            raise ValueError(f"Failed to load configuration file. Error: {e}")

    def schedule_chats(self):
        """
        Schedule the summarize_and_send function for all chats based on their cron settings.
        """
        if not self.config or "chats" not in self.config:
            raise ValueError("Invalid configuration format. No 'chats' section found.")

        for chat in self.config['chats']:
            try:
                # Extract required information from the configuration.
                (cron_expression,
                 source_chat_id,
                 source_chat_name,
                 summary_period_hours,
                 target_chat_id,
                 prompt_name,
                 model,
                 max_output_tokens) = (
                    self.get_chat_params(chat))

                # Parse the cron expression and schedule the task using APScheduler
                cron_trigger = CronTrigger.from_crontab(cron_expression)
                prompt = get_prompt(prompt_name)
                self.scheduler.add_job(
                    summarize_and_send,
                    trigger=cron_trigger,
                    args=[source_chat_id, source_chat_name, target_chat_id, summary_period_hours, prompt, model, max_output_tokens],
                    id=f"chat_summary_{source_chat_id}",  # Unique ID for each job
                    replace_existing=True
                )

                print(f"Scheduled summary for chat '{source_chat_id}' with cron '{cron_expression}'.")

            except ValueError as e:
                print(f"Invalid cron expression for chat: {e}")
            except Exception as e:
                print(f"Error scheduling chat: {e}")


    def execute_chats_summary(self):
        """
        Schedule the summarize_and_send function for all chats based on their cron settings.
        """
        if not self.config or "chats" not in self.config:
            raise ValueError("Invalid configuration format. No 'chats' section found.")

        for chat in self.config['chats']:
            try:
                # Extract required information from the configuration.
                (cron_expression,
                 source_chat_id,
                 source_chat_name,
                 summary_period_hours,
                 target_chat_id,
                 prompt_name,
                 model,
                 max_output_tokens) = (
                    self.get_chat_params(chat))

                prompt = get_prompt(prompt_name)
                summarize_and_send(source_chat_id, source_chat_name, target_chat_id, summary_period_hours, prompt, model, max_output_tokens)

            except Exception as e:
                print(f"Error executing chat summary: {e}")



    def get_chat_params(self, chat):
        try:
            source_chat_id = chat['source']['chat_id']
            source_chat_name = chat['source']['chat_name']
            summary_period_hours = chat['source']['summary_period_hours']
            target_chat_id = chat['target']['chat_id']
            cron_expression = chat['scheduler']['cron']
            prompt_name = chat['summary']['prompt']
            model = chat['summary']['model']
            max_output_tokens = chat['summary']['max_output_tokens']
        except KeyError as e:
            print(f"Missing required configuration key: {e}")
            raise e

        return cron_expression, source_chat_id, source_chat_name, summary_period_hours, target_chat_id, prompt_name, model, max_output_tokens

    def start_scheduler(self):
        """
        Start the scheduler to execute scheduled tasks.
        """
        print("Scheduler is starting...")
        self.scheduler.start()
        try:
            # Keep the scheduler running
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            print("Shutting down the scheduler...")
            self.scheduler.shutdown()


def start_summary_schedule(config_path):
    chat_summary = ChatSummary(config_path)

    chat_summary.load_config()
    chat_summary.schedule_chats()
    chat_summary.start_scheduler()

def execute_summary(config_path):
    chat_summary = ChatSummary(config_path)

    chat_summary.load_config()
    chat_summary.execute_chats_summary()
