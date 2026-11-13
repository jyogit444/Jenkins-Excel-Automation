JENKINS + EXCEL ASSIGNMENT (Windows)
====================================
GOAL
Start with 100 employees in Master_Records_100.xlsx. Click "Build Now" in Jenkins.
10 unique employees from New_Records_10.xlsx are appended automatically.
The master ends with 110 employee rows. Running the build again keeps it at 110.

WHAT'S INCLUDED
Master_Records_100.xlsx - original master workbook, Records sheet has 100 rows
New_Records_10.xlsx    - incoming workbook, Records sheet has 10 rows
update_records.py       - update logic (deduplicates on Employee ID)
requirements.txt        - Python dependency
setup_python.bat        - one-time environment installation
run_jenkins_build.bat   - Jenkins job entry point
Jenkinsfile             - optional Pipeline job version

PREREQUISITES
1. Windows 10/11 and Python 3 installed (https://www.python.org/downloads/windows/)
2. JDK 21+ installed (https://adoptium.net/temurin/releases/)
3. Jenkins LTS MSI (https://www.jenkins.io/download/)

PART A - Prepare the assignment folder
1. Extract the ZIP on your computer.
2. Move this assignment's files directly into C:\JenkinsExcelDemo\ (no nested folder).
   Required: C:\JenkinsExcelDemo\Master_Records_100.xlsx and the other files.
3. Open Command Prompt (cmd.exe) and run:
      cd /d C:\JenkinsExcelDemo
      setup_python.bat
4. Keep the master Excel file CLOSED when Jenkins updates it.

PART B - Create the Jenkins job (easy Freestyle option)
1. In browser open http://localhost:8080 and sign in.
2. Click "New Item" and enter the name Excel-Record-Update.
3. Choose "Freestyle project" then click OK.
4. Scroll to Build Steps -> Add build step -> "Execute Windows batch command".
5. Paste this command:
      call "C:\JenkinsExcelDemo\run_jenkins_build.bat"
6. Click Save. Then click Build Now.
7. Open the build number -> Console Output, and check for success.
8. Open C:\JenkinsExcelDemo\Master_Records_100.xlsx and count the records.
   There will be 110 data rows (plus one header row).

PART C - Second build
1. Close the Excel file.
2. Hit Build Now again. It should say "New records: 0" and
   "Duplicates: 10 skipped". The master still has 110 records.
3. Add Employee IDs EMP0111 ... EMP0120 (10 new rows) to the
   Records sheet of New_Records_10.xlsx and save it. Close Excel.
4. Click Build Now again. It should say "New records: 10" and
   "After build: 120". Existing 10 incoming records will be skipped.

OPTIONAL PIPELINE JOB
Instead of Freestyle, choose "Pipeline" in New Item, paste the content of
Jenkinsfile into the Pipeline -> Script box, and click Save -> Build Now.

TROUBLESHOOTING
- The Python package is installed by setup_python.bat, not by Jenkins.
- If build says "Access denied", give the Windows user running the Jenkins
  service read/write access to C:\JenkinsExcelDemo and close the master workbook.
- Jenkins runs as a Windows service; that service account may be different from
  your Windows login. Check Services -> Jenkins -> Properties -> Log On.
- If a Pipeline build is queued, confirm Jenkins has an available Windows executor.
- Do not manually edit Employee ID values to duplicates. They are unique keys.
- Do not rename the Records sheet or the 5 column headers.
- The Excel file is updated on your computer at C:\JenkinsExcelDemo, not
  in Jenkins' web interface. Jenkins Console Output displays the result.

SCREENSHOTS TO SUBMIT
1. Jenkins dashboard/job configuration showing build command.
2. Master workbook before first build (100 rows).
3. New_Records_10.xlsx with 10 new rows.
4. Jenkins Console Output showing New records: 10 and After build: 110.
5. Master workbook after the build (110 rows).
6. Optional second-build log showing zero additions and 10 skipped duplicates.
