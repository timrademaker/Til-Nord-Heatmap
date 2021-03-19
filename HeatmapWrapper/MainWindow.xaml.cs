using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace HeatmapWrapper
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private static string LocationDataTabPrefix = "LocationData_V";
        private static string BumpDataTabPrefix = "BumpLocationData_V";

        private SpreadsheetHelper SsHelper = new SpreadsheetHelper();
        private int LatestVersion = 0;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void GenerateHeatmap_Click(object sender, RoutedEventArgs e)
        {
            // TODO: Run console command to run Python file
        }

        private void RefreshGameVersions_Click(object sender, RoutedEventArgs e)
        {
            HashSet<string> versionNames = GetGameVersionsFromSpreadsheets();

            // Sort versions descending
            IEnumerable<string> sortedVersions = versionNames.OrderByDescending(v => int.Parse(v));

            if(sortedVersions.Count() > 0)
            {
                LatestVersion = int.Parse(sortedVersions.First());
            }

            // Update game version ComboBox values
            cmbGameVersion.Items.Clear();

            cmbGameVersion.Items.Add("Latest");

            foreach(var ver in sortedVersions)
            {
                cmbGameVersion.Items.Add(ver);
            }

            cmbGameVersion.SelectedItem = "Latest";
        }

        private HashSet<string> GetGameVersionsFromSpreadsheets()
        {
            // TODO: Determine if development or release

            // Get tab names from Google Spreadsheets
            List<string> tabNames = SsHelper.GetTabNames("1ov0qAnzW4CXzwF1wSzVcvUVolx4om7j73NDyi-z7wdI");

            // Remove tab name prefixes
            for(int i = 0; i < tabNames.Count; ++i)
            {
                tabNames[i] = tabNames[i].Replace(BumpDataTabPrefix, "");
                tabNames[i] = tabNames[i].Replace(LocationDataTabPrefix, "");
            }

            return tabNames.ToHashSet();
        }
    }
}
