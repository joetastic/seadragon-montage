cnt=0
echo $cnt;
for image_file in ../10000*.images; do
    echo $image_file; echo;
    cat $image_file |
    while read i
    do
        filename=$(echo $i | cut -d/ -f4-)
        if [ -r $filename ]; then
            continue
        else
            if [ -r $(basename $filename) ]; then
                [ -d $(dirname $filename) ] || mkdir -p $(dirname $filename)
                mv $(basename $filename) $filename
                continue
            fi
        fi
        [ -d $(dirname $filename) ] || mkdir -p $(dirname $filename)
        cnt=$(($cnt+1))
        echo -e '\033[1F\033[1G'$cnt
        curl -s -o $filename $i || (echo $filename; break)
        [ $(($cnt%50)) -eq 0 ] && sleep 1
        true
    done || break
    mv $image_file $image_file.done
done
