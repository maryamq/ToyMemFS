
# Release Log
## Core Features
1. Change Working dir (cd)
2. Get working dir (pwd)
3. Create new dir (mk)
4. Get Dir content (ls)
5. Remove Dir (rm)
6. Create new file (mk)
7. Get File content (cat)
8. Move file or dir (mv)
9. Search for file

## Extensions:
1. Virtual Drives: Create new drives, mount drives, list (new)
2. Operations on path: absolute and relative. hello, /hello, ../hello are all valid
3. Walk a subtree: Print entire drive, dir subtree, recursive search with regex
4. Load a mem drive by executing commands from file on disk (new)
5. Append to a file instead of overwrite.
6. Remove a File or dir.



----
Draft Notes.

## Initial Design:
Base filesystem:
- Be able to create multiple filesystem -> Specify a name and ("maryam://") -> Decorator registration should make it easier
	- Like virtual env
- File Structure: AbstractBase for all File system objects: Dirs and FIles. This could be lazy load internet file
	- SymLinks
	- Use Iterator Protocol (will simply code later on. )
- Path Management (This will get messy - allocate time for testing)
	- Use SimplePath for python.
	- Handle Absolute and Relative Path
	- Handle ...: Will Require Child to know their parent
- Search:
	- TODO: 
	- Direct and recursive: 
- Print Whole Filesystem structure:
	- Not required but useful for testing.
	- Also add a test filesystem (preloaded  for testing)
* Command Line Parsing: 
	* TODO: Come up with a the format first. 
* Error Handling
	* TODO


AIs:
1.  Build a command line prompt: Input command and parses correctly.
	1. Help Command: 
2. Create a filesystem + Switch Filesystem: Decorator registration is working correctly.
3. Path: Helper functions to create paths , pwd, resolve paths
4. Make Directories + switch Paths: (Big)
	1. mkdir, ls , cd
	2. Handle pwd
5. Make Directories 2: Force create new (Ext but will make testing easier)
6. Delete Dir
7. Print Whole Disk (Ext but will make debugging easier)
8. Create File + Delete File.
9. Write to File + Implement cat


Extension:
10. Move Directories: 
	1. Check references
11. Copy :
	1. Implement copy protocol correctly. 
	2. Copy + Merge: Use id(object) to resolve merges
13. Symlink:
	1. Soft: Easy: New File type
	2. Hard: 
		1. Impl Option 1: Keep a table separately for all symlinks
		2. File Object manages its own symlinks. On Delete: It should notify HardSymlink:
			1. Some complexity here : Symlink can be deleted without deleting the original file. Communication must be bi-directional. 
			2. Should hard links be deleted if the file itself is deleted
			

