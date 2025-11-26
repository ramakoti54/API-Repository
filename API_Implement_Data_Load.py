# Python Modules defined in the implementation process for Dataloading.
# Major python modules include, numpy, pandas, matplotlib, colab drive and auth, dotenv for loading environment variables to call microsoft sql server
# user and system DSN properties. Operating system to gather Environment variables for knowing the User details of the sql server database.
# Oracledb module uses tnsentry details for hostname and database user credentials and properties to pull database objects information to integration.
# Getpass is another module illustrates the authentication process through storing password encyrption method for connecting to database using username, password and connection string.

import numpy as np;
import pandas as pd;
import matplotlib as mtl;
#import SQLLite as sqt;
from google.colab import drive;
from google.colab import auth;
from dotenv import load_dotenv;
from os import getenv;
import mssql_python as msp;
from mssql_python import connect;
import oracledb;
import getpass;

# auth.authenticate_service_account()
# drive.mount("/Content/MyDrive/JPM.csv");
# clb.drive("");

# The major functionality of class API_Implement_Data_Load is to implement Data load process for loading both CSV and Datbase source ticker details to Dataframe.
# Class file is structured to define two distinct functions the Init mehtod is initiated during the creation of an Object to the class to create a consturctor functionality for assigning 
# information related to stock ticker file. Another area that init method concentrates on initiating empty list data types to create Data frame as well as to store Database Objects. SQL Connection string holds the information related to Driver
# connectivity to either SQL Server or Oracle Database objects. These objects has distinct connection strings defined as a concise formated structrual strings defined for each of these databases depends on type of the Driver used to connect.
# Implement_CSV_Data_Load method defined to explain about the DataFile properties for Stock Ticker on a given intraday. The Trading file holds the information rleated to Open, Close, High, Low, Adj Close and Volume.
# All of these prices incorporated into a list to store them and process through a Data frame for further transformations using Distributions and Standard Normalizations prior to using imputations and Feature engineering principles like PCA and other Normalization techniques.
# The second part of the API functionality demonstrates the usecase of both MSSQL Server and Oracle Databases. A conditional statement works to identify the connection string to be MSSQL Server and try to capture
# SQL Connection string information from its arguments and use it in finding the environment properties. A Connection object is introduced to store them and ran thorugh an other object called cursor for
# executing the SQL Query with selection of Database Object(Table/View). Output of SQL query stored in results through calling fetchall() method. The method loops all
# of the fields data to append at Database Object list as an item and returns the cursor result in the form of Database Object after closing the Cursor in the method.
# The same process followed while working on Oracle Database connectivity in the otherwise part of the conditional check for SQL Connection String. The Orclpdb works as an
# identifier for enabling the Oracle Database connectivity. In case of Oracle DB Connection establishment it tries to use username, connection string and password as user credentials to 
# connect to Oracle Database and the connection establishes through Connect mehtod of Oracledb module in python with username, password and datasourcename as connection string.
# Rest of the process remains as is in MSSQL Server DB to open a connection and work on the SQL Query execution to generate results of the Query to
# to represent the results through Database Object. One of the Database objects from the conditional statement of the method is returned to Init method for demonstrating the Data frame with 
# all stock ticker columns/attributes including Open, Close, High, Low, Adj Close and Volume.

class API_Implement_Data_Load:
   def Implement_CSV_Data_Load(self,Data_File,Data_Frame):
      Open_Price = Data_File['Open'];
      Close_Price = Data_File['Close'];
      High_Price = Data_File['High'];
      Low_Price = Data_File['Low'];
      Adj_Close = Data_File['Adj Close'];
      Volume = Data_File['Volume'];
      Data_Frame = [Open_Price,Close_Price,High_Price,Low_Price,Adj_Close,Volume];
      return(Data_Frame);

   def Implement_Database_Load(self,Database_Object,SQL_QUERY,SQL_CONNECTION_STRING):
      if("mssql" in SQL_CONNECTION_STRING):
         conn = connect(getenv("SQL_CONNECTION_STRING"));
         cursor = conn.cursor();
         cursor.execute(SQL_QUERY);
         results = cursor.fetchall();
         for i in results:
            print(f"{i.OPEN_PRICE}\t{i.CLOSE_PRICE}\t{i.HIGH_PRICE}\t{i.LOW_PRICE}\t{i.ADJUSTMENT_PRICE}\t{i.VOLUME}");
            Database_Object.append([i.OPEN_PRICE,i.CLOSE_PRICE,i.HIGH_PRICE,i.LOW_PRICE,i.ADJUSTMENT_PRICE,i.VOLUME]);
         cursor.close();
      elif("orclpdb" in SQL_CONNECTION_STRING):
         un = "Oracle DB Username";
         connection_string = SQL_CONNECTION_STRING;
         password = getpass.getpass(f"Enter Password for Oracle DB with Username {un}@{connection_string}:");
         con = oracledb.connect(user=un,password=password,dsn=connection_string);
         cursor = con.cursor();
         cursor.execute(SQL_QUERY);
         results = cursor.fetchall();
         for i in results:
            print(f"{i.OPEN_PRICE}\t{i.CLOSE_PRICE}\t{i.HIGH_PRICE}\t{i.LOW_PRICE}\t{i.ADJUSTMENT_PRICE}\t{i.VOLUME}");
            Database_Object.append([i.OPEN_PRICE,i.CLOSE_PRICE,i.HIGH_PRICE,i.LOW_PRICE,i.ADJUSTMENT_PRICE,i.VOLUME]);
         cursor.close();
      else:
         return(Database_Object);
      return(Database_Object);
      
   def __init__(self):
      CSV_File = pd.read_CSV("/content/Stocks_Data/JPM.csv");
      Data_Frame = [];
      Database_Object =[];
      SQL_QUERY = "SELECT OPEN as OPEN_PRICE, CLOSE as CLOSE_PRICE, HIGH as HIGH_PRICE, LOW as LOW_PRICE, 'ADJ CLOSE' as ADJUSTMENT_CLOSE FROM Financial_Money_Tree_DB.TICKER_NAME_LIVE_DATA as TN_LD WHERE TN_LD.LOW >= 0 and TN_LD.HIGH <= 0.50* TN_LD.LOW GROUP BY OPEN as OPEN_PRICE, CLOSE as CLOSE_PRICE, HIGH as HIGH_PRICE, LOW as LOW_PRICE, 'ADJ CLOSE' as ADJUSTMENT_CLOSE";
      SQL_CONNECTION_STRING = str(input("Enter SQL Connection String in the required format for either SQL Server or Oracle Database"));
      #"Server=<server_name>;Database={<database_name>};Encrypt=yes;TrustServerCertificate=no;Authentication=ActiveDirectoryInteractive";
      Data_File = self.Implement_CSV_Data_Load(CSV_File,Data_Frame);
      Database_Object = self.Implement_Database_Load(Database_Object,SQL_QUERY,SQL_CONNECTION_STRING);
      return(0);
     
Imp_CSV_Data_Load = API_Implement_Data_Load();
