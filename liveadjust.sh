escape_char=$(printf "\u1b")

function alter {
	current=$(cat /mnt/offset)
	integer=$(echo $current|sed -e "s/\(\-*\)\([0-9]\)\.\([0-9]*\)/\1\2\3/" -e "s/\(^\-*\)0*/\1/" )
	echo "integer: $integer"
	if [[ $1 == "up" ]]
	then
		new=$(( $integer + 1))
	elif [[ $1 == "down" ]]
	then
		new=$(( $integer - 1))
	fi

	if [[ $new -lt 0 ]]
	then
		negative=$(( $new * -1))
		printf "-" >/mnt/offset
		printf "0.%02d" $negative >>/mnt/offset
	else
			printf "0.%02d" $new >/mnt/offset
	fi

	cat /mnt/offset
	echo
}

while read -rsn1 mode # get 1 character
do
if [[ $mode == $escape_char ]]; then
    read -rsn2 mode # read 2 more chars
fi
case $mode in
    'q') echo QUITTING ; exit ;;
    '[A') alter up ;;
    '[B') alter down ;;
    '[D') echo LEFT ;;
    '[C') echo RIGHT ;;
    *) >&2 echo 'ERR bad input'; return ;;
esac
done


