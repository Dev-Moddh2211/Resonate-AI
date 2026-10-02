import unittest
from realtime.service import RealtimeRegistry
from realtime.stream import ReplayStream

class PollingServiceTests(unittest.TestCase):
    def test_poll_returns_new_event_and_cursor(self):
        registry=RealtimeRegistry(); pipeline=registry.create('poll-call')
        chunk=next(iter(ReplayStream('poll-call',[{'speaker':'customer','text':'Can you call me tomorrow?','timestamp_ms':1000}],deterministic=True)))
        pipeline.process(chunk)
        first=registry.poll('poll-call',0)
        self.assertEqual(len(first['events']),1); self.assertEqual(first['cursor'],1)
        self.assertEqual(registry.poll('poll-call',first['cursor'])['events'],[])
