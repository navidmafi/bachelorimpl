CREATE TABLE runs (
run_id UUID PRIMARY KEY,
started_at TIMESTAMP WITH TIME ZONE,
hyperparams JSONB
);
CREATE TABLE metrics (
    run_id UUID REFERENCES runs(run_id),
    epoch INT,
    phase TEXT CHECK (phase IN ('train', 'val')),
    metric TEXT,
 logged_at  TIMESTAMP(6) WITH TIME ZONE,
    value DOUBLE PRECISION,
    PRIMARY KEY (run_id, epoch, phase, metric)
);


-- ALTER TABLE runs
--   ALTER COLUMN started_at TYPE TIMESTAMPTZ
--   USING started_at AT TIME ZONE 'Asia/Tehran';

-- ALTER TABLE runs
-- ALTER COLUMN started_at TYPE TIMESTAMP
-- USING started_at AT TIME ZONE 'UTC';


-- ALTER TABLE runs
-- ALTER COLUMN started_at DROP DEFAULT

-- ALTER TABLE metrics
-- ALTER COLUMN logged_at DROP DEFAULT


-- TZ FIX

-- ALTER TABLE runs ADD COLUMN started_at_fixed TIMESTAMPTZ;

-- UPDATE runs
-- SET started_at_fixed = started_at AT TIME ZONE 'Asia/Tehran';

-- SELECT started_at, started_at_fixed FROM runs LIMIT 10;
-- ALTER TABLE runs DROP COLUMN started_at;
-- ALTER TABLE runs RENAME COLUMN started_at_fixed TO started_at;

-- SELECT * from runs ORDER BY started_at DESC

-- ------------------------------


-- ALTER TABLE metrics ADD COLUMN logged_at_fixed TIMESTAMPTZ;
-- UPDATE metrics
-- SET logged_at_fixed = logged_at AT TIME ZONE 'Asia/Tehran';

-- ALTER TABLE metrics DROP COLUMN logged_at;
-- ALTER TABLE metrics RENAME COLUMN logged_at_fixed TO logged_at;

-- SELECT * from metrics ORDER BY logged_at DESC



-- Shift epochs

BEGIN;
ALTER TABLE metrics
  DROP CONSTRAINT IF EXISTS metrics_pkey;
 UPDATE metrics
   SET epoch = epoch + 1;
ALTER TABLE metrics
  ADD PRIMARY KEY (run_id, epoch, phase, metric);
COMMIT;
