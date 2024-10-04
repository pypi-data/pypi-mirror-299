import sys

import gibson.core.Colors as Colors
from gibson.api.Cli import Cli
from gibson.command.BaseCommand import BaseCommand
from gibson.core.TimeKeeper import TimeKeeper
from gibson.dev.Dev import Dev


class Test(BaseCommand):
    def execute(self, entity_name=sys.argv[3]):
        self.configuration.require_project()
        entity = self.memory.recall_stored_entity(entity_name)
        if entity is None:
            self.conversation.not_sure_no_entity(
                self.configuration.project.name, entity_name
            )
            exit(1)

        time_keeper = TimeKeeper()

        cli = Cli(self.configuration)
        response = cli.code_testing([entity["name"]])

        Dev(self.configuration).tests(
            response["code"][0]["entity"]["name"], response["code"][0]["definition"]
        )

        if self.configuration.project.dev.active is True:
            self.conversation.type(
                f"Gibson wrote the following {Colors.argument('tests')} to your project:\n"
            )

        print(response["code"][0]["definition"])
        time_keeper.display()
