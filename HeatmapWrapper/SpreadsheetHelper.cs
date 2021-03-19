using Google.Apis.Auth.OAuth2;
using Google.Apis.Sheets.v4;
using Google.Apis.Sheets.v4.Data;
using Google.Apis.Services;
using Google.Apis.Util.Store;
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;

namespace HeatmapWrapper
{
    class SpreadsheetHelper
    {
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
    }
}
