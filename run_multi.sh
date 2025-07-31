
model_0=$1
model_1=$2
game=$3
num_rounds="5"
cues_or_cold="none"
multi="multi"

[[ ! ("$game" != "base" && "$cues_or_cold" == "cold") ]] && spv="v1" || spv="v2"

if [ -z "$model_0" ] || [ -z "$model_1" ] || [ -z "$game" ]; then
  echo "Usage: $0 <model_0> <model_1> <game>"
  exit 1
fi

if [ "$game" = "base" ]; then
  for i in {1..6}
  do
    for perm in {0..4}
    do
      echo "Run #$i: $model_0 vs $model_1 -> $game with SPV: $spv and GPV: v3.$perm, $cues_or_cold $multi"
      python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v3.$perm" "$cues_or_cold $multi"
      
      echo "Run #$i: $model_0 vs $model_1 -> $game with SPV: $spv and GPV: v4.$perm, $cues_or_cold $multi"
      python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v4.$perm" "$cues_or_cold $multi"
      
      echo "Run #$i: $model_0 vs $model_1 -> $game with SPV: $spv and GPV: v5.$perm, $cues_or_cold $multi"
      python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v5.$perm" "$cues_or_cold $multi"
    done
  done
elif [ "$game" = "ultimatumgame" ]; then
  for i in {1..10}
  do
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v1, $cues_or_cold $multi"
    python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v1" "$cues_or_cold $multi"
    
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v2, $cues_or_cold $multi"
    python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v2" "$cues_or_cold $multi"
    
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v3, $cues_or_cold $multi"
    python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v3" "$cues_or_cold $multi"
  done
else
  for i in {1..10}
  do
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v9 $cues_or_cold $multi"
    python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v9" "$cues_or_cold $multi"
    
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v10 $cues_or_cold $multi"
    python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v10" "$cues_or_cold $multi"
    
    echo "Run #$i: $model_0 vs $model_1 -> Game: $game with SPV: $spv and GPV: v11 $cues_or_cold $multi"
    python3 main.py "$model_0" "$model_1" "$game" "$num_rounds" "$spv" "v11" "$cues_or_cold $multi"
  done
fi
