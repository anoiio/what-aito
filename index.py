from service.summary_worker import start_summary_schedule, execute_summary

CHATS_CONFIG = "config/summary/chats_summary_template.yml"

if __name__ == '__main__':
    # will execute configured chats summary immediately
    execute_summary(CHATS_CONFIG)

    # will schedule chats summary according to configuration
    #start_summary_schedule(CHATS_CONFIG)