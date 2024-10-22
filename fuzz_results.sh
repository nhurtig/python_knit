for i in {0..17}; do grep -n "Process $i:" word_fuzz_out.txt | tail -n 1; done > fuzz_results.txt
cat fuzz_results.txt
echo
echo "Total words tested across all processes:"
for i in {0..17}; do grep -oP "Process $i: tested \K[0-9]+" fuzz_results.txt; done | awk '{sum += $1} END {print sum}'
rm fuzz_results.txt

