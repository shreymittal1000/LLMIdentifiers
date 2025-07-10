
model_0=$1
model_1=$2
game=$3
num_rounds="5"
spv="v1"
cues_or_cold="cold"

if [ -z "$model_0" ] || [ -z "$model_1" ] || [ -z "$game" ]; then
  echo "Usage: $0 <model_0> <model_1> <game>"
  exit 1
fi

if [ "$game" = "base" ]; then
  for i in {1..6}
  do
    for perm in {0..4}
    do
      echo "Run #$i: $model_0 vs $model_1 -> $game with SPV: $spv and GPV: v3.$perm"
      python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v3.$perm" "$cues_or_cold"
      
      echo "Run #$i: $model_0 vs $model_1 -> $game with SPV: $spv and GPV: v4.$perm"
      python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v4.$perm" "$cues_or_cold"
      
      echo "Run #$i: $model_0 vs $model_1 -> $game with SPV: $spv and GPV: v5.$perm"
      python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v5.$perm" "$cues_or_cold"
    done
  done
else
  for i in {1..10}
  do
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v6"
    python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v6" "$cues_or_cold"
    
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v7"
    python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v7" "$cues_or_cold"
    
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v8"
    python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v8" "$cues_or_cold"
  done
fi
