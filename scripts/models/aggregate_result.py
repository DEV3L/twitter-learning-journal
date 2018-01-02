class AggregateResult:
    def __init__(self, medium):
        self.medium = medium

        self.item_count = 0
        self.kcv = 0

        self.timeline = {}  # { 'date': {'category': count} }
        self.report_entries = []
