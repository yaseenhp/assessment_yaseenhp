from assessment_functions import (
    get_employees_df,
    get_departments_df,
    check_emp_df_columns,
    check_dept_df_columns,
    data_prep_emp,
    data_prep_dept,
    calculate_employees_salaries_stats,
    calculate_avg_salary_per_dept,
    categorize_column_by_avg,
    determine_salary_category_per_dept,
    find_dept_employees,
    increase_dept_salary_by_pcnt,
    calculate_empty_values_of_column
    )

if __name__ == '__main__':
    
    # Load the data
    employees = get_employees_df()
    departments = get_departments_df()
    
    # Check the data
    check_emp_df_columns(employees)
    check_dept_df_columns(departments)

    # Prepare the data
    employees = data_prep_emp(employees)
    departments = data_prep_dept(departments)
    
    print('Data loaded and prepared.')
    
    # Question 1
    input('\nPress a key to continue to the first answer...\n')  
    print('\n 1 - The avg, median, lower and upper qtiles of emp salaries:')
    (avg_salary, median_salary, lower_qtile_salary, upper_qtile_salary) = \
        calculate_employees_salaries_stats(employees)
    print('Average Salary     :', avg_salary)
    print('Median Salary      :', median_salary)
    print('Lower Qtile Salary :', lower_qtile_salary)
    print('Upper Qtile Salary :', upper_qtile_salary)

    # Question 2
    input('\nPress Enter to continue to the next answer ...\n')
    print('\n 2 - The average salary per department.')
    avg_salary_per_dept = calculate_avg_salary_per_dept(employees, departments)
    print(avg_salary_per_dept)

    # Question 3
    input('\nPress a key to continue to the next answer...\n')
    print('\n 3 - Calculate average category. ')
    salary_category = categorize_column_by_avg(employees, 'SALARY', avg_salary)
    print(salary_category[['EMPLOYEE_ID', 'SALARY', 'SALARY_CATEGORY']])

    # Question 4
    input('\nPress a key to continue to the next answer...\n')
    print('\n 4 - Calculate average `SALARY_CATEGORY_AMONG_DEPARTMENT`. ')
    salary_category_per_dept  = determine_salary_category_per_dept(employees)
    print(salary_category_per_dept[['EMPLOYEE_ID', 'DEPARTMENT_ID', 'SALARY', 
                    'SALARY_CATEGORY_AMONG_DEPARTMENT']])
    
    # Question 5    
    input('\nPress a key to continue to the next answer...\n')
    print('\n 5 - Employees belongs to DEPARTMENT_ID 20 ')
    dept_20_employees = find_dept_employees(employees,20)
    print(dept_20_employees[['EMPLOYEE_ID', 'DEPARTMENT_ID', 'SALARY', 
                    'SALARY_CATEGORY_AMONG_DEPARTMENT']])
    
    # Question 6
    input('\nPress a key to continue to the next answer...\n')
    print('\n 6 - Increase salary by 10% for Dept # 20 employees')
    emp_updated_salaries = \
        increase_dept_salary_by_pcnt(employees, 20, 10)    
    print(emp_updated_salaries[['EMPLOYEE_ID', 'DEPARTMENT_ID', 'SALARY']] \
        [emp_updated_salaries['DEPARTMENT_ID']==20])
        
    # Question 7
    input('\nPress a key to continue to the next answer...\n')
    print('\n 7 -  Check if any of the PHONE_NUMBER column values are empty.')
    employees_count_with_empty_phone = \
        calculate_empty_values_of_column(employees,'PHONE_NUMBER')
    print('No. of employees with empty phone no:', 
            employees_count_with_empty_phone)
