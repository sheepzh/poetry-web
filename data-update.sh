if [ "$1" ];then
  rm data -rf
  cp $1 -r data
  rm data/**/*.sh -r
  rm data/**/*.md -r
else 
  echo "No origin data"
fi