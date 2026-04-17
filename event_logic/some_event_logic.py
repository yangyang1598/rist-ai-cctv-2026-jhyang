

class SomeEventLogic:
    def __init__(self, event_data):
        self.event_data = event_data

    def process_event(self):
        # Example processing logic
        if self.event_data.get('type') == 'example':
            return self.handle_example_event()
        else:
            return self.handle_default_event()

    def handle_example_event(self):
        # Logic for handling example event
        return f"Processed example event with data: {self.event_data}"

    def handle_default_event(self):
        # Logic for handling default event
        return f"Processed default event with data: {self.event_data}"