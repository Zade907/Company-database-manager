CREATE DATABASE company_db;
USE company_db;

CREATE TABLE employee_data (
	emp_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_name VARCHAR(20) ,
    emp_designation VARCHAR(255) ,
    emp_salary DECIMAL(10,2) ,
    emp_department VARCHAR(255) 
);

CREATE TABLE customer_data (
	customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(255), 
    customer_contact VARCHAR(15), 
    customer_address VARCHAR(255),
    CHECK (CHAR_LENGTH(customer_contact) = 10)
    );
    
CREATE TABLE financial_data(
	transaction_id INT PRIMARY KEY AUTO_INCREMENT,
	customer_id INT,
	emp_id INT,
	amount DECIMAL(10,2),
	transaction_type VARCHAR(20),
	date DATE,
	FOREIGN KEY (customer_id) REFERENCES customer_data(customer_id),
	FOREIGN KEY (emp_id) REFERENCES employee_data(emp_id)
    );
