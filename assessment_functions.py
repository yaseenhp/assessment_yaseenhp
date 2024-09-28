import pandas as pd
import requests 
import os 


def load_csv_df(file_name):
    """
    Return dataframe loaded with CSV file
    Args:
        file_name (string): File path or URL
    Returns:
        df (dataframe) : Dataframe loaded file file
    """
    try:
        if file_name.startswith(('http://', 'https://')):
            response = requests.get(file_name)
            response.raise_for_status()
        else:
            if not os.path.exists(file_name):
                raise FileNotFoundError(f"File not found: {file_name}")
        df = pd.read_csv(file_name)
        return df
    except requests.exceptions.ConnectionError:
        print("Error: Unable to open the file. Check your internet connection"
              "\nEnding the session")

    except pd.errors.EmptyDataError:
        print("Error: Empty CSV file.\nEnding the session")

    except pd.errors.ParserError:
        print("Error: Failed to parse the CSV file.\nEnding the session")

    except FileNotFoundError as fnf_err:
        print(f"Error: {fnf_err}\nEnding the session")

    except Exception as e:
        print(f"An error occurred: {e}\nEnding the session")
    # End the python session (Fail fast)
    exit() 
    
def get_employees_df():
    """
    Loads employee data and returns a DataFrame.
    Returns:
        (pd.DataFrame) : A DataFrame containing the employee data.
    """
    try:
        emp_filename = (
        "https://gist.githubusercontent.com/kevin336/acbb2271e66c10a5b73aacf82"
        "ca82784/raw/e38afe62e088394d61ed30884dd50a6826eee0a8/employees.csv"
        )
        return load_csv_df(emp_filename)
    except Exception as e:
        print(f"An error occurred loading emp csv: {e} \nEnding the session")
        exit()

def get_departments_df():
    """
    Loads department data and returns a DataFrame.
    Returns:
        (pd.DataFrame) : A DataFrame containing the department data.
    """
    try :
        dept_filename = (
        "https://gist.githubusercontent.com/kevin336/5ea0e96813aa88871c20d315b"
        "5bf445c/raw/d8fcf5c2630ba12dd8802a2cdd5480621b6a0ea6/departments.csv"
        )
        dep_df = load_csv_df(dept_filename)
        return dep_df
    except Exception as e:
        print(f"An error occurred loading dept csv: {e} \nEnding the session")
        exit()

def check_emp_df_columns(emp_df):
    """
    Performs the following checks on the given DataFrame:
    - Verifies that all required columns exist.
    - Ensures the DataFrame contains at least one row.
    Args:
        emp_df (dataframe): Employees dataframe
    Returns:
    """
    emp_col_list = ['EMPLOYEE_ID','FIRST_NAME','LAST_NAME','EMAIL',
                    'PHONE_NUMBER','HIRE_DATE','JOB_ID','SALARY',
                    'COMMISSION_PCT','MANAGER_ID','DEPARTMENT_ID']
    col_list = list(emp_df.columns.values)
    lists_mismatch = set(emp_col_list)!=set(col_list)

    if lists_mismatch:
        raise Exception("Employees data columns mismatch. \nEnding session")
        exit()
    elif emp_df.shape[0]==0:
        raise Exception("No records in the emp csv file. \nEnding session")
        exit()
        
def check_dept_df_columns(dept_df):
    """
    Performs the following checks on the given DataFrame:
    - Verifies that all required columns exist.
    - Ensures the DataFrame contains at least one row.
    Args:
        dept_df (dataframe): Departments dataframe
    Returns:
    """
    dept_col_list = ['DEPARTMENT_ID','DEPARTMENT_NAME','MANAGER_ID',
                     'LOCATION_ID']
    col_list = list(dept_df.columns.values)
    lists_mismatch = set(dept_col_list)!=set(col_list)
    if lists_mismatch:
        raise Exception("Department data columns mismatch. \nEnding session")
        exit()
    elif dept_df.shape[0]==0:
        raise Exception("No records in the dept csv file. \nEnding session")
        exit()

def data_prep_emp(emp_df):
    """
    Performs all necessary data preparation for employee data.
    Args:
        emp_df (dataframe): Employees dataframe
    Returns:
        emp_df (dataframe): Updated Employees dataframe
    """
    try:
        emp_df['SALARY'] = emp_df['SALARY'].astype(float)
        return emp_df
    except Exception as e:
        print(f"An error occurred in data_prep_emp(): {e}")

def data_prep_dept(dept_df):
    """
    Performs all necessary data preparation for department data.
    Args:
        dept_df (dataframe): Department dataframe
    Returns:
        dept_df (dataframe): Updated Department dataframe
    """
    try:
        dept_df.rename(columns={'DEPARTMENT_IDENTIFIER':'DEPARTMENT_ID'}, 
                       inplace=True)
        return dept_df
    except Exception as e:
        print(f"An error occurred: {e}")

def calculate_employees_salaries_stats(emp_df):
    """
    Calculates employee salary statistics including:
    - Average salary
    - Median salary
    - Lower and upper quartiles
    Args:
        emp_df (dataframe): Employees dataframe
    Returns:
        avg_salary         : Average Salary
        median_salary      : Median Salary
        lower_qtile_salary : Lower Quartile Salary
        upper_qtile_salary : Upper Quartile Salary
    """
    try:
        avg_salary = emp_df['SALARY'].mean()
        median_salary = emp_df['SALARY'].median()
        lower_qtile_salary = emp_df['SALARY'].quantile(0.25)
        upper_qtile_salary = emp_df['SALARY'].quantile(0.75)
        return avg_salary, median_salary, lower_qtile_salary, upper_qtile_salary
    except Exception as e:
        print(f"An error occurred: {e}")

def calculate_avg_salary_per_dept(emp_df, dept_df):
    """
    Left joins the department df (`dept_df`) with the employee df (`emp_df`).
    Calculates the average salary per department and 
    Formats the currency values to two decimal places.
    Args:
        emp_df (dataframe): Employees dataframe
        dept_df (dataframe): Department dataframe
    Returns:
        avg_salary_per_dept (dataframe): returns average salary per dept 
        and dept name
    """
    try:
        merged_df = pd.merge(emp_df, dept_df, on='DEPARTMENT_ID', how='left')
        avg_salary_per_dept = merged_df.groupby('DEPARTMENT_NAME')['SALARY'] \
            .mean().reset_index()  
        avg_salary_per_dept['SALARY'] = avg_salary_per_dept['SALARY'].apply(
            lambda x: float("{:.2f}".format(x)))
        return avg_salary_per_dept
    except Exception as e:
        print(f"An error occurred: {e}")
    
def categorize_column_by_avg(df, col_name, col_avg):
    """
    Categorizes a column's values into 'low' and 'high' based on the average
    value of that column.
    Args:
        df (dataframe)   : Dataframe with data
        col_name (string): Column Name that the function will categorize
        col_avg (float)  : Column Average value
    Returns:
        df(dataframe): The result column with additional category column
    """
    try:
        cat_col_name = f'{col_name}_CATEGORY'
        df[cat_col_name] = df[col_name].apply(
            lambda x: 'low' if x < col_avg else 'high')
        return df
    except Exception as e:
        print(f"An error occurred: {e}")

def determine_salary_category_per_dept(emp_df):
    """
    Categorizes salaries into 'low' and 'high' based on the average salary
    within the department.
    Args:
        emp_df (dataframe)   : Dataframe with employees data
    Returns:
        emp_df(dataframe): The modified employees dataframe with new category
        column
    """
    try :
        avg_salary_by_dept = emp_df.groupby('DEPARTMENT_ID')['SALARY'] \
            .transform('mean')
        emp_df['SALARY_CATEGORY_AMONG_DEPARTMENT'] = emp_df.apply(
            lambda row: 'low' if row['SALARY'] < avg_salary_by_dept[row.name]
                else 'high',axis=1 )
        return emp_df
    except Exception as e:
        print(f"An error occurred: {e}")

def find_dept_employees(emp_df, dept_id):
    """
    Retrieves employees belonging to a specified department.
    Args:
        emp_df (dataframe) : Dataframe with employees data
        dept_id (int)      : Department ID
    Returns:
        dept_employees(dataframe): The result of dept filter on employees data
    """
    try:
        dept_filter = emp_df['DEPARTMENT_ID']==dept_id
        dept_employees = emp_df[dept_filter]
        return dept_employees
    except Exception as e:
        print(f"An error occurred: {e}")

def increase_dept_salary_by_pcnt(emp_df, dept_id, pcnt):
    """
    Increases the salaries of all employees in a specified department 
    by a given percentage.
    Args:
        emp_df (dataframe) : Dataframe with employees data
        dept_id (int)      : Department ID
        pcnt (float)       : The percentage increase
    Returns:
        dept_employees(dataframe): emp_df dataframe with updated salaries
    """
    try:
        dept_filter = emp_df['DEPARTMENT_ID']==dept_id
        sal_increase_pcnt = 1+pcnt/100
        emp_df.loc[dept_filter, 'SALARY'] *= sal_increase_pcnt
        return emp_df
    except Exception as e:
        print(f"An error occurred: {e}")

def calculate_empty_values_of_column(df, column_name): 
    """
    Determine the count of records with empty values in a particular
    column.
    Args:
        df (dataframe)       : Dataframe with employees data
        column_name (string) : Department ID
    Returns:
        count(int): Count of records with empty values in column_name
    """
    try:
        empty_col_values_filter = df[column_name].isnull() | \
            df[column_name].str.strip().eq('')
        return empty_col_values_filter[empty_col_values_filter==True].count()
    except Exception as e:
        print(f"An error occurred: {e}")
