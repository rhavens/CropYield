import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, ARDRegression
from sklearn.metrics import mean_squared_error, RocCurveDisplay
import os
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
import plotly.figure_factory as ff

def train_model(data: pd.DataFrame):
    x = data[['state_code', 'county_code', 'year']]
    y = data[['value']]

    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    plot_model(data)
    score = model.score(X_test, y_test)
    return score

def draw_map(data: pd.DataFrame):
    # fips = data[['state_code', 'county_code']].apply(lambda row: '_'.join(row.values.astype(str)), axis=1).to_dict()
    state = data['state_code'].astype(str).str.zfill(2)
    county = data['county_code'].astype(str).str.zfill(3)

    fips = state + county
    fips = list(fips.to_dict().values())

    values = range(len(fips))

    fig = ff.create_choropleth(fips=fips, values=values)
    fig.layout.template = None
    fig.show()

    pass

def plot_model(df: pd.DataFrame):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = df['state_code']
    y = df['county_code']
    z = df['year']
    c = df['value']

    img = ax.scatter(x, y, z, c=c, cmap=plt.hot())
    fig.colorbar(img)
    ax.set_xlabel('state')
    ax.set_ylabel('county')
    ax.set_zlabel('year')
    plt.show()
    # pivot_df = df.pivot_table(index='state_name', columns='year', values='value', aggfunc='mean')
    # sns.heatmap(data=pivot_df, cmap='viridis')
    # plt.xlabel('Year')
    # plt.ylabel('State')
    # plt.title('Heatmap of Value by State and Year')
    # plt.show()


def train_models(data: pd.DataFrame, location) -> float:
    x = data[['STATE_FIPS_CODE', 'COUNTY_CODE', 'YEAR']]
    y = data[["VALUE"]]

    try:
        X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=42)
        return linear_model(X_train, X_test, y_train, y_test, location)
    except ValueError:
        return -1
        print("error")# some counties have such little data that it is impossible to train a model

    # ard_model(X_train, X_test, y_train, y_test)


def linear_model(X_train, X_test, y_train, y_test, location) -> float:
    model = LinearRegression()
    model.fit(X_train, y_train)
    # plot_county_data(model, X_test, y_test, "Linear Regression", location)
    return model.score(X_test, y_test)


# doesn't seem very useful
# def ard_model(X_train, X_test, y_train, y_test):
#     model = ARDRegression()
#     model.fit(X_train, y_train)
#     plot_data(model, X_test, y_test, "ARD Regression")


def plot_county_data(model, X_test, y_test, display_name, location):
    y_pred = model.predict(X_test)

    plt.scatter(X_test, y_test, color='blue', label='Actual Values')
    plt.plot(X_test, y_pred, color='red', linewidth=2,
             label=f'{location['state']}, {location['state_code']}, {location['county']}, {location['county_code']}')

    plt.title(f'{display_name} - Actual vs Predicted Values')
    plt.xlabel('Year')
    plt.ylabel('Crop Value')
    plt.legend()
    plt.show()


def plot_us_data(model, X_test, y_test):
    pass


def get_data(data, county_code, state_code) -> pd.DataFrame:
    county_data = data.loc[(data['COUNTY_CODE'] == county_code) & (data["STATE_FIPS_CODE"] == state_code)]
    return county_data
    # state_data = df.loc[df["STATE_FIPS_CODE"] == state_code]
    # return state_data


def get_states(data):
    state_data_unique = pd.Series({c: data[c].unique() for c in data})
    return zip(state_data_unique.STATE_FIPS_CODE, state_data_unique.STATE_NAME)


def get_counties_from_state(data, state_code):
    county_data = data.loc[data["STATE_FIPS_CODE"] == state_code]
    county_data_unique = pd.Series({c: county_data[c].unique() for c in county_data})
    return zip(county_data_unique.COUNTY_CODE, county_data_unique.COUNTY_NAME)


def train_all_counties(file_path, data):
    results = []
    # Train a LR model for each individual county
    for _state_code, _state_name in get_states(data):
        print(f'Processing state {_state_name}')
        for _county_code, _county_name in get_counties_from_state(data, _state_code):
            _location = {
                'state': _state_name,
                'state_code': _state_code,
                'county': _county_name,
                'county_code': _county_code
            }
            _county_data = get_data(data, _county_code, _state_code)
            results.append(
                [_state_code, _state_name, _county_code, _county_name, train_models(_county_data, _location)])

    columns = ['state_code', 'state_name', 'county_code', 'county_name', 'fit']
    results_frame = pd.DataFrame(columns=columns)
    for result in results:
        results_frame.loc[-1] = result
        results_frame.index += 1
    results_frame = results_frame.sort_index()
    results_frame.to_csv(file_path + 'linear_regression_fits.csv', index=False)
    print(results_frame)


if __name__ == "__main__":
    _file_name = 'crop_data_cleaned_pruned.csv'  # Adjust the input file path as needed
    _file_path = os.getcwd().replace("backend", "") + os.path.sep + "data" + os.path.sep
    _data = pd.read_csv(_file_path + _file_name)

    draw_map(_data)
    # train_model(_data)
    # train_all_counties(_file_path, _data)
