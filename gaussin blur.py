import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel,QGraphicsPathItem, QPushButton, QVBoxLayout, QWidget, QAction, QMenuBar, QMessageBox, QHBoxLayout, QColorDialog, QGraphicsDropShadowEffect, QSlider,QGraphicsOpacityEffect
from PyQt5.QtCore import QSize, Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QImage, QPixmap, QIcon, QColor, QPainterPath



class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        
        self.image = None
        self.selected_image_path = ""
        self.image_selected = False
        self.selected_color = None  # Lưu màu sắc đã chọn

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Ứng dụng Xử Lý Ảnh")
        self.setWindowIcon(QIcon("icon.png"))
        self.image = cv2.imread  # Gán giá trị cho self.image
       

       
        

        menubar = self.menuBar()

        # Tạo menu "Tệp"
        file_menu = menubar.addMenu("Tệp")

        # Thêm mục "Mở ảnh" vào menu "Tệp"
        open_action = QAction("Mở Ảnh", self)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

        # Thêm mục "Chuyển đổi Định Dạng" vào menu "Tệp"
        convert_action = QAction("Chuyển đổi Định Dạng", self)
        convert_action.triggered.connect(self.convert_image_format)
        file_menu.addAction(convert_action)

        # Thêm mục "Thoát" vào menu "Tệp"6
        exit_action = QAction("Thoát", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Tạo menu "Trợ Giúp"
        help_menu = menubar.addMenu("Trợ Giúp")

        # Thêm các mục hướng dẫn vào menu "Trợ Giúp"
        self.add_section(help_menu, "Chọn ảnh", "Nhấn nút để chọn một ảnh để xử lý.", "Bấm nút này để chọn một ảnh từ máy tính của bạn và hiển thị lên ứng dụng.")
        self.add_section(help_menu, "Chuyển đổi Định Dạng", "Chuyển đổi định dạng ảnh và lưu.", "Bấm nút này để chuyển đổi định dạng ảnh và lưu lại ảnh đã xử lý.")
        self.add_section(help_menu, "Áp dụng Gaussian Blur", "Áp dụng Gaussian Blur lên ảnh.", "Bấm nút này để áp dụng hiệu ứng làm mờ Gaussian lên ảnh.")
        self.add_section(help_menu, "Áp dụng Median Blur", "Áp dụng Median Blur lên ảnh.", "Bấm nút này để áp dụng hiệu ứng làm mờ Median lên ảnh.")
        self.add_section(help_menu, "Áp dụng Bilateral Blur", "Áp dụng Bilateral Blur lên ảnh.", "Bấm nút này để áp dụng hiệu ứng làm mờ Bilateral lên ảnh.")
        self.add_section(help_menu, "Thay đổi kích thước ảnh", "Thay đổi kích thước ảnh.", "Bấm nút này để thay đổi kích thước của ảnh theo kích thước bạn mong muốn.")

        self.layout = QVBoxLayout()

        self.selected_image_label = QLabel(self)
        self.layout.addWidget(self.selected_image_label)

        self.image_preview_label = QLabel(self)
        self.layout.addWidget(self.image_preview_label)

        button_layout = QHBoxLayout()

        open_button = HoverButton("Chọn ảnh", self)
        open_button.setFixedSize(120, 50)
        open_button.setIcon(QIcon("open.png"))
        open_button.setIconSize(QSize(50, 50))
        open_button.clicked.connect(self.open_image)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        open_button.setGraphicsEffect(shadow)

        convert_button = HoverButton("Chuyển đổi Định Dạng", self)
        convert_button.clicked.connect(self.convert_image_format)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        convert_button.setGraphicsEffect(shadow)

        apply_button = HoverButton("Áp dụng và Lưu", self)
        apply_button.clicked.connect(self.confirm_and_apply_effects)
        apply_button.setFixedSize(120, 50)
        apply_button.setIcon(QIcon("save.png"))
        apply_button.setIconSize(QSize(50, 50))
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        apply_button.setGraphicsEffect(shadow)

        button_layout.addWidget(open_button)
        button_layout.addWidget(convert_button)
        button_layout.addWidget(apply_button)
        self.layout.addLayout(button_layout)

        # Thêm nút "Chọn Màu"
        color_picker_button = QPushButton("Chọn Màu", self)
        color_picker_button.clicked.connect(self.show_color_picker)
        self.layout.addWidget(color_picker_button)
    
        # Hiển thị màu đã chọn
        self.color_label = QLabel(self)
        self.layout.addWidget(self.color_label)

        self.status_label = QLabel(self)
        self.layout.addWidget(self.status_label)


   

    

        sliders_layout = QVBoxLayout()

        self.gaussian_slider = QSlider(self)
        self.gaussian_slider.setOrientation(Qt.Horizontal)
        self.gaussian_slider.setRange(1, 31)
        self.gaussian_slider.valueChanged.connect(self.update_gaussian_blur)


        
        # Áp dụng animation cho thanh slider này:
        start_value = self.gaussian_slider.value()  # Giá trị hiện tại của slider
        end_value = 1  # Giá trị mục tiêu cho slider
        animation = self.create_slider_animation(self.gaussian_slider, start_value, end_value)

        # Bắt đầu animation
        animation.start()


        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        self.gaussian_slider.setGraphicsEffect(shadow)

        gaussian_button = HoverButton("Gaussian Blur", self)
        gaussian_button.clicked.connect(self.apply_gaussian)

        self.median_slider = QSlider(self)
        self.median_slider.setOrientation(Qt.Horizontal)
        self.median_slider.setRange(1, 31)
        self.median_slider.valueChanged.connect(self.update_median_blur)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        self.median_slider.setGraphicsEffect(shadow)

        median_button = HoverButton("Median Blur", self)
        median_button.clicked.connect(self.apply_median)





   

        resize_button = HoverButton("Thay đổi kích thước ảnh", self)
        resize_button.clicked.connect(self.resize_image)

        sliders_layout.addWidget(self.gaussian_slider)
        sliders_layout.addWidget(gaussian_button)
        sliders_layout.addWidget(self.median_slider)
        sliders_layout.addWidget(median_button)
   

        sliders_layout.addWidget(resize_button)

        button_layout.addLayout(sliders_layout)

        main_widget = QWidget(self)
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)




        
    def resize_and_show_image(self, image):
        if image is not None:
            # Lấy kích thước của khung preview
            preview_width = self.image_preview_label.width()
            preview_height = self.image_preview_label.height()

        # Thay đổi kích thước ảnh để vừa với khung preview
            resized = cv2.resize(image, (preview_width, preview_height))
            self.show_image_preview(resized)
            

    def showEvent(self, event):
    # Khi cửa sổ chính được hiển thị, bạn sẽ tạo và bắt đầu animation ở đây.
        start_value = self.gaussian_slider.value()  # Giá trị hiện tại của slider
        end_value = 1  # Giá trị mục tiêu cho slider
        print("Start value:"), start_value
        print("End value"),end_value
        animation = self.create_slider_animation(self.gaussian_slider, start_value, end_value)
        animation.valueChanged.connect(lambda value: print("sd",value))
        animation.finished.connect(lambda: print("animtion finisish"))



        animation.start()
        QMainWindow.showEvent(self, event)

         # Bổ sung một hàm để tạo animation cho thanh trượt
    def create_slider_animation(self, slider, start_value, end_value):
        animation = QPropertyAnimation(slider, b"value")
        animation.setDuration(500)  # Thời gian animation (ms)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.setEasingCurve(QEasingCurve.Linear)  # Loại animation (có thể thay đổi)
        animation.valueChanged.connect(lambda value: print(value))
        return animation
    

        

    def show_color_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.color_label.setStyleSheet(f"background-color: {self.selected_color.name()};")
            self.status_label.setText(f"Màu đã chọn: {self.selected_color.name()}")

    def add_section(self, help_menu, title, description, help_text):
        help_action = QAction(title, self)
        help_action.triggered.connect(lambda checked, help_text=help_text: self.show_help_dialog(title, help_text))
        help_menu.addAction(help_action)

    def show_help_dialog(self, title, text):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec_()

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.selected_image_path, _ = QFileDialog.getOpenFileName(self, "Chọn Ảnh", "", "Image files (*.jpg *.jpeg *.png *.bmp *.gif *.tiff);;All Files (*)", options=options)

        if self.selected_image_path:
            self.selected_image_label.setText(f"Ảnh đã chọn: {self.selected_image_path}")
            self.image = cv2.imread(self.selected_image_path)
            
            if self.image is not None:
                self.image_selected = True
                self.enable_buttons()
                self.resize_and_show_image(self.image)  # Thực hiện resize và hiển thị ảnh
            else:
                self.status_label.setText("Không thể đọc được tệp tin ảnh. Vui lòng kiểm tra lại định dạng ảnh.")

    def enable_buttons(self):
        self.gaussian_slider.setEnabled(True)
        self.median_slider.setEnabled(True)


    def is_valid_kernel_size(self, ksize):
        return ksize % 2 == 1

    def convert_image_format(self):
        if self.image_selected:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            output_format, _ = QFileDialog.getSaveFileName(self, "Chuyển đổi và Lưu Ảnh", "", "JPEG files (*.jpg);;PNG files (*.png)", options=options)
            if output_format:
                cv2.imwrite(output_format, self.image)
                self.status_label.setText(f"Chuyển đổi ảnh thành công và lưu tại {output_format}")
        else:
            self.status_label.setText("Vui lòng chọn ảnh trước khi chuyển đổi định dạng.")

    def apply_gaussian(self):
        if self.image_selected:
            kernel_size = self.gaussian_slider.value()
            if self.is_valid_kernel_size(kernel_size):
                self.status_label.setText(f"Kích thước hiệu ứng Gaussian Blur: {kernel_size}")
                gaussian = cv2.GaussianBlur(self.image, (kernel_size, kernel_size), 0)
                self.show_image_preview(gaussian)
                return gaussian
            else:
                self.status_label.setText("Kích thước bộ lọc không hợp lệ. Kích thước phải là số lẻ và lớn hơn 0.")
                return None
        else:
            self.status_label.setText("Vui lòng chọn ảnh trước khi áp dụng phương pháp làm mờ Gaussian.")
            return None
    def apply_median(self):
        if self.image_selected:
            kernel_size = self.median_slider.value()
            if self.is_valid_kernel_size(kernel_size):
                self.status_label.setText(f"Kích thước hiệu ứng Median Blur: {kernel_size}")
                median = cv2.medianBlur(self.image, kernel_size)
                self.show_image_preview(median)
                return median 

            else:
                self.status_label.setText("Kích thước bộ lọc không hợp lệ. Kích thước phải là số lẻ và lớn hơn 0.")
                return self.image
        else:
            self.status_label.setText("Vui lòng chọn ảnh trước khi áp dụng phương pháp làm mờ Median.")
            return None


    def show_image_preview(self, image):
        if image is not None:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_preview_label.setPixmap(pixmap)

            

    def update_gaussian_blur(self):
        if self.image_selected:
            kernel_size = self.gaussian_slider.value()
            self.status_label.setText(f"Kích thước hiệu ứng Gaussian Blur: {kernel_size}")
            self.apply_gaussian()
        else:
            self.status_label.setText("Vui lòng chọn ảnh trước khi điều chỉnh kích thước Gaussian Blur.")

    def update_median_blur(self):
        if self.image_selected:
            kernel_size = self.median_slider.value()
            self.status_label.setText(f"Kích thước hiệu ứng Median Blur: {kernel_size}")
            self.apply_median()
        else:
            self.status_label.setText("Vui lòng chọn ảnh trước khi điều chỉnh kích thước Median Blur.")


    def resize_image(self):
        if self.image_selected:
            new_width = self.width_slider.value()
            new_height = self.height_slider.value()
            self.status_label.setText(f"Kích thước mới: {new_width}x{new_height}")
            resized = cv2.resize(self.image, (new_width, new_height))
            self.show_image_preview(resized)
        else:
            self.status_label.setText("Vui lòng chọn ảnh trước khi điều chỉnh kích thước.")

    def confirm_and_apply_effects(self):
        if self.image_selected:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            output_format, _ = QFileDialog.getSaveFileName(self, "Lưu Ảnh", "", "Image files (*.jpg *.jpeg *.png *.bmp *.gif *.tiff);;All Files (*)", options=options)
            if output_format:
                gaussian_processed_image = self.apply_gaussian()
                median_processed_image = self.apply_median()


                if gaussian_processed_image is not None:
                    cv2.imwrite(output_format, gaussian_processed_image)
                    self.image = gaussian_processed_image
                    self.status_label.setText(f"Ảnh đã xử lý (Gaussian Blur) và lưu tại {output_format}")

                if median_processed_image is not None:
                    cv2.imwrite(output_format, median_processed_image)
                    self.image = median_processed_image  
                    self.status_label.setText(f"Ảnh đã xử lý (Median Blur) và lưu tại {output_format}")
                else:
                    cv2.imwrite(output_format, self.image)
                    self.status_label.setText(f"Ảnh đã lưu tại {output_format}")

                
            self.status_label.setText(f"Ảnh đã xử lý và lưu tại {output_format}")
        else:
            self.status_label.setText("Vui lòng chọn ảnh trước khi xử lý và lưu.")

        

class HoverButton(QPushButton):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setStyleSheet("background-color: #59baff; color: white; border-radius: 10px;")
        #animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)  # Thời gian của hiệu ứng (miligiây)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)  # Loại hiệu ứng
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(self.geometry().adjusted(-5, -5, 5, 5))  # Dịch chuyển kích thước nút
        self.animation.start()

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: #e4e9f0; color: black; border-radius: 10px;")
        #animation
        if self.animation is not None:
            self.animation.setDirection(QPropertyAnimation.Backward)
            self.animation.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())