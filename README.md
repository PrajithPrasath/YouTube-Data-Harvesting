**YouTube-Data-Harvesting**
-YouTube Data Harvesting and Warehousing using jupyter notebook,VS Code,pymysql,MongoDB and Streamlit

**Overview**
-This project focuses on harvesting data from YouTube channels using the YouTube API, processing the data, and warehousing it. The harvested data is initially stored locally in a MongoDB database as documents and is then converted into SQL records for in-depth data analysis. The project's core functionality relies on the Extract, Transform, Load (ETL) process.

**Key Features**
-Harvest data from YouTube channels using the YouTube API.
-Store harvested data locally in a MongoDB database.
-Convert MongoDB documents into SQL records for further analysis.
-Perform Extract, Transform, Load (ETL) operations on the harvested data.
-Provide a user-friendly interface for data harvesting and migration using Streamlit.

**Getting Started**

**Ensure the necessary Python modules are installed:**
-pip install streamlit pandas pymongo pymysql google-api-python-client isodate

**Database Setup:**
-Ensure you have access to a local MongoDB instance and have set up a local mysql DBMS on your environment.

**Technical Steps to Execute the Project:**

**Step 1: Install/Import Modules**
-Ensure the required Python modules are installed: Streamlit, Pandas, PyMongo, Pymysql, Googleapiclient, and Isodate.

**Step 2: Utilize the "YT2SQL" Class**
-The project utilizes the "YT2SQL" class, which contains 11 methods, each with specific functionality for data extraction and transformation. These methods cover tasks like data retrieval, data storage, and data analysis.

**Step 3: Run the Project with Streamlit**
Open the command prompt in the directory where "Youtube.py" is located.
Execute the command:
streamlit run "Youtube.py"
This will open a web browser,Microsoft Edge, displaying the project's user interface.

**Step 4: Configure Databases**
Ensure that you are connected to both the local MongoDB instance and your local mysql DBMS.

**Methods:**
-1.Get YouTube Channel Data: Fetches YouTube channel data using a Channel ID and creates channel details in JSON format.
-2.Get Video and Comment Details: Returns video and comment details for the given video IDs.
-3.Get All Channel Details: Provides channel, video, and comment details in JSON format.
-4.Merge Channel Data: Combines channel details, video details, and comment details into a single JSON format.
-5.Insert Data into MongoDB: Inserts channel data into the local MongoDB as a document.
-6.Get Channel Names from MongoDB: Retrieves channel names from MongoDB documents.
-7.Convert MongoDB Document to Dataframe: Fetches MongoDB documents and converts them into dataframes for local SQL data insertion.
-8.Data Transformation for SQL: Performs data transformation for loading into local SQL.
-9.Data Load to SQL: Loads data into local SQL.
-10.Data Analysis: Conducts data analysis using SQL queries and Python integration.
-11.Manage MongoDB Documents: Manages MongoDB documents with various options.
-12.Delete SQL Records: Deletes local SQL records related to the provided YouTube channel data with various options.

**Skills Covered:**
-Python (Scripting)
-Data Collection
-MongoDB
-SQL
-API Integration
-Data Management using local MongoDB and local mysql
-IDE: jupyter notebook,VS Code
