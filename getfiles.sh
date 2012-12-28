cnt=0
for image_file in 10000b*.images; do
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
        curl -s -o $filename $i; echo $i
        [ $(($cnt%50)) -eq 0 ] && sleep 1
    done
done
