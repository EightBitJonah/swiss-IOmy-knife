# swiss-IOmy-knife

What does this do???

This script runs nmap to collect a list of live hosts. It then parses the targets out of that list, creates a file, and uploads the contents of that file to an existing scan in Tenable.io.

***More modules planned for the future

Requirements

python3

nmap

pytenable
  install pytenable with `pip install pytenable`
  
  No Windows support, use WSL2
