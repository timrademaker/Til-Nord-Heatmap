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
        private static String locationDataTabPrefix = "LocationData_V";
        private static String bumpDataTabPrefix = "BumpLocationData_V";

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
            HashSet<String> versionNames = GetGameVersionsFromSpreadsheets();
            // TODO: Sort from high to low?

            // Update game version ComboBox values
            cmbGameVersion.Items.Clear();

            cmbGameVersion.Items.Add("Latest");

            foreach(var ver in versionNames)
            {
                cmbGameVersion.Items.Add(ver);
            }

            cmbGameVersion.SelectedItem = "Latest";

        }

        private HashSet<String> GetGameVersionsFromSpreadsheets()
        {
            // TODO: Determine if development or release

            // TODO: Get tab names from Google Spreadsheets
            List<String> tabNames = new List<String>();

            // Remove tab name prefixes
            for(int i = 0; i < tabNames.Count; ++i)
            {
                tabNames[i] = tabNames[i].Replace(locationDataTabPrefix, "");
                tabNames[i] = tabNames[i].Replace(bumpDataTabPrefix, "");
            }

            return tabNames.ToHashSet();
        }
    }
}
