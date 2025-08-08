SAMPLES=50000
THREADS=8
SEED="your_seed_here"

# 1. List all files and sort
rsync --no-motd --list-only rsync://176.9.41.242:873/biggan/portraits/ \
  | awk '{print $5}' \
  | sort > all_files_sorted.txt

# 2. Deterministic shuffle
openssl enc -aes-256-ctr -pass pass:$SEED -nosalt </dev/zero 2>/dev/null \
  | shuf --random-source=/dev/stdin all_files_sorted.txt > shuffled.txt

# 3. Pick top $SAMPLES
head -n $SAMPLES shuffled.txt > selected.txt

# 4. Split evenly into $THREADS
split -d -n l/$THREADS selected.txt chunk_

# 5. Parallel rsync
echo "Starting multithreaded download"
for chunk in chunk_??; do
  rsync -av -R \
    --files-from="$chunk" \
    rsync://176.9.41.242:873/biggan/portraits/ \
    ./portraits/ &
done
wait

