from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from tqdm import tqdm
import re
from selenium.webdriver.common.by import By
from tools.file import FileManager
from market_research.scraper._scraper_scheme import Scraper




class ModelScraper_se(Scraper):
    def __init__(self, enable_headless=True,
                 export_prefix="sse_model_info_web", intput_folder_path="input", output_folder_path="results",
                 verbose: bool = False, wait_time=2):

        super().__init__(enable_headless=enable_headless, export_prefix=export_prefix,
                         intput_folder_path=intput_folder_path, output_folder_path=output_folder_path)

        self.tracking_log = verbose
        self.wait_time = wait_time
        self.file_manager = FileManager
        self.log_dir = "logs/sse/models"
        if self.tracking_log:
            FileManager.make_dir(self.log_dir)
   
    @property
    def data(self):
        return self._data
    
    def _fetch_model_data(self, demo_mode:bool=False) -> pd.DataFrame:
        
        if demo_mode:
            # Load existing JSON data
            # df_models = pd.read_json('https://raw.githubusercontent.com/xikest/research_market_tv/main/l_scrape_model_data.json', orient='records', lines=True)
            df_models = pd.read_json('se_scrape_model_data.json', orient='records', lines=True)

            print("operating demo")


        else:
          # dict_models = {}
        # url ="https://www.samsung.com/us/televisions-home-theater/tvs/oled-tvs/55-class-oled-s95d-qn55s95dafxza/"
        # self._extract_global_specs(url=url)
        # dict_info = self._extract_model_details(url)
        # dict_models["key"] = dict_info
        # dict_spec = self._extract_global_specs(url=url)
        # dict_models["key"].update(dict_spec)
            print("collecting models")
            url_series_set = self._get_series_urls()
            url_series_dict = {}
            for url in url_series_set:
                url_models = self._extract_models_from_series(url=url)
                url_series_dict.update(url_models)
            print("number of total model:", len(url_series_dict))
            print("collecting spec")
            visit_url_dict = {}
            dict_models = {}
            cnt_loop=2
            
            for cnt in range(cnt_loop):#main try
                for key, url_model in tqdm(url_series_dict.items()):
                    try:
                        dict_info = self._extract_model_details(url_model)
                        dict_models[key] = dict_info
                        dict_spec = self._extract_global_specs(url=url_model)
                        dict_models[key].update(dict_spec)
                        visit_url_dict[key] = url_model
                    except Exception as e:
                        if cnt == cnt_loop - 1 :
                            print(f"\nFailed to get info from {key}")
                            print(e)
                        pass
                break

            if self.tracking_log:
                print("\n")
                for model, url in visit_url_dict.items():  print(f"{model}: {url}")
                
            df_models = pd.DataFrame.from_dict(dict_models).T
            df_models.to_json(self.output_folder / 'se_scrape_model_data.json', orient='records', lines=True)
        
        FileManager.df_to_excel(df_models.reset_index(), file_name=self.output_xlsx_name, sheet_name="raw_na",
                                    mode='w')
        return df_models
    
    def _wrap_get_segments_url(func):
        def wrapper(self):
            seg_urls = {
                "neo_qled": "https://www.samsung.com/us/televisions-home-theater/tvs/all-tvs/?technology=Samsung+Neo+QLED+8K,Samsung+Neo+QLED+4K",
                "oled": "https://www.samsung.com/us/televisions-home-theater/tvs/oled-tvs/",
                "lifestyle": "https://www.samsung.com/us/televisions-home-theater/tvs/all-tvs/?technology=The+Frame,The+Sero,Portable+Projector,The+Terrace,The+Serif,4K+Laser+Projectors",
                "qled": "https://www.samsung.com/us/televisions-home-theater/tvs/qled-4k-tvs/"
            }
            
            dict_segurls = {}
            
            for seg, seg_url in seg_urls.items():
                dict_segurls[seg] = func(self, seg_url)
            
            print("Segment URLs collected:", dict_segurls)
            return dict_segurls
        return wrapper
          
    @_wrap_get_segments_url
    def _get_series_urls(self, url) -> set:

        prefix = "https://www.samsung.com"
        step = 200
        url_series = set()
        try_total = 5
        for _ in range(2): #page_checker
            for _ in range(try_total):
                driver = self.web_driver.get_chrome()
                try:
                    driver.get(url=url)
                    time.sleep(self.wait_time)
                    scroll_distance_total = self.web_driver.get_scroll_distance_total()
                    scroll_distance = 0

                    while scroll_distance < scroll_distance_total:
                        for _ in range(2):
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'html.parser')
                            elements = soup.find_all('a', class_="ProductCard-learnMore-1030346118 isTvPf")
                            for element in elements:
                                url_series.add(prefix + element['href'].strip())
                            driver.execute_script(f"window.scrollBy(0, {step});")
                            time.sleep(self.wait_time)
                            scroll_distance += step
                    driver.quit()
                    break
                except Exception as e:
                    driver.quit()
                    if self.tracking_log:
                        print(f"Try collecting {_ + 1}/{try_total}")
                        print(e)
        print("The website scan has been completed.")
        print(f"number of total series: {len(url_series)}")
        print(url_series)
        return url_series

    def _extract_models_from_series(self, url: str, prefix="https://www.samsung.com/") -> dict:
        """
        Extract all model URLs from a given series URL.
        """
        try_total = 5
        for cnt_try in range(try_total):
            try:
                dict_url_models = {}
                driver = self.web_driver.get_chrome()
                driver.get(url=url)
                time.sleep(self.wait_time)
                radio_btns = driver.find_elements(By.CLASS_NAME, "SizeTile_button_wrapper__rIeR3")
                
                for btn in radio_btns:
                    btn.click()
                    time.sleep(self.wait_time)
                    element_url =  driver.current_url
                    label = self.file_manager.get_name_from_url(element_url)
                    dict_url_models[label] = element_url.strip()
                if self.tracking_log:
                    print(f"SSE {self.file_manager.get_name_from_url(url)[4:]} series: {len(dict_url_models)}")
                for key, value in dict_url_models.items():
                    if self.tracking_log:
                        print(f'{key}: {value}')
                return dict_url_models
            except Exception as e:
                if self.tracking_log:
                    print(f"_extract_models_from_series try: {cnt_try + 1}/{try_total}")

    def _extract_model_details(self, url: str='') -> dict:
        """
        Extract model information (name, price, description) from a given model URL.
        """

        driver = self.web_driver.get_chrome()
        driver.get(url=url)
        time.sleep(self.wait_time)
        if self.tracking_log:
            print(" Connecting to", url)
  
        dict_info = {}
        label_element = driver.find_element(By.CLASS_NAME,"Header_sku__PBGyN")
        label = label_element.text
        print(f"label:{label}")
        dict_info["model"] = label.split()[-1]
        try:
            price = driver.find_element(By.CLASS_NAME,'Header_newdesc__NRnRP')          
            split_price = price.text.split('$')
            prices = split_price
            print(f"prices:{prices}")
            if len(prices) > 2:
                dict_info["price"] = float(prices[-2].replace(',', ''))
                dict_info["price_original"] = float(prices[-1].replace(',', ''))
                dict_info["price_gap"] = round(dict_info["price_original"] - dict_info["price"], 1)
            else:
                dict_info["price"] = price
        except:
            dict_info["price"] = None
        dict_info.update(self._parse_model_name(dict_info.get("model")))
        
        descriptions = driver.find_element(By.CLASS_NAME,'Header_productTitle__48wOA').text        
        dict_info["description"] = descriptions
        
        if self.tracking_log:
            print(dict_info)
        return dict_info

    def _extract_global_specs(self, url: str='https://www.lg.com/us/tvs/lg-oled77g4wua-oled-4k-tv-b') -> dict:
        """
        Extract global specifications from a given model URL.
        """
        try_total = 1
        model = None
        driver = None
        case = 0
        for cnt_try in range(try_total):
            try:
                driver = self.web_driver.get_chrome()
                driver.get(url=url)
                model = self.file_manager.get_name_from_url(url)
                dir_model = f"{self.log_dir}/{model}"
                stamp_today = self.file_manager.get_datetime_info(include_time=False)
                stamp_url = self.file_manager.get_name_from_url(url)
                if self.tracking_log:
                    self.file_manager.make_dir(dir_model)
                if self.tracking_log:
                    driver.save_screenshot(f"./{dir_model}/{stamp_url}_0_model_{stamp_today}.png")
                time.sleep(self.wait_time)
                
                try: 
                    element_specs = driver.find_element(By.CLASS_NAME, f"tl-btn-expand")
                    self.web_driver.move_element_to_center(element_specs)
                    time.sleep(self.wait_time)
                    
                    element_specs.click()
                    time.sleep(self.wait_time)
                except:
                    pass
                    time.sleep(self.wait_time)
                

                if self.tracking_log:
                    driver.save_screenshot(
                        f"./{dir_model}/{stamp_url}_1_element_all_specs_{stamp_today}.png")
                dict_spec = dict()
                

                table_elements= driver.find_elements(By.CLASS_NAME, "subSpecsItem.Specs_subSpecsItem__acKTN")
                for element in table_elements:
                    item_name = element.find_element(By.CLASS_NAME, 'Specs_subSpecItemName__IUPV4').text
                    item_value = element.find_element(By.CLASS_NAME, 'Specs_subSpecsItemValue__oWnMq').text
                    item_name = re.sub(r'[\n?]', '', item_name)
                    item_value = re.sub(r'[\n?]', '', item_value)
                    dict_spec[item_name] = item_value
                
                driver.quit()
                if self.tracking_log:
                    print(f"Received information from {url}")
                return dict_spec
            except Exception as e:
                if self.tracking_log:
                    print(f"An error occurred on page 3rd : {model} try {cnt_try + 1}/{try_total}")
                    print(e)
                driver.quit()
                pass


    def _parse_model_name(self, model: str):
        model = model.lower()  # 대소문자 구분 제거
        model = model[:-4]
        dict_info = {}
        
        # 연도 매핑
        year_mapping = {'qn':
                            {'ca': "2023",
                            'da': "2024",
                            'ea': "2025",
                            'fa': "2026"},
                        'un':{ 
                            'cu': "2024",
                            'du': "2024",
                            'eu': "2024",
                            'fu': "2024",
                            }
                        }
        
        if "qn" in model or "kq" in model:
            dict_info["grade"] = model[:2]            
            model= model.replace(dict_info["grade"], "")
            dict_info["size"] = model[:3]
            model= model.replace(dict_info["size"], "")
            dict_info["year"] = model[-2:]
            dict_info["year"] = year_mapping.get('qn').get(dict_info.get("year"), None)
            dict_info["series"] = model

 
        # "lcd" 
        elif "un" in model :
            dict_info["grade"] = model[:2]            
            model= model.replace(dict_info["grade"], "")
            dict_info["size"] = model[:3]
            model= model.replace(dict_info["size"], "")
            dict_info["year"] = model[-2:]
            dict_info["year"] = year_mapping.get('un').get(dict_info.get("year"), None)
            dict_info["series"] = model
        else:
            raise ValueError("NO TV product")
        return dict_info



    def _convert_soup_to_dict(self, soup):
        """
        Convert BeautifulSoup soup to dictionary.
        """
        try:
            h4_tag = soup.find('h4').text.strip()
            p_tag = soup.find('p').text.strip()
        except:
            try:
                h4_tag = soup.find('h4').text.strip()
                p_tag = ""
            except Exception as e:
                print("Parser error", e)
                h4_tag = "Parser error"
                p_tag = "Parser error"
        return {h4_tag: p_tag}
