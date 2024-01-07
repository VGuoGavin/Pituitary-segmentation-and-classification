import sys
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QWidget, \
    QFileDialog, QTabWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt
import pydicom
import re
from pathlib import Path
from difflib import SequenceMatcher
import os  # needed navigate the system to get the input data
import numpy as np

import SimpleITK as sitk

import nibabel as nib
import gzip
import shutil

class FileHandlerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Set up main window
        self.setWindowTitle('Beijing Tiantan Hospital tools')
        #self.setGeometry(100, 100, 600, 400)

        # Create tab widget for the sidebar
        self.sidebar_tab_widget = QTabWidget()
        self.page1_widget = QWidget()
        self.page2_widget = QWidget()
        self.sidebar_tab_widget.addTab(self.page1_widget, 'Page 1')
        self.sidebar_tab_widget.addTab(self.page2_widget, 'Page 2')

        # Create stacked widget for the main content
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setFixedSize(0, 0)
        # Add pages to the stacked widget
        self.init_ui_page1()
        self.init_ui_page2()

        # Set up central widget
        central_widget = QWidget(self)
        central_layout = QHBoxLayout(central_widget)
        central_layout.addWidget(self.sidebar_tab_widget)
        central_layout.addWidget(self.stacked_widget)

        # Set stretch factor for the stacked widget to make it take up all available space
        central_layout.setStretch(0, 0)

        self.setCentralWidget(central_widget)

        # Logo
        # logo_label = QLabel()
        # logo_pixmap = QPixmap("/Users/shipingguo/Downloads/Unknown-removebg-preview.png")  # Provide the path to your logo image
        # logo_label.setPixmap(logo_pixmap.scaledToWidth(150))  # Adjust the width as needed

        # Add logo to the top of the window
        # central_layout.addWidget(logo_label, alignment= Qt.AlignCenter)

        # Connect tab changes to show the corresponding page
        self.sidebar_tab_widget.currentChanged.connect(self.show_page)

    '''
    init_ui_page1
    Used for create nnUNet file
    '''
    def init_ui_page1(self):
        # Widgets for Page 1
        # Convert DICOM files to nii files
        function1_label = QLabel('DICOM to Nii format')
        function1_label.setAlignment(Qt.AlignCenter)

        # Convert nii to nii.gz files
        function2_label = QLabel('nii to nii.gz format')
        function2_label.setAlignment(Qt.AlignCenter)

        # Combine images with mask
        function3_label = QLabel('Combine Image and Mask (nii.gz format)')
        function3_label.setAlignment(Qt.AlignCenter)

        # Layout for Page 1

        layout = QVBoxLayout(self.page1_widget)

        # Horizontal layout for QLineEdit and QPushButton
        file_path_label = QLabel('Original MRI:')
        file_path_line_edit = QLineEdit()
        file_path_line_edit.setReadOnly(True)
        browse_button = QPushButton('Browse')
        read_button = QPushButton('Transform')
        line_edit_layout = QHBoxLayout()
        line_edit_layout.addWidget(file_path_label)
        line_edit_layout.addWidget(file_path_line_edit)
        line_edit_layout.addWidget(browse_button)
        line_edit_layout.addWidget(read_button)

        file_path_line_edit.setObjectName("file_path_line_edit1")

        # Adding the horizontal layout and other widgets to the main vertical layout
        layout.addWidget(function1_label)
        layout.addLayout(line_edit_layout)

        file_path_label2 = QLabel('Original MRI:')
        file_path_line_edit2 = QLineEdit()
        file_path_line_edit2.setReadOnly(True)
        browse_button2 = QPushButton('Browse')
        read_button2 = QPushButton('Transform')
        line_edit_layout2 = QHBoxLayout()
        line_edit_layout2.addWidget(file_path_label2)
        line_edit_layout2.addWidget(file_path_line_edit2)
        line_edit_layout2.addWidget(browse_button2)
        line_edit_layout2.addWidget(read_button2)
        file_path_line_edit2.setObjectName("file_path_line_edit2")


        layout.addWidget(function2_label)
        layout.addLayout(line_edit_layout2)

        file_path_label3 = QLabel('Original MRI:')
        file_path_line_edit3 = QLineEdit()
        file_path_line_edit3.setReadOnly(True)
        browse_button3 = QPushButton('Browse')
        read_button3 = QPushButton('Transform')
        read_button3.setDisabled(True)
        line_edit_layout3 = QHBoxLayout()
        line_edit_layout3.addWidget(file_path_label3)
        line_edit_layout3.addWidget(file_path_line_edit3)
        line_edit_layout3.addWidget(browse_button3)
        line_edit_layout3.addWidget(read_button3)
        file_path_line_edit3.setObjectName("file_path_line_edit3")

        file_path_label4 = QLabel('Target Mask:')
        file_path_line_edit4 = QLineEdit()
        file_path_line_edit4.setReadOnly(True)
        browse_button4 = QPushButton('Browse')
        read_button4 = QPushButton('Transform')
        line_edit_layout4 = QHBoxLayout()
        line_edit_layout4.addWidget(file_path_label4)
        line_edit_layout4.addWidget(file_path_line_edit4)
        line_edit_layout4.addWidget(browse_button4)
        line_edit_layout4.addWidget(read_button4)
        file_path_line_edit4.setObjectName("file_path_line_edit4")

        layout.addWidget(function3_label)
        layout.addLayout(line_edit_layout3)
        layout.addLayout(line_edit_layout4)

        log_display = QTextEdit()
        layout.addWidget(log_display)

        browse_button.clicked.connect(self.browse_folder1_1)
        browse_button2.clicked.connect(self.browse_folder1_2)
        browse_button3.clicked.connect(self.browse_folder1_3)
        browse_button4.clicked.connect(self.browse_folder1_4)

        read_button.clicked.connect(lambda:  self.transform1_1(log_display))
        read_button2.clicked.connect(lambda:  self.transform1_2(log_display))
        read_button4.clicked.connect(lambda:  self.transform1_3(log_display))

        # read_button.clicked.connect(lambda: self.read_file(file_path_line_edit.text(), log_display))

    def init_ui_page2(self):
        # Widgets for Page 2
        layout = QVBoxLayout(self.page2_widget)

        file_path_label1 = QLabel('Original image:')
        file_path_line_edit1 = QLineEdit()
        file_path_line_edit1.setReadOnly(True)
        browse_button1 = QPushButton('Browse')
        # Horizontal layout for QLineEdit and QPushButton
        line_edit_layout = QHBoxLayout()
        line_edit_layout.addWidget(file_path_label1)
        line_edit_layout.addWidget(file_path_line_edit1)
        line_edit_layout.addWidget(browse_button1)


        file_path_label2 = QLabel('Labling image:')
        file_path_line_edit2 = QLineEdit()
        file_path_line_edit2.setReadOnly(True)
        browse_button2 = QPushButton('Browse')
        line_edit_layout2 = QHBoxLayout()
        line_edit_layout2.addWidget(file_path_label2)
        line_edit_layout2.addWidget(file_path_line_edit2)
        line_edit_layout2.addWidget(browse_button2)

        file_path_label3 = QLabel('Output folder:')
        file_path_line_edit3 = QLineEdit()
        file_path_line_edit3.setReadOnly(True)
        browse_button3 = QPushButton('Browse')
        line_edit_layout3 = QHBoxLayout()
        line_edit_layout3.addWidget(file_path_label3)
        line_edit_layout3.addWidget(file_path_line_edit3)
        line_edit_layout3.addWidget(browse_button3)

        file_path_line_edit1.setObjectName("file_path_line_edit1")
        file_path_line_edit2.setObjectName("file_path_line_edit2")
        file_path_line_edit3.setObjectName("file_path_line_edit3")

        read_button = QPushButton('Transform')
        log_display = QTextEdit()
        # Adding the horizontal layout and other widgets to the main vertical layout
        layout.addLayout(line_edit_layout)
        layout.addLayout(line_edit_layout2)
        layout.addLayout(line_edit_layout3)
        layout.addWidget(read_button)
        layout.addWidget(log_display)

        browse_button1.clicked.connect(self.browse_folder2_1)
        browse_button2.clicked.connect(self.browse_folder2_2)
        browse_button3.clicked.connect(self.browse_folder2_3)
        read_button.clicked.connect(lambda: self.transform2(file_path_line_edit1.text(), file_path_line_edit2.text(), file_path_line_edit3.text(), log_display))

    def browse_folder1_1(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.page1_widget.findChild(QLineEdit, 'file_path_line_edit1').setText(folder_path)

    def convert_dicom_to_nifti( self, input_folder, output_folder, output_filename, log_display):
        # Read DICOM file
        dicom_reader = sitk.ImageSeriesReader()
        dicom_names = dicom_reader.GetGDCMSeriesFileNames(input_folder)
        dicom_reader.SetFileNames(dicom_names)
        dicom_image = dicom_reader.Execute()

        # extract DICOM
        dicom_info = pydicom.read_file(dicom_names[0])

        # change NIfTI formate
        nifti_image = sitk.GetImageFromArray(sitk.GetArrayFromImage(dicom_image))
        nifti_image.SetOrigin(dicom_image.GetOrigin())
        nifti_image.SetSpacing(dicom_image.GetSpacing())
        nifti_image.SetDirection(dicom_image.GetDirection())

        # save as nii.gz file
        output_path = os.path.join(output_folder, output_filename)
        sitk.WriteImage(nifti_image, output_path)
        log_display.append(f"Conversion completed. NIfTI file saved at: {output_path}")

    def transform1_1(self, log_display):
        # father file
        input_folder_path = self.page1_widget.findChild(QLineEdit, 'file_path_line_edit1').text()
        if input_folder_path != '':
            entries = os.listdir(input_folder_path)  # 获取路径下文件夹和文件名字
            # filter the folders
            subdirectories = [entry for entry in entries if os.path.isdir(os.path.join(input_folder_path, entry))]
            for i in range(len(subdirectories)):
                output_filename = 'Pituitarytumor' + '_' + str(i) + '_0000' + ".nii.gz"  # set the file name
                input_path = os.path.join(input_folder_path, subdirectories[i])  # save under father folder
                # transform
                self.convert_dicom_to_nifti(input_path, input_folder_path, output_filename, log_display)
            else:
                log_display.append(f'Error reading file: Its empty')

    def browse_folder1_2(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.page1_widget.findChild(QLineEdit, 'file_path_line_edit2').setText(folder_path)

    def create_folder_if_not_exists(self, folder_path):
        # Use Path to check the folder exist or not
        path = Path(folder_path)

        if not path.exists():
            # if not exist, creat a new one
            path.mkdir(parents=True, exist_ok=True)
            print(f"Folder '{folder_path}' created.")
        else:
            print(f"Folder '{folder_path}' already exists.")

    def convert_nii_gz_to_nii(self, input_path, output_path):
        with gzip.open(input_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    def transform1_2(self, log_display):
        Target_path = self.page1_widget.findChild(QLineEdit, 'file_path_line_edit2').text()
        #imagesTr_nii_gz = os.path.join(Target_path, 'imagesTr_nii_gz')
        #labelsTr_nii_gz = os.path.join(Target_path, 'labelsTr_nii_gz')
        images_list = [f for f in os.listdir(Target_path) if os.path.isfile(os.path.join(Target_path, f))]
        #masks_list = [f for f in os.listdir(labelsTr_nii_gz) if os.path.isfile(os.path.join(labelsTr_nii_gz, f))]

        images_list_nii = [file_name for file_name in images_list if file_name.endswith(".nii")]
        #masks_list_nii = [file_name for file_name in masks_list if file_name.endswith(".nii")]

        # Using list comprehension to filter out items not ending with ".nii.gz"
        images_list = [file_name for file_name in images_list if file_name.endswith(".nii.gz")]
        #masks_list = [file_name for file_name in masks_list if file_name.endswith(".nii.gz")]
        images_list = sorted(images_list, reverse=False)
        #masks_list = sorted(masks_list, reverse=False)

        imagesTr_nii = os.path.join(Target_path, 'images_nii')
        #labelsTr_nii = os.path.join(Target_path, 'labelsTr_nii')
        self.create_folder_if_not_exists(imagesTr_nii)
        #self.create_folder_if_not_exists(labelsTr_nii)
        for patient in images_list:
            input_file = os.path.join(Target_path, patient)
            output_file_name = patient.split('.')[0] + '.nii'
            output_file = os.path.join(imagesTr_nii, output_file_name)
            files_in_directory = os.listdir(Target_path)

            if output_file_name not in files_in_directory:
                self.convert_nii_gz_to_nii(input_file, output_file)
        log_display.append('nii files:' + imagesTr_nii)
    def browse_folder1_3(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.page1_widget.findChild(QLineEdit, 'file_path_line_edit3').setText(folder_path)

    def browse_folder1_4(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.page1_widget.findChild(QLineEdit, 'file_path_line_edit4').setText(folder_path)

    def binarize_mask(self, mask_data):
        # 将mask数据二值化，使所有非零值变为1
        return np.where(mask_data > 0, 1, 0)

    def merge_nifti_files(self, original_file_path, mask_file_path, output_file_path):
        images_list = [f for f in os.listdir(original_file_path) if os.path.isfile(os.path.join(original_file_path, f))]
        images_list_filtered = [file_name for file_name in images_list if file_name.endswith(".nii.gz")]

        mask_list = [f for f in os.listdir(mask_file_path) if os.path.isfile(os.path.join(mask_file_path, f))]
        mask_list_filtered = [file_name for file_name in mask_list if file_name.endswith(".nii.gz")]
        # 这里需要重排序，验证等
        images_list_filtered = sorted(images_list_filtered, key=lambda s: int(re.search(r'\d+', s).group()) if re.search(r'\d+', s) else 0)
        mask_list_filtered = sorted(mask_list_filtered, key=lambda s: int(re.search(r'\d+', s).group()) if re.search(r'\d+', s) else 0)
        for i in range(len(images_list_filtered)):
            # 读取原始文件和mask文件
            image_file_path = os.path.join(original_file_path, images_list_filtered[i])
            original_image = nib.load(image_file_path)

            mask_path = os.path.join(mask_file_path, mask_list_filtered[i])
            mask_image = nib.load(mask_path)

            # 获取原始数据和mask数据
            original_data = original_image.get_fdata()
            mask_data = mask_image.get_fdata()

            # 二值化mask数据
            binarized_mask_data = self.binarize_mask(mask_data)
            # 将二值化后的mask应用于原始数据
            merged_data = original_data - 150 * binarized_mask_data  # 将两个文件叠加在一起
            # 创建一个新的NIfTI文件对象
            merged_image = nib.Nifti1Image(merged_data, original_image.affine)
            # 保存合并后的NIfTI文件
            combined_file_path = os.path.join(output_file_path, images_list_filtered[i])
            nib.save(merged_image, combined_file_path)
    def transform1_3(self, log_display):
        # Combine two files
        original_file_path = self.page1_widget.findChild(QLineEdit, 'file_path_line_edit3').text()
        mask_file_path = self.page1_widget.findChild(QLineEdit, 'file_path_line_edit4').text()

        combined_file_path = os.path.join(os.path.dirname(original_file_path), 'combined')
        self.create_folder_if_not_exists(combined_file_path)
        self.merge_nifti_files(original_file_path, mask_file_path, combined_file_path)
        log_display.append("conbined file: "+combined_file_path)

    def browse_folder2_1(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.page2_widget.findChild(QLineEdit, 'file_path_line_edit1').setText(folder_path)

    def browse_folder2_2(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.page2_widget.findChild(QLineEdit, 'file_path_line_edit2').setText(folder_path)

    def browse_folder2_3(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.page2_widget.findChild(QLineEdit, 'file_path_line_edit3').setText(folder_path)

    def check_binary_nifti(self, file_path):
        # read .nii.gz file
        img = nib.load(file_path)
        # read array file
        data = img.get_fdata()
        # check the value only contain 0 and 1
        is_binary = np.all(np.logical_or(data == 0, data == 1))
        return is_binary
    def compare_nifti_dimensions(self, file1_path, file2_path):
        # Read.nii.gz file
        img1 = nib.load(file1_path)
        img2 = nib.load(file2_path)
        header1 = img1.header
        header2 = img2.header
        # The size
        shape1 = header1.get_data_shape()
        shape2 = header2.get_data_shape()
        # read the slice info
        spacing1 = header1.get_zooms()
        spacing2 = header2.get_zooms()
        # check the size
        if shape1 != shape2:
            return False, "尺寸不同"
        # check the distance between slice
        if not np.allclose(spacing1, spacing2):
            return False, "切片间隔不同"
        return True, "两个文件相同"
    def transform2(self, file_path, file_path2, file_path3, log_display):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                log_display.append(f'Read from {file_path}:\n{content}')
        except FileNotFoundError:
            log_display.append(f'File not found: {file_path}')
        except Exception as e:
            log_display.append(f'Error reading file: {e}')

        try:
            with open(file_path2, 'r') as file:
                content = file.read()
                log_display.append(f'Read from {file_path2}:\n{content}')
        except FileNotFoundError:
            log_display.append(f'File not found: {file_path2}')
        except Exception as e:
            log_display.append(f'Error reading file: {e}')

        self.create_folder_if_not_exists(file_path3)

        folder1 = file_path
        folder2 = file_path2

        file_Tr = [f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))]
        file_La = [f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))]
        file_Tr = sorted(file_Tr)
        file_La = sorted(file_La)
        N = 0
        if len(file_La) == len(file_Tr):
            N = len(file_La)
        else:
            log_display.append('The length of training and lables are different')
        print(N)

        imagesTr = os.path.join(file_path3, 'imagesTr')
        labelsTr = os.path.join(file_path3, 'labelsTr')

        self.create_folder_if_not_exists(imagesTr)
        self.create_folder_if_not_exists(labelsTr)

        similarity_ratio = []
        # 这里定义三个list，分别对应original image name list，筛选过的image name list和label list，为了保证修改名字前后对应起来！！！
        PRE_IMAGE_LIST = []
        PRE_LABEL_LIST = []
        IMAGE_LIST = []
        LABEL_LIST = []
        IMAGE_LIST_NII = []
        LABEL_LIST_NII = []
        for i in range(N):
            similarity_ratio.append(SequenceMatcher(None, file_Tr[i], file_La[i]).ratio())
            if file_Tr[i][-7:] == '.nii.gz' and file_La[i][-7:] == '.nii.gz':
                image = os.path.join(folder1, file_Tr[i])
                mask = os.path.join(folder2, file_La[i])
                result, message = self.compare_nifti_dimensions(image, mask)
                if result:
                    if not self.check_binary_nifti(mask):
                        log_display.append('Error 1: ' + file_Tr[i] + "该标注不只包含0和1值" + ' Pituitarytumor' + '_' + str(
                            i) + '_0000 will be missing')
                    else:
                        PRE_IMAGE_LIST.append(file_Tr[i])
                        PRE_LABEL_LIST.append(file_La[i])
                        if similarity_ratio[i] > 0.8:  # 这里模糊匹配一下,这里不严谨，有可能会遗漏
                            name_Tr = 'Pituitarytumor' + '_' + str(i) + '_0000' + file_Tr[i][-7:]
                            IMAGE_LIST.append(name_Tr)
                            IMAGE_LIST_NII.append('Pituitarytumor' + '_' + str(i) + '_0000' + '.nii')
                            name_La = 'Pituitarytumor' + '_' + str(i) + file_Tr[i][-7:]
                            LABEL_LIST.append(name_La)
                            LABEL_LIST_NII.append('Pituitarytumor' + '_' + str(i) + '.nii')

                            shutil.copy(os.path.join(folder1, file_Tr[i]), os.path.join(imagesTr, name_Tr))
                            shutil.copy(os.path.join(folder2, file_La[i]), os.path.join(labelsTr, name_La))
                        else:
                            log_display.append('Error 3: ' + "Please check the files " + file_Tr[i] + ' and ' + file_La[
                                i] + ' match or not?')
                else:
                    log_display.append('Error 2: ' + file_Tr[i] + ' ' + message + ' Pituitarytumor' + '_' + str(
                        i) + '_0000 will be missing')
            else:
                log_display.append('Error 0: ' + file_Tr[i][-7:] + ' or ' + file_La[i][-7:] + " fomate is wrong!")
        log_display.append("Result: " + file_path3)

    def show_page(self, index):
        # Change the current page of the stacked widget based on the selected tab
        self.stacked_widget.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_handler_app = FileHandlerApp()
    file_handler_app.show()
    sys.exit(app.exec_())
