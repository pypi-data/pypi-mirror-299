#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <storage_path> [options...]"
    exit 1
fi

trap "tput cnorm; exit" EXIT
tput civis

storage_path="$1"; shift
question_pfx="$1"; shift
answer_pfx="$1"; shift
selected_pfx="$1"; shift
options=("$@")
selected=0

print_menu() {
    for ((i=0; i<${#options[@]}; i++)); do
        if [[ $i -eq $selected ]]; then
            echo -e "${selected_pfx}${options[$i]}\033[0m"
        else
            echo -e "${answer_pfx}${options[$i]}\033[0m"
        fi
    done
    tput cuu ${#options[@]}
}

navigate_menu() {
    while true; do
        print_menu
        read -rsn1 input
        if [[ $input == $'\x1b' ]]; then
            read -rsn2 input
            case $input in
                '[A')
                    ((selected--))
                    if [[ $selected -lt 0 ]]; then
                        selected=$(( ${#options[@]} - 1 ))
                    fi
                    ;; 
                '[B')
                    ((selected++))
                    if [[ $selected -ge ${#options[@]} ]]; then
                        selected=0
                    fi
                    ;; 
            esac
        elif [[ $input == "" ]]; then
            tput cud $(( ${#options[@]} ))
            echo "$selected" > "$storage_path"
            break
        fi
    done
}

navigate_menu
tput cnorm