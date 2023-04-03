# ToyMemFS
A library to create a simple in-memory filesystem in python with a command line interface.


## FeatureList
### Core Features
1. Change Working dir (cd)
2. Get working dir (pwd)
3. Create new dir (mk)
4. Get Dir content (ls)
5. Remove Dir (rm)
6. Create new file (mk)
7. Get File content (cat)
8. Move file or dir (mv)
9. Search for file or dir (regex - recursive)

## #Additional :
1. Virtual Drives: Create new drives, mount drives, list (new)
2. Operations on path: absolute and relative. hello, /hello, ../hello are all valid
3. Walk a subtree: Print entire drive, dir subtree, recursive search with regex
4. Load a mem drive by executing commands from file on disk (new)
5. Append to a file instead of overwrite.
6. Remove a File or dir.
## Setup:
```
python3 ToyMemFS/main.py
```

Tip: The setup steps can be executed directly from files.
```
python3 ToyMemFS/main.py
load test/step1.txt
load test/step2.txt
load test/step3.txt
load test/step4.txt
load test/step5.txt
load test/step6.txt
load test/step7.txt
load test/step8.txt
```

### Setup a virtual drive  and load test data (1)
Virtual drives are similar to physical hard drives. You can create and switch among multiple virtual drives.
The input prompt will specify the active virtual drive. A 'default' drive is created at startup. 

- create a new virtual drive "test" and mount it. 
- List all available virtual drives
- Lets populate the 'test' drive with some files and directories.
- View a snapshot of the entire virtual drive.
```
drives
new test
mount test
drives
load test/test_config.txt
sys
```

### Navigation (2)
We can use relative and absolute paths. 
- Navigate to a sub directory
- Check the present working directory
- Lists content of a directory.
```
cd /movies/paramount
pwd
cd ../..
pwd
cd /movies
pwd
ls
ls disney

```

### Create Directories and Files (3)
- Files without extensions are treated as directories.
- Use .txt extension of text files (only supported file format)
```
echo Creating directories.
cd /movies
mk mgm
mk mgm/rocky
cd mgm/
ls
echo Creating some text files
cd /movies
mk my_fav_movies.txt
mk bad_movies.txt
mk finding_nemo
mk finding_nemo/nemo.txt
mk ../root_file.txt
mk mgm/rocky/rocky_1976.txt
ls

```


### Write,  append and view text file (4)
```
cd /
write movies/my_fav_movies.txt matrix
write append movies/my_fav_movies.txt finding nemo
cat movies/my_fav_movies.txt
cd movies
write finding_nemo/nemo.txt we found nemo
cat finding_nemo/nemo.txt

```

### Play with regex search (5)
- Search is recursive. 
```
echo ********** Step 5: Search for directories and files 
cd /
find . rocky
cd /movies/mgm/rocky
find . rocky
cd /
find . mov
echo Find all txt files in the system
find / .*\.txt$

```


### Move  Files and directories (6)
- Directories and files can be moved. Name collision resolution is not supported.
- Root directory cannot be moved.
```

echo ********** Step 6: Move Files and directories
sys
echo "Move directory"
cd /movies
ls
mv finding_nemo disney
ls 
ls disney
cat disney/finding_nemo/nemo.txt
cd disney/finding_nemo
pwd
echo ******* Move tv_show.txt ****
cd /movies/disney
cat tv_show.txt
mv tv_show.txt ../../tv
cd /tv
ls
cat tv_show.txt
sys

```


### Delete Files and Directories (7)
- Delete files and empty directories.
- Root directory cannot be deleted.
```
echo ********** Step 7: Delete files and directories
sys
cd /
ls 
echo "Deleting a non-empty directory should fail"
rm tv
echo "Delete files in /tv and try again"
ls tv
rm tv/tv_show.txt
ls tv
rm tv
ls
echo "Deleting root dir should fail"
rm /
sys
```

### Error Handling and wrap up (8)
- Type exit to quit.
```
echo ********** Step 8: Error Handling and wrap up
sys
cd ../../../../
pwd
cd missing_dir
mk /movies
mk /movies/disney/finding_nemo/nemo.txt
echo Create unsupported files
mk temp.jpg
echo mount the default drive.
drives
mount default
sys

```
