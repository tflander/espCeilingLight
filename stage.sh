export AMPY_PORT=/dev/cu.SLAB_USBtoUART
ampy ls

for python_folder in "web_control" "parsers"
do
  echo $python_folder
  if ! ampy ls | grep ${python_folder} &> /dev/null; then
    echo "making folder ${python_folder}"
  ampy mkdir ${python_folder}
  else
    echo "folder ${python_folder} exists"
  fi
done

for python_folder in "" "web_control/" "parsers/"
do
  for file in ${python_folder}*.py
  do
    echo "updating ${file}..."
    ampy put ${file} ${file}
  done
done

echo "resetting..."
ampy reset
echo "done."
