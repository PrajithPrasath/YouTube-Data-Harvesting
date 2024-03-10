**YouTube-Data-Harvesting**<br>
YouTube Data Harvesting and Warehousing using jupyter notebook,VS Code,pymysql,MongoDB and Streamlit

**Overview**<br>
This project focuses on harvesting data from YouTube channels using the YouTube API, processing the data, and warehousing it. The harvested data is initially stored locally in a MongoDB database as documents and is then converted into SQL records for in-depth data analysis. The project's core functionality relies on the Extract, Transform, Load (ETL) process.

**Key Features**<br>
-Harvest data from YouTube channels using the YouTube API.<br>
-Store harvested data locally in a MongoDB database.<br>
-Convert MongoDB documents into SQL records for further analysis.<br>
-Perform Extract, Transform, Load (ETL) operations on the harvested data.<br>
-Provide a user-friendly interface for data harvesting and migration using Streamlit.<br>

**Getting Started**<br>
**Ensure the necessary Python modules are installed:**<br>
pip install streamlit pandas pymongo pymysql google-api-python-client isodate
**Database Setup:**<br>
Ensure you have access to a local MongoDB instance and have set up a local mysql DBMS on your environment.

**Technical Steps to Execute the Project:**
**Step 1: Install/Import Modules**<br>
Ensure the required Python modules are installed: Streamlit, Pandas, PyMongo, Pymysql, Googleapiclient, and Isodate.<br>
**Step 2: Utilize the "YT2SQL" Class**<br>
The project utilizes the "YT2SQL" class, which contains 11 methods, each with specific functionality for data extraction and transformation. These methods cover tasks like data retrieval, data storage, and data analysis.<br>
**Step 3: Run the Project with Streamlit**<br>
Open the command prompt in the directory where "Youtube.py" is located.<br>
Execute the command:streamlit run "Youtube.py"<br>
This will open a web browser,Microsoft Edge, displaying the project's user interface.<br>
**Step 4: Configure Databases**<br>
Ensure that you are connected to both the local MongoDB instance and your local mysql DBMS.

**Methods:**<br>
1.Get YouTube Channel Data: Fetches YouTube channel data using a Channel ID and creates channel details in JSON format.<br>
2.Get Video and Comment Details: Returns video and comment details for the given video IDs.<br>
3.Get All Channel Details: Provides channel, video, and comment details in JSON format.<br>
4.Merge Channel Data: Combines channel details, video details, and comment details into a single JSON format.<br>
5.Insert Data into MongoDB: Inserts channel data into the local MongoDB as a document.<br>
6.Get Channel Names from MongoDB: Retrieves channel names from MongoDB documents.<br>
7.Convert MongoDB Document to Dataframe: Fetches MongoDB documents and converts them into dataframes for local SQL data insertion.<br>
8.Data Transformation for SQL: Performs data transformation for loading into local SQL.<br>
9.Data Load to SQL: Loads data into local SQL.<br>
10.Data Analysis: Conducts data analysis using SQL queries and Python integration.<br>
11.Manage MongoDB Documents: Manages MongoDB documents with various options.<br>
12.Delete SQL Records: Deletes local SQL records related to the provided YouTube channel data with various options.<br>

**Skills Covered:**
-Python (Scripting) <br>
-Data Collection <br>
-MongoDB <br>
-SQL <br>
-API Integration <br>
-Data Management using local MongoDB and local mysql <br>
-IDE: jupyter notebook,VS Code <br>
