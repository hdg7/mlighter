cd "$(dirname "$0")"

# build the package
python3 -m build

# install the latest version from the dist folder
dist_files=$(ls dist)
sorted_builds=$(echo "$dist_files" | sort -V -r)
latest_build=$(echo "$sorted_builds" | head -n 1)

pip3 install dist/"$latest_build"