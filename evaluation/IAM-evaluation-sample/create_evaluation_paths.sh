# Creates evaluation_paths file to be fed to wer.py
# the file it creates maps the reference files to the hypothesis files
ref_dir="./sample_gold_standards"
hyp_dir="./sample_output"
out_file="./evaluation_paths.ls"

while IFS='' read -r line ; do
    ref_path="$ref_dir/$line.gold.txt"
    hyp_path="$hyp_dir/$line.recognized.txt"

    printf "$ref_path\t$hyp_path\n" >> $out_file
done < sample_forms.ls
