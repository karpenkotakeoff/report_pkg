# Report tool

This tool takes a raw data of qualification F1, make report, and printing this report on the screen.

You must have that file structure
```
data
|--abbreviations.txt
|--start.log
'--end.log
```

abbreviations.txt
```
DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER
SVF_Sebastian Vettel_FERRARI
...
```
start.log
```
SVF2018-05-24_12:02:58.917
NHR2018-05-24_12:02:49.914
...
```
end.log
```
MES2018-05-24_12:05:58.778
RGH2018-05-24_12:06:27.441
...
```

#Quick start
After installing the package you can simply importing function ```main``` and invoke her
```
# example.py
from report_pkg import main

if __name__ == "__main__":
    main()
```
Now, you can use CLI with few parameters

Run this command from the same directory where ```example.py``` is located for a showing list of drivers and optional
order (default order is asc)
```
python example.py --files <folder_path> [--asc | --desc]
```
Output:
```
 1. Daniel Ricciardo    | RED BULL RACING TAG HEUER     | 1:12.013
 2. Sebastian Vettel    | FERRARI                       | 1:12.415
 3. Valtteri Bottas     | MERCEDES                      | 1:12.434
...
15. Nico Hulkenberg     | RENAULT                       | 1:13.065
--------------------------------------------------------------------
16. Brendon Hartley     | SCUDERIA TORO ROSSO HONDA     | 1:13.179
17. Marcus Ericsson     | SAUBER FERRARI                | 1:13.265
18. Lance Stroll        | WILLIAMS MERCEDES             | 1:13.323
19. Kevin Magnussen     | HAAS FERRARI                  | 1:13.393
```
You can show statistic about driver with:
```
python report.py --files <folder_path> driver “Sebastian Vettel”
```
Output:
```
2. Sebastian Vettel    | FERRARI                       | 1:12.415
```
