import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_data(input_path, output_path):
    # Load the CSV file
    df = pd.read_csv(input_path)

    # Assuming 'class' is the target variable, let's encode it using LabelEncoder
    le = LabelEncoder()
    df['class'] = le.fit_transform(df['class'])

    # Assuming other columns are binary, let's map 'Yes' and 'No' to 1 and 0
    binary_mapping = {'Yes': 1, 'No': 0}
    binary_columns = ['Polyuria', 'Polydipsia', 'sudden weight loss', 'weakness', 'Polyphagia',
                      'Genital thrush', 'visual blurring', 'Itching', 'Irritability',
                      'delayed healing', 'partial paresis', 'muscle stiffness', 'Alopecia', 'Obesity']

    for column in binary_columns:
        df[column] = df[column].map(binary_mapping)

    # Save the preprocessed data to a new CSV file
    df.to_csv(output_path, index=False)