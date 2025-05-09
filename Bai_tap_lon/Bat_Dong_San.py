import time
import pandas as pd
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

def Lay_Bat_Dong_San():
    #1. Vào website đã chọn.
    driver = webdriver.Chrome()
    driver.get("https://homedy.com/")
    time.sleep(10)

    #2. Click chọn bất kì Tỉnh/TP(Hà Nội, Đà Nẵng, Hồ Chí Minh, …). Chọn bất kì loại nhà đất(Căn hộ chung cư, nhà, đất, …).
    try:
        driver.find_element(By.ID, "LocationName").click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "choose-city"))).click()
        city_list = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dropdown_cities")))
        ho_chi_minh = city_list.find_element(By.XPATH, ".//div[@class='loc-item' and contains(text(),'TP Hồ Chí Minh')]")
        ho_chi_minh.click()
        time.sleep(1)
        driver.find_element(By.ID, "CategoryName").click()
        time.sleep(1)
        category_list = driver.find_element(By.ID, "Categories")
        bat_dong_san_khac = category_list.find_element(By.XPATH, ".//a[contains(text(),'Bất động sản khác')]")
        print(bat_dong_san_khac.text)
        bat_dong_san_khac.click()
        time.sleep(1)
    except Exception as e:
        print("Lỗi khi chọn thành phố và loại bất động sản:", e)
        driver.quit()
        return

    data = []
    trang = 1
    max_retries = 3
    
    while True:
        #5. Lấy tất cả dữ liệu của các trang.
        print(f"Đang lấy dữ liệu trang {trang}...")
        url = f"https://homedy.com/ban-bat-dong-san-khac-tp-ho-chi-minh/p{trang}"
        driver.get(url)
        time.sleep(3)
        
        try:
            notfound = driver.find_element(By.CSS_SELECTOR, "div.report")
            print("Hết trang")
            break
        except:
            pass
        
        #4. Lấy tất cả dữ liệu(Tiêu đề, Mô tả, Địa chỉ, Diện tích, Giá) hiển thị ở bài viết.
        danhsach_bds = driver.find_elements(By.CLASS_NAME, "product-content")
        
        for i in range(len(danhsach_bds)):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    current_bds = driver.find_elements(By.CLASS_NAME, "product-content")[i]
                    tieude = current_bds.find_element(By.CSS_SELECTOR, "h3 a.title").get_attribute("title").strip()
                    link = current_bds.find_element(By.CSS_SELECTOR, "h3 a.title").get_attribute("href")
                    
                    try:
                        gia = current_bds.find_element(By.CLASS_NAME, "price").text.strip()
                    except NoSuchElementException:
                        gia = "Không có thông tin"
                    
                    try:
                        dientich = current_bds.find_element(By.CLASS_NAME, "acreage").text.strip()
                    except NoSuchElementException:
                        dientich = "Không có thông tin"
                    
                    try:
                        diachi = current_bds.find_element(By.CLASS_NAME, "address").text.strip()
                    except NoSuchElementException:
                        diachi = "Không có thông tin"

                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(link)
                    time.sleep(3)
                    
                    try:
                        mota = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".description.readmore"))
                        ).text.strip()
                    except:
                        mota = "Không có thông tin"

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])    
                    data.append({
                        "titles": tieude,
                        "describes": mota,
                        "prices": gia,
                        "acreages": dientich,
                        "addresss": diachi,
                        "links": link
                    })
                    print(f"Tiêu đề: {tieude} - giá: {gia} - địa chỉ: {diachi} - diện tích: {dientich}")
                    break
                    
                except StaleElementReferenceException:
                    retry_count += 1
                    print(f"Lỗi stale element, thử lại lần {retry_count}")
                    time.sleep(2)
                    if retry_count == max_retries:
                        print("Đã thử lại tối đa số lần, bỏ qua tin đăng này")
                except Exception as e:
                    print("Lỗi khi lấy dữ liệu tin đăng:", e)
                    break
        trang += 1 
    driver.quit()
    
    #6. Lưu dữ liệu
    if data:
        df = pd.DataFrame(data)
        try:
            df.to_excel("D:\Tu_dong_hoa_python\Bai_tap_lon\Bat_Dong_San_Khac_TP_HCM.xlsx", index=False, engine='openpyxl')
            print(f"Lưu thành công excel với {len(data)} bản ghi")
        except Exception as e:
            print("Lỗi khi lưu file Excel:", e)
    else:
        print("Không có dữ liệu để lưu")

#7. Set lịch chạy vào lúc 6h sáng hằng ngày.
schedule.every().day.at("06:00").do(Lay_Bat_Dong_San)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
