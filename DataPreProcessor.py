import re
import numpy as np
import pandas as pd
import regex
from datetime import datetime


class DataPreProcessor():

    def __init__(self, data):
        '''
            Contructor tạo tạo đối tượng để tiền xử lý dữ liệu

            Parameters
            ----------
                - data (pd.DataFrame): dữ liệu dạng dataframe trong pandas cần xử lý
        '''
        self.data = data

    def remove_excess_whitespace(self, on_cell=True, on_column_name=False):
        '''
            Xóa khoảng trắng dư thừa của tên cột và toàn bộ dữ liệu string trên dataframe

            Parameters
            ----------
                - on_cell (bool): Lựa chọn xóa khoảng trắng dư thừa toàn bộ dữ liệu trên dataframe. Giá trị mặc định là True
                - on_column_name (bool): Lựa chọn xóa khoảng trắng dư thừa trên tên thuộc tính. Giá trị mặc định là False
        '''
        if on_cell:
            for i in self.data.columns:
                if self.data[i].dtype == int:
                    continue
                self.data[i] = [j.strip() for j in self.data[i]]

        if on_column_name:
            self.data.columns = [i.strip() for i in self.data.columns]

    def replace_value(self, features, value_to_replaces, replace_values):
        '''
            Thay thế giá trị của các thuộc tính trong bộ dữ liệu
            Lưu ý: Độ dài features, value_to_replaces và replace_values phải như nhau

            Parameters
            ----------
                - features (list): Danh sách tên các thuộc tính cần thay thế giá trị
                - value_to_replaces: Danh sách các giá trị cần thay thế tương ứng với các thuộc tính trong danh sách
                - replace_values: Danh sách các giá trị thay thế bằng các giá trị này tương ứng với các thuộc tính trong danh sách
                
        '''
        if len(features) == len(value_to_replaces) == len(replace_values):
            for feature, value_to_replace, replace_value in zip(features, value_to_replaces, replace_values):
                self.data[feature].replace(r'[{}]'.format(value_to_replace), replace_value, inplace=True, regex=True)
        else:
            print("ERROR - Length of parameters are not the same")
    
    def convert_data_type(self, features, data_types):
        '''
            Chuyển đổi kiểu dữ liệu của một hoặc nhiều thuộc tính

            Parameters
            ----------
                - feature (string): Danh sách tên các thuộc tính cần chuyển đổi kiểu dữ liệu
                - data_types: Danh sách các kiểu dữ liệu tương ứng cần chuyển đổi
                
        '''
        for feature, data_type in zip(features, data_types):
            self.data[feature] = self.data[feature].astype(data_type)

    def __get_number_from_string(self, x):
        '''
            Tìm và trả về giá trị số nguyên đầu tiên trong chuổi bằng Regular Expression

            Parameters
            ----------
                - x (string): Chuỗi cần tách số

            Returns
            ----------
                - number (float): Số nguyên đầu tiên trong chuỗi x
        '''
        x = x.lower()
        # Tách các số có trong chuỗi
        # Số thực sẽ bị tách thành list do có chứa dấu phẩy(,) hoặc chấm(.)
        ele = re.findall(r'\d+[\.,]\d+', x)
        if len(ele) > 0:
            number = [float(_.replace(',', '.')) for _ in ele]

        else:
            number = np.nan

        if 'nhiều hơn' in x:
            return f'{number}+'

        return number

    def split_number(self, *features):
        '''
            Tách số trong một hay nhiều thuộc tính của data trong đối tượng

            Parameters
            ----------
                - features (list): Tên của một hoặc nhiều thuộc tính
        '''
        for feature in features:
            self.data[feature] = self.data[feature].apply(
                lambda x: self.__get_number_from_string(x) if x is not np.nan else np.nan)

    def drop_column(self, features):
        '''
            Xóa một hay nhiều thuộc tính của dữ liệu

            Parameters
            ----------
                - features (list): Danh sách các thuộc tính cần drop
        '''
        self.data.drop(features, axis=1, inplace=True)

    def drop_row_nan(self, subset):
        '''
            Xóa các dòng trong dữ liệu có giá trị là nan hoặc NaN

            Parameters
            ----------
                - subset (list): Danh sách các thuộc tính để kiểm tra
        '''
        self.data.dropna(subset=subset, inplace=True)

    def convert_timestamp_to_date(self, feature, format='%d/%m/%Y'):
        '''
            Chuyển giá của một thuộc tính trong dataframe ở timestamp sang dạng ngày tháng 

            Parameters
            ----------
                - feature (string): Tên thuộc tính của dữ liệu chứa giá trị timestamp
                - format (string): Định dạng ngày tháng cần chuyển đổi. Mặc định là '%d/%m/%Y'
        '''
        self.data[feature] = [datetime.fromtimestamp(
            x/1000) for x in self.data[feature]]
        self.data[feature] = self.data[feature].dt.strftime(format)

    def check_unique_unit(self, feature):
        '''
            Kiểm tra giá các đơn vị của một thuộc tính trong dữ diệu 

            Parameters
            ----------
                - feature (string): Tên thuộc tính của dữ liệu cần kiểm tra đơn vị

            Returns
            ----------
                - unit_uniques (list): Danh dách các đơn vị có trong thuộc tính
        '''
        unit_uniques = []
        # for value in self.data[feature].unique():
        #     if value is np.nan or isinstance(value, int) or isinstance(value, float):
        #         continue
        #     spl = value.split(' ')
        #     if spl[1] not in unit_uniques:
        #         unit_uniques.append(spl[1])
        for value in self.data.loc[:, feature]:
            try:
                units = regex.findall(r'(?i)\p{L}+\b', value)
                if len(units) > 1:
                    if units not in unit_uniques:
                        unit_uniques.append(units)
                else:
                    if units[0] not in unit_uniques:
                        unit_uniques.append(units[0])
            except:
                continue

        return unit_uniques

    def check_value_unit(self, units, feature):
        valueOfUnit = {}
        for idx, val in enumerate(self.data.loc[:, feature]):
            count = 0
            try:
                for _ in units:
                    if _ in val:
                        count += 1
            except:
                continue
            if len(units) == count:
                valueOfUnit[idx] = val
        return valueOfUnit

    def __remove_unit(self, x, uniques, converters):
        '''
            Xóa và chuyển đổi giá trị chuỗi đầu vào về cùng một đơn vị. Với danh sách các đơn vị đầu vào
            và danh sách tỷ lệ chuyển đổi giá trị tương tứng
            Lưu ý: danh sách các đơn vị và danh sách tỷ lệ chuyển đổi phải phù hợp và có cùng kích thước

            Parameters
            ----------
                - x (string): Chuổi giá trị cần chuyển đổi
                - uniques (list): Danh sách các đơn vị
                - converters (list): Danh sách tỷ lệ chuyển đổi tương ứng

            Returns
            ----------
                - number (nan hoặc int hoặc float): giá trị trả về là số đã được đổi về cùng một đơn vị
                nếu chuỗi đầu vào khác nan hoặc nan thì không chuyển đổi
        '''
        if x is np.nan or isinstance(x, int) or isinstance(x, float):
            return x
        spl = x.split(' ')
        for unit_unique, unit_converter in zip(uniques, converters):
            if spl[1] == unit_unique:
                return float(spl[0].replace(',', '.')) * unit_converter
        return float(spl[0])

    def convert_to_same_unit(self, feature, uniques, converters, add_unit_name=False, unit_name=None):
        '''
            Xóa và chuyển đổi các giá trị của một thuộc tính về cùng một đơn vị. Với danh sách các đơn vị đầu vào
            và danh sách tỷ lệ chuyển đổi giá trị tương tứng
            Lưu ý: danh sách các đơn vị và danh sách tỷ lệ chuyển đổi phải phù hợp và có cùng kích thước

            Parameters
            ----------
                - feature (string): Tên thuộc tính cần chuyển đổi
                - uniques (list): Danh sách các đơn vị
                - converters (list): Danh sách tỷ lệ chuyển đổi tương ứng
                - add_unit_name (bool): Để xem xét có thực hiện đổi tên thuộc tính hay không (thêm đơn vị vào sau tên thuộc tính)
                - unit_name (string): tên đơn vị cần thêm thêm chọn thay đổi tên thuộc tính
        '''
        if len(uniques) != len(converters):
            print("[ERROR] - Length uniques and converters are not the same")
            return

        self.data[feature] = self.data[feature].apply(
            lambda x: self.__remove_unit(x, uniques, converters))
        if add_unit_name:
            if unit_name is None:
                print("[ERROR] - Unit name can not none")
            else:
                self.data.rename(
                    columns={feature: f'{feature} ({unit_name})'}, inplace=True)

    def convert_unit(self, feature, convert_rate, add_unit_name=False, unit_name=None):
        '''
            Chuyển đổi giá trị của thuộc tính với một tỷ lệ nhất định.

            Parameters
            ----------
                - feature (string): Tên thuộc tính cần chuyển đổi
                - convert_rate (int hoặc float): Tỷ lệ chuyển đổi
        '''
        self.data[feature] = self.data[feature].apply(
            lambda x: x/convert_rate if x is not np.nan else np.nan)

        if add_unit_name:
            if unit_name is None:
                print("[ERROR] - Unit name can not none")
            else:
                self.data.rename(
                    columns={feature: f'{feature} ({unit_name})'}, inplace=True)

    def merge_column(self, name_feature, features):
        '''
            Merge các thuộc tính trong dữ liệu lại với nhau thành một thuộc tính mới
            Lưu ý: Cần ít nhất hai thuộc tính

            Parameters
            ----------
                - name_feature (string): Tên thuột tính mới
                - features (list): danh sách các thuộc tính cần merge
        '''
        values = []
        for val in self.data[features].values:
            x = ''.join(val)

            values.append(x)

        self.data[name_feature] = values

    def save_as_csv(self, file_name):
        '''
            Lưu lại dữ liệu đã được tiền xử lý dưới dạng file csv

            Parameters
            ----------
                - file_name (string): Tên file cần lưu hoặc đường dẫn đến nơi lưu trữ
        '''
        self.data.to_csv(file_name, index=False)
