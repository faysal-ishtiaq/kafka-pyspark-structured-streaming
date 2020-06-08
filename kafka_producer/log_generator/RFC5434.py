import datetime
import random
import faker
import syslog_rfc5424_parser


class RFC5434:
    def __init__(self):
        self.line = ""
        self.priority_levels = list(range(24))
        self.version = 1
        self.faker = faker.Faker()
        self.facilities = ["kern", "user", "mail", "daemon", "auth", "syslog", "lpr", "news", "uucp", "cron", "authpriv", "ftp", "ntp", "security", "console", "solaris-cron", "local0", "local1", "local2", "local3", "local4", "local5", "local6", "local7"]
        self.severity_levels = list(range(8))

    def generate(self, hostname):
        version = self.version
        timestamp = datetime.datetime.now().astimezone().isoformat()
        priority_level = random.choice(self.priority_levels)
        facility = self.facilities[priority_level]
        severity = random.choice(self.severity_levels)
        priority = priority_level * 8 + severity
        pid = random.randint(1000, 2500)
        message = self.faker.bs()
        message_id = random.choice(list(range(100)))
        structured_data = "-"

        return f"<{priority}>{version} {timestamp} {hostname} {facility} {pid} {message_id} {structured_data} {message}"


if __name__ == "__main__":
    syslog_generator = RFC5434()

    print(syslog_rfc5424_parser.SyslogMessage.parse(syslog_generator.generate(faker.Faker().hostname())).as_dict())