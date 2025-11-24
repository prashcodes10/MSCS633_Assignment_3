import sys
from django.core.management.base import BaseCommand
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


class Command(BaseCommand):
    help = 'Launching an interactive terminal conversation with the AI assistant'

    def handle(self, *args, **options):
        # Creating an AI assistant instance with database and logic adapters
        ai_assistant = ChatBot(
            'TerminalAssistant',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            logic_adapters=[
                'chatterbot.logic.BestMatch',              # Handling general conversation
                'chatterbot.logic.TimeLogicAdapter',       # Responding with current time
                'chatterbot.logic.MathematicalEvaluation' # Solving mathematical expressions
            ],
            database_uri='sqlite:///assistant_db.sqlite3'
        )

        # Training the AI assistant on English language corpus
        trainer = ChatterBotCorpusTrainer(ai_assistant)
        trainer.train('chatterbot.corpus.english')

        # Displaying startup message and informing how to exit
        self.stdout.write(self.style.SUCCESS(
            'Starting conversation! (Typing "exit" or using Ctrl-C to quit)\n'
        ))

        # Running conversation loop continuously
        while True:
            try:
                # Asking user for input continuously
                user_message = input('You: ').strip()

                # Skipping if the user is entering nothing
                if not user_message:
                    continue

                # Checking if the user is typing exit command
                if user_message.lower() == 'exit':
                    self.stdout.write('\nEnding conversation. Goodbye!')
                    break

                # Generating assistant response and displaying it
                response_message = ai_assistant.get_response(user_message)
                self.stdout.write(f'Assistant: {response_message}')

            # Handling Ctrl-C or Ctrl-D interruptions gracefully
            except (KeyboardInterrupt, EOFError):
                self.stdout.write('\nEnding conversation. Goodbye!')
                break

        # Displaying final exit message
        self.stdout.write(self.style.ERROR('Conversation session is ending!'))
        sys.exit(0)
