import tempfile,unittest
from pathlib import Path
from workflow import connect,plan,approve
class QueueTests(unittest.TestCase):
 def test_idempotent_daily_plan(self):
  with tempfile.TemporaryDirectory() as t:
   c=connect(Path(t));plan(c,'2026-11-07');plan(c,'2026-11-07');self.assertEqual(c.execute('select count(*) from jobs').fetchone()[0],6)
   plan(c,'2026-11-08');self.assertEqual(dict(c.execute('select channel,count(*) from jobs group by channel').fetchall()),{'ai':6,'quiz':6})
 def test_replan_preserves_existing_review(self):
  with tempfile.TemporaryDirectory() as t:
   c=connect(Path(t));plan(c,'2026-11-07')
   c.execute("UPDATE jobs SET state='review',manifest='kept' WHERE id='2026-11-07-1'");c.commit()
   plan(c,'2026-11-07')
   self.assertEqual(tuple(c.execute("SELECT state,manifest FROM jobs WHERE id='2026-11-07-1'").fetchone()),('review','kept'))
   self.assertEqual(dict(c.execute('SELECT channel,count(*) FROM jobs GROUP BY channel').fetchall()),{'ai':3,'quiz':3})
 def test_unverified_job_cannot_be_approved(self):
  with tempfile.TemporaryDirectory() as t:
   c=connect(Path(t));plan(c,'2026-11-07')
   with self.assertRaises(ValueError):approve(c,'2026-11-07-1')
if __name__=='__main__':unittest.main()
