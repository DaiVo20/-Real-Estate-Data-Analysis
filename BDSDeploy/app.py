from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

model_file = open('linear_model.pkl', 'rb')
model = pickle.load(model_file, encoding='bytes')

@app.route('/')
def index():
    return render_template('index.html', price=0)

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Predict the real estate price based on user inputs
    and render the result to the html page
    '''

    if request.method == 'POST':
        type_real_estate = request.form['type_real_estate']
        region = request.form['region']
        area = request.form['area']
        property_legal_document = request.form['property_legal_document']
        rooms = request.form['rooms']
        toilets = request.form['toilets']
        floors = request.form['floors']
        year = request.form['year']
        month = request.form['month']
        width = request.form['width']
        size = request.form['size']
        front_road = request.form['front_road']
    


    o_type_real_estate = type_real_estate
    o_area = area
    o_region = region
    o_property_legal_document = property_legal_document
    o_rooms = rooms
    o_toilets = toilets
    o_floors = floors

    type_real_estate = "type_real_estate_" + type_real_estate
    area = "area_" + area
    property_legal_document = 'property_legal_document_' + property_legal_document
    rooms = "rooms_"+ rooms
    region = "region_"+ region
    toilets = "toilets_"+ toilets
    floors = "floors_"+ floors

    feature_name = ['size', 'width', 'front_road', 'year', 'month',
                    'area_Huyện Bình Chánh', 'area_Huyện Bắc Tân Uyên',
                    'area_Huyện Cần Giờ', 'area_Huyện Cẩm Mỹ', 'area_Huyện Củ Chi',
                    'area_Huyện Dầu Tiếng', 'area_Huyện Hóc Môn', 'area_Huyện Long Thành',
                    'area_Huyện Nhà Bè', 'area_Huyện Nhơn Trạch', 'area_Huyện Phú Giáo',
                    'area_Huyện Thống Nhất', 'area_Huyện Trảng Bom', 'area_Huyện Tân Phú',
                    'area_Huyện Vĩnh Cửu', 'area_Huyện Xuân Lộc', 'area_Huyện Định Quán',
                    'area_Quận 1', 'area_Quận 10', 'area_Quận 11', 'area_Quận 12',
                    'area_Quận 2', 'area_Quận 3', 'area_Quận 4', 'area_Quận 5',
                    'area_Quận 6', 'area_Quận 7', 'area_Quận 8', 'area_Quận 9',
                    'area_Quận Bình Thạnh', 'area_Quận Bình Tân', 'area_Quận Gò Vấp',
                    'area_Quận Phú Nhuận', 'area_Quận Tân Bình', 'area_Quận Tân Phú',
                    'area_Thành phố Biên Hòa', 'area_Thành phố Dĩ An',
                    'area_Thành phố Long Khánh', 'area_Thành phố Thuận An',
                    'area_Thành phố Thủ Dầu Một', 'area_Thành phố Thủ Đức',
                    'area_Thị xã Bến Cát', 'area_Thị xã Tân Uyên', 'region_Hồ Chí Minh',
                    'region_Đồng Nai', 'property_legal_document_Đang chờ sổ',
                    'property_legal_document_Đã có sổ', 'rooms_1', 'rooms_10', 'rooms_2',
                    'rooms_3', 'rooms_4', 'rooms_5', 'rooms_6', 'rooms_7', 'rooms_8',
                    'rooms_9', 'rooms_Nhiều hơn 10', 'toilets_1', 'toilets_2', 'toilets_3',
                    'toilets_4', 'toilets_5', 'toilets_6', 'toilets_Nhiều hơn 6',
                    'floors_1', 'floors_10', 'floors_2', 'floors_3', 'floors_4', 'floors_5',
                    'floors_6', 'floors_7', 'floors_8', 'floors_9', 'floors_Nhiều hơn 10',
                    'type_real_estate_Khác', 'type_real_estate_Nhà ở',
                    'type_real_estate_Đất']

    df = pd.DataFrame(columns=feature_name)
    df.at[0, :] = 0

    if type_real_estate in df.columns:
        df[type_real_estate] = 1
    if area in df.columns:
        df[area] = 1
    if rooms in df.columns:
        df[rooms] = 1
    if toilets in df.columns:
        df[toilets] = 1
    if property_legal_document in df.columns:
        df[property_legal_document] = 1
    if floors in df.columns:
        df[floors] = 1
    if region in df.columns:
        df[region] = 1

    df['width'] = float(width)
    df['size'] = float(size)
    df['front_road'] = float(front_road)
    df['year'] = int(year)
    df['month'] = int(month)

    price_predict = np.round(model.predict(df)[0], 2)
    return render_template('index.html', price=price_predict,
                            type_real_estate=o_type_real_estate,
                            region =  o_region,
                            property_legal_document=o_property_legal_document,
                            area = o_area,
                            rooms = o_rooms,
                            toilets = o_toilets,
                            floors=o_floors,
                            width = width,
                            size = size,
                            front_road=front_road,
                            year=year,
                            month=month)


if __name__ == '__main__':
    app.run()
