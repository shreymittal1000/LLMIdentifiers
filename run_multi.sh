
model_0=$1
model_1=$2
game=$3
spv="v1"

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
      python3 main.py "$model_0" "$model_1" "$game" "$spv" "v6.$perm"
      
      echo "Run #$i: $model_0 vs $model_1 -> $game with SPV: $spv and GPV: v4.$perm"
      python3 main.py "$model_0" "$model_1" "$game" "$spv" "v7.$perm"
      
      echo "Run #$i: $model_0 vs $model_1 -> $game with SPV: $spv and GPV: v5.$perm"
      python3 main.py "$model_0" "$model_1" "$game" "$spv" "v8.$perm"
    done
  done
else
  for i in {1..10}
  do
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v3"
    python3 main.py "$model_0" "$model_1" "$game" "$spv" "v6"
    
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v4"
    python3 main.py "$model_0" "$model_1" "$game" "$spv" "v7"
    
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v5"
    python3 main.py "$model_0" "$model_1" "$game" "$spv" "v8"
  done
fi
