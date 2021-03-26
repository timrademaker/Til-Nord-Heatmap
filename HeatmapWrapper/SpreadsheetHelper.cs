using Google.Apis.Auth.OAuth2;
using Google.Apis.Sheets.v4;
using Google.Apis.Sheets.v4.Data;
using Google.Apis.Services;
using Google.Apis.Util.Store;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading;

namespace HeatmapWrapper
{
    class SpreadsheetHelper
    {
        public static string CsvDelimiter = ";";

        private static string[] Scopes = { SheetsService.Scope.SpreadsheetsReadonly };
        private static string ApplicationName = "Til Nord Heatmap Wrapper";

        private SheetsService SpreadsheetService;

        public SpreadsheetHelper()
        {
            UserCredential credential;

            // Authenticate
            using(var stream = new FileStream("credentials.json", FileMode.Open, FileAccess.Read))
            {
                string credPath = "SpreadsheetToken";
                credential = GoogleWebAuthorizationBroker.AuthorizeAsync(
                    GoogleClientSecrets.Load(stream).Secrets,
                    Scopes,
                    "user",
                    CancellationToken.None,
                    new FileDataStore(credPath, true)).Result;
            }            

            // Create new Google Sheet API service
            SpreadsheetService = new SheetsService(new BaseClientService.Initializer()
            {
                HttpClientInitializer = credential,
                ApplicationName = ApplicationName
            });
        }

        public List<string> GetTabNames(string SheetID)
        {
            SpreadsheetsResource.GetRequest request = SpreadsheetService.Spreadsheets.Get(SheetID);
            Spreadsheet sheet = request.Execute();

            List<string> tabNames = new List<string>();

            foreach(Sheet sh in sheet.Sheets)
            {
                tabNames.Add(sh.Properties.Title);
            }

            return tabNames;
        }

        /**
         * Downloads the data from a spreadsheet tab in csv format
         * @param SheetID The ID of the spreadsheet to get data from
         * @param TabName The name of the tab to get data from
         * @param CellRange The cell range to get data from, in A1 or R1C1 notation. Example: "A1:C"
         * @param GameConfiguration The configuration of the game that 
         * @return The path to the spreadsheet data
         */
        public string GetSpreadsheetData(string SheetID, string TabName, string CellRange, string GameConfiguration)
        {
            Directory.CreateDirectory(GameConfiguration);

            string filePath = GameConfiguration + "/" + TabName + ".csv";

            string range = TabName + "!" + CellRange;

            SpreadsheetsResource.ValuesResource.GetRequest request = SpreadsheetService.Spreadsheets.Values.Get(SheetID, range);
            ValueRange response = request.Execute();

            // Write spreadsheet data to a file
            UTF8Encoding utf8 = new UTF8Encoding();
            byte[] newLineByte = utf8.GetBytes("\n");

            FileStream fs = File.Create(filePath);
            foreach(var val in response.Values)
            {
                for(var i = 0; i < val.Count; ++i)
                {
                    byte[] b = utf8.GetBytes(val[i] as string + CsvDelimiter);
                    fs.Write(b, 0, b.Length);
                }
                fs.Write(newLineByte, 0, newLineByte.Length);
            }

            fs.Close();

            return filePath;
        }
    }
}
