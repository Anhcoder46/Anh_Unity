🏠 BÀI TẬP LỚN: THU THẬP DỮ LIỆU BẤT ĐỘNG SẢN TẠI TP HỒ CHÍ MINH
📝 Mô tả
Bat_Dong_San.py là script Python tự động thu thập dữ liệu bất động sản loại "Bất động sản khác" tại Thành phố Hồ Chí Minh từ website homedy.com. Dữ liệu được thu thập bao gồm:
    Tiêu đề tin đăng
    Mô tả chi tiết
    Giá bán/cho thuê
    Diện tích
    Địa chỉ
    Link chi tiết
    Dữ liệu sau khi thu thập sẽ được lưu vào file Excel Bat_Dong_San_Khac_TP_HCM.xlsx.

⚙️ Yêu cầu môi trường
    Python: Phiên bản 3.7 trở lên
    Trình duyệt: Google Chrome (phiên bản mới nhất)
    ChromeDriver: Phiên bản tương thích với Chrome
    Thư viện Python:
        selenium
        pandas
        schedule
        openpyxl
Cài đặt các thư viện cần thiết:
    pip install selenium pandas schedule openpyxl

🚀 Hướng dẫn sử dụng
1. Cài đặt ChromeDriver
Kiểm tra phiên bản Chrome của bạn (vào chrome://settings/help)
Tải ChromeDriver tương ứng từ trang chủ
Đặt file chromedriver.exe vào thư mục project hoặc thêm vào PATH hệ thống

2. Chạy script
    python Bat_Dong_San.py

3. Quy trình hoạt động
Script sẽ tự động:
Mở trình duyệt Chrome và truy cập homedy.com
Chọn:
    Địa điểm: TP Hồ Chí Minh
    Loại bất động sản: "Bất động sản khác"
    Thu thập dữ liệu từ tất cả các trang có sẵn
    Lưu dữ liệu vào file Excel tại đường dẫn: D:\Tu_dong_hoa_python\Bai_tap_lon\Bat_Dong_San_Khac_TP_HCM.xlsx

4. Lập lịch tự động
Script được cài đặt chạy tự động vào 6h sáng hàng ngày. Có thể thay đổi thời gian trong code:
python
schedule.every().day.at("06:00").do(Lay_Bat_Dong_San)

📊 Cấu trúc dữ liệu đầu ra
File Excel bao gồm các cột sau:
    Tên cột	    Mô tả	                Ví dụ
    titles	    Tiêu đề tin đăng	    "Cho thuê mặt bằng Q1"
    describes	Mô tả chi tiết	        "Mặt bằng 50m2, kinh doanh..."
    prices	    Giá	                    "15 triệu/tháng"
    acreages	Diện tích	            "50 m²"
    addresss	Địa chỉ	                "Quận 1, TP HCM"
    links	    URL bài đăng	        "https://homedy.com/..."

🔧 Tùy chỉnh
Thay đổi địa điểm: Sửa dòng code sau để chọn thành phố khác:
    ho_chi_minh = city_list.find_element(By.XPATH, ".//div[@class='loc-item' and contains(text(),'TP Hồ Chí Minh')]")

Thay đổi loại bất động sản: Sửa dòng code sau:
    bat_dong_san_khac = category_list.find_element(By.XPATH, ".//a[contains(text(),'Bất động sản khác')]")

Thay đổi thời gian chờ: Điều chỉnh các tham số:
    time.sleep(3)  # Giảm nếu mạng nhanh, tăng nếu mạng chậm
    WebDriverWait(driver, 30)  # Thời gian chờ tối đa

⚠️ Lưu ý
Nếu website thay đổi giao diện, cần cập nhật lại các selector trong code
Đảm bảo ChromeDriver tương thích với phiên bản Chrome
Script sử dụng cơ chế retry (thử lại 3 lần) khi gặp lỗi
Dữ liệu được lưu tự động vào ổ D theo đường dẫn đã chỉ định
