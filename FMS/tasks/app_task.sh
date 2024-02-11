#!/bin/bash
# This script would create a folder for your django project, create a virtual environment, install the given packages/dependencies, prompt you for a project name and app name(s), and then create them

counter=0

read -p "Enter the project name for $PWD: " project_name
echo "$project_name created successfully!"

echo "Application names (leave a space after each name): "

read -a app_names

for app in "${app_names[@]}"; do
    if [ "${#app_names[@]}" -gt "$counter" ]; then
        counter=$((counter + 1))
        echo "Application $counter: $app"
    fi
done

object(){
    
}