import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# App title
st.title("INX Employment Performance Rate App")

# Description
st.write(''' INX Future Inc, (referred to as INX), is one of the leading data analytics and automation solutions providers 
with over 15 years of global business presence. INX is consistently rated among the top 20 best employers for the past 5 
years. INX's human resource policies are considered employee-friendly and widely perceived as best practices in the industry.''')

# Load data

df= pd.read_excel("C:\\Users\\maina\\OneDrive\\Desktop\\Employee Performance project\\INX_Future_Inc_Employee_Performance_CDS_Project2_Data_V1.8.xls")
st.write(df.head(5))

# User slider to select number of rows to display
num_rows = st.slider("Select the number of rows", min_value=1, max_value=len(df), value=5)
st.write(f"Displaying first {num_rows} rows of the dataset")
st.write(df.head(num_rows))

# Display dataset shape
st.write(f"Dataset shape: {df.shape}")

# Check for duplicates
if st.checkbox("Check for duplicates"):
    duplicates = df[df.duplicated()]
    st.write(f"Found {len(duplicates)} duplicates")
    st.write(duplicates)

# Mapping categorical variables
df['EmpEnvironmentSatisfaction'] = df['EmpEnvironmentSatisfaction'].map({1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very High'})
df['EmpWorkLifeBalance'] = df['EmpWorkLifeBalance'].map({1: 'Bad', 2: 'Good', 3: 'Better', 4: 'Best'})
df['PerformanceRating'] = df['PerformanceRating'].map({1: 'Low', 2: 'Good', 3: 'Excellent', 4: 'Outstanding'})

# Label Encoding
encoded_columns = ['EmpNumber', 'Gender', 'EducationBackground', 'MaritalStatus', 'EmpDepartment', 'EmpJobRole', 
                   'BusinessTravelFrequency', 'EmpEducationLevel', 'EmpEnvironmentSatisfaction', 'EmpJobInvolvement', 
                   'EmpJobSatisfaction', 'OverTime', 'EmpRelationshipSatisfaction', 'EmpWorkLifeBalance', 'Attrition', 
                   'PerformanceRating']

le_dict = {col: LabelEncoder() for col in encoded_columns}

for column in encoded_columns:
    le_dict[column].fit(df[column])
    df[column] = le_dict[column].transform(df[column])

#Give x and y variables
x = df.drop('PerformanceRating',axis=1)
y = df['PerformanceRating']
#Split the variables
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)
#Give model variable
model = RandomForestClassifier()
#Fit the model
model.fit(x_train,y_train)
#Predict the model
y_pred = model.predict(x_test)
#Check accuracy
accuracy = accuracy_score(y_test,y_pred)
print("Accuracy:",accuracy)
st.write(f'Accuracy: {accuracy * 100:.2f}%')

# Sidebar for user input
st.sidebar.header("Enter New Data for Prediction")

user_input = {
    'EmpEnvironmentSatisfaction': st.sidebar.selectbox('EmpEnvironmentSatisfaction', le_dict['EmpEnvironmentSatisfaction'].classes_),
    'EmpLastSalaryHikePercent': st.sidebar.number_input("EmpLastSalaryHikePercent"),
    'TotalWorkExperienceInYears': st.sidebar.number_input("TotalWorkExperienceInYears"),
    'EmpWorkLifeBalance': st.sidebar.selectbox("EmpWorkLifeBalance", le_dict['EmpWorkLifeBalance'].classes_),
    'ExperienceYearsAtThisCompany': st.sidebar.number_input("ExperienceYearsAtThisCompany"),
    'ExperienceYearsInCurrentRole': st.sidebar.number_input("ExperienceYearsInCurrentRole"),
    'YearsSinceLastPromotion': st.sidebar.number_input("YearsSinceLastPromotion"),
    'YearsWithCurrManager': st.sidebar.number_input("YearsWithCurrManager"),
    'EmpDepartment': st.sidebar.selectbox("EmpDepartment", le_dict['EmpDepartment'].classes_),
    'EmpJobRole': st.sidebar.selectbox("EmpJobRole", le_dict['EmpJobRole'].classes_)
}

# Encode user input for prediction
encoded_input = {key: le_dict[key].transform([value])[0] if key in le_dict else value for key, value in user_input.items()}

# Convert to DataFrame for prediction
encoded_input_df = pd.DataFrame([encoded_input])

# Predict the PerformanceRating based on user input
if st.sidebar.button('Predict PerformanceRating'):
    prediction = model.predict(encoded_input_df)[0]
    st.sidebar.write('Predicted PerformanceRating:', le_dict['PerformanceRating'].inverse_transform([prediction])[0])

