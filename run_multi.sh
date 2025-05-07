
model_0=$1
model_1=$2

if [ -z "$model_0" ] || [ -z "$model_1" ]; then
  echo "Usage: $0 <model_0> <model_1>"
  exit 1
fi

for i in {1..100}
do
  echo "Run #$i: $model_0 vs $model_1"
  python3 main.py "$model_0" "$model_1"
done