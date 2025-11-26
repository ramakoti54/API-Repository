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

#auth.authenticate_service_account()
#drive.mount("/Content/MyDrive/JPM.csv");
#clb.drive("");

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


