using System.Windows;
using System.Windows.Forms;

namespace HeatmapWrapper
{
    /// <summary>
    /// Interaction logic for SettingsWindow.xaml
    /// </summary>
    public partial class SettingsWindow : Window
    {
        private OpenFileDialog BackgroundImageFileDialog;

        public SettingsWindow()
        {
            InitializeComponent();

            BackgroundImageFileDialog = new OpenFileDialog();
            BackgroundImageFileDialog.RestoreDirectory = true;
            BackgroundImageFileDialog.Title = "Select Heatmap Background Image";
            BackgroundImageFileDialog.Filter = "Image files (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg|All files (*.*)|*.*";
            BackgroundImageFileDialog.CheckPathExists = true;
            BackgroundImageFileDialog.CheckFileExists = true;
        }

        private void BackgroundImageButton_Click(object sender, RoutedEventArgs e)
        {
            // Open file browser and update text in block
            if(BackgroundImageFileDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                tbBackgroundImage.Text = BackgroundImageFileDialog.FileName;
            }
        }

        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            Properties.Settings.Default.Reload();
            Close();
        }

        private void ConfirmButton_Click(object sender, RoutedEventArgs e)
        {
            Properties.Settings.Default.Save();
            Close();
        }
    }
}
