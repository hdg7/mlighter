cd "$(dirname "$0")"

# build the package
pip3 install --upgrade build
python3 -m build

# install the latest version from the dist folder
dist_files=$(ls dist)
sorted_builds=$(echo "$dist_files" | sort -V -r)
latest_build=$(echo "$sorted_builds" | head -n 1)

pip3 install dist/"$latest_build" --force-reinstall