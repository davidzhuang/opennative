from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'instance1 instances2'
    help = 'Display command arguments'

    def handle(self, *args, **options):
        self.stdout.write("args: ")
        for arg in args:
            print arg

        self.stdout.write("\noptions: ")
        keys = options.keys()
        for key in keys:
            print key, "=", options[key]
            #self.stdout.write(key, "=", options[key], ", ")
