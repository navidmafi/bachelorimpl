import time
import random
from influxdb_client import InfluxDBClient, Point  # type: ignore
from influxdb_client.client.write_api import ASYNCHRONOUS
from influxdb_client.domain.write_precision import WritePrecision
import uuid

INFLUX_TOKEN = "sometoken"
INFLUX_BUCKET = "metrics"
INFLUX_ORG = "myorg"
INFLUX_URL = "http://localhost:8086"

client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG,
)

write_api = client.write_api(write_options=ASYNCHRONOUS)


run_id = uuid.uuid4()


step = 0
epoch = 0
while step < 100:

    # Simulate train loss
    train_loss = random.uniform(0.2, 1.0)
    point_train = (
        Point("loss_metrics")
        .tag("phase", "train")
        .field(f"value_{str(run_id)}", train_loss)
        .field("step", step)
        .time(time.time_ns(), WritePrecision.NS)
    )
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point_train)
    print(f"[{step}] run={run_id} TRAIN loss={train_loss:.4f}")

    # Simulate val loss every 5 steps
    if step % 5 == 0:
        val_loss = train_loss + random.uniform(0.01, 0.2)  # usually higher
        point_val = (
            Point("loss_metrics")
            .tag("phase", "val")
            .field(f"value_{str(run_id)}", val_loss)
            .field("step", step)
            .time(time.time_ns(), WritePrecision.NS)
        )
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point_val)
        print(f"[{step}] run={run_id}  VAL  loss={val_loss:.4f}")

    # Randomly increment epoch (every 3-6 steps)
    if step % random.randint(3, 6) == 0:
        epoch += 1

    step += 1
    time.sleep(0.5)  # simulate batch delay

# Ensure all async writes are flushed
write_api.flush()
client.close()
