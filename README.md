# neu-mathe-am-testpage-parser

 An advanced mathematics exam answer getter for mathe.neu.edu.cn



## Usage

1. Import .SQL file into your MySql database.

2. Modify the database configuration in the code.

   ```python
   conn = connect(host="localhost", user="[USER]", passwd="[PASSWORD]", database="[DATABASE]")
   ```

3. Copy the source code of the exam page (by F12) to ```questions.html```.

4. Run this script and the answer will be output to the console like this:

   ```
   [INFO] 数据库中的答案
   总题量： 25
   ACACC
   ACDCB
   BCCBD
   ADABD
   CDDCC
   ```

5. If "the operation of this exam is abnormal n times" appears, run the following code in the browser console:

   ```javascript
   function monitor(){return;}
   ```

   
