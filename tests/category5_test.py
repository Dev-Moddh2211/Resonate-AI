import unittest
import tempfile, wave
from realtime.stream import ReplayStream
from realtime.pipeline import RealtimePipeline
from realtime.metrics import latency_report
from realtime.audio import wav_chunks
from realtime.asr import ChunkASR

class Category5Tests(unittest.TestCase):
    def run_call(self, rows):
        p=RealtimePipeline()
        for chunk in ReplayStream('call-5', rows, deterministic=True): p.process(chunk)
        return p
    def test_incremental_missed_opportunity(self):
        p=self.run_call([{'speaker':'customer','text':'We are expanding into another location.','timestamp_ms':1000}])
        self.assertEqual(p.events[0]['nudges'][0]['signal_id'],'missed_opportunity')
    def test_compliance_only_agent(self):
        p=self.run_call([{'speaker':'agent','text':'Your loan is definitely approved.','timestamp_ms':1000}])
        self.assertEqual(p.events[0]['nudges'][0]['signal_id'],'compliance_gap')
    def test_noise_does_not_nudge(self):
        p=self.run_call([{'speaker':'customer','text':'[noise] frustrated? maybe not clear','timestamp_ms':1000}])
        self.assertFalse(p.events[0]['nudges'])
    def test_duplicate_suppression(self):
        p=self.run_call([{'speaker':'customer','text':'This is frustrating.','timestamp_ms':1000},{'speaker':'customer','text':'I am frustrated.','timestamp_ms':2000}])
        self.assertEqual(sum(len(e['nudges']) for e in p.events),1)
    def test_latency_report_is_measured(self):
        p=self.run_call([{'speaker':'customer','text':'Can you call me tomorrow afternoon?','timestamp_ms':1000}])
        report=latency_report(p.latencies)
        self.assertEqual(report['end_to_end_ms']['sample_count'],1)
        self.assertIsNotNone(report['end_to_end_ms']['p50'])
    def test_polling_cursor_and_call_isolation(self):
        a=self.run_call([{'speaker':'agent','text':'Your loan is definitely approved.','timestamp_ms':1000}])
        b=self.run_call([{'speaker':'customer','text':'Can you call me tomorrow?','timestamp_ms':1000}])
        events, cursor=a.poll(0)
        self.assertEqual(events[0]['nudges'][0]['call_id'], 'call-5')
        self.assertNotEqual(a.nudges.history[0]['signal_id'], b.nudges.history[0]['signal_id'])
        self.assertEqual(cursor, 1)
    def test_cooldown_and_expiry_controls(self):
        p=self.run_call([{'speaker':'customer','text':'This is frustrating.','timestamp_ms':1000},{'speaker':'customer','text':'I am frustrated.','timestamp_ms':2000}])
        self.assertEqual(len(p.nudges.history), 1)
        p.nudges.active['rising_frustration']['expires_at']='2000-01-01T00:00:00+00:00'
        p.nudges.expire('2026-01-01T00:00:00+00:00')
        self.assertFalse(p.nudges.active)
    def test_real_wav_is_chunked_and_asr_failure_is_visible(self):
        with tempfile.NamedTemporaryFile(suffix='.wav') as f:
            with wave.open(f.name, 'wb') as out:
                out.setnchannels(1); out.setsampwidth(2); out.setframerate(8000); out.writeframes(b'\0\0' * 8000 * 2)
            chunks=list(wav_chunks(f.name, 'audio-call', 1000))
        self.assertEqual(len(chunks), 2)
        result=RealtimePipeline().process_audio_chunk(chunks[0], ChunkASR(executable='missing-asr'))
        self.assertIsNotNone(result['audio']['asr_error'])
        self.assertIsNone(result['transcript'])
