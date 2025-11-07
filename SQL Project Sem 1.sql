CREATE DATABASE BankDB;
USE BankDB;

CREATE TABLE Customers (
  CustomerID INT PRIMARY KEY,
  Name VARCHAR(50),
  Gender CHAR(1),
  Age INT,
  City VARCHAR(30),
  Phone VARCHAR(15)
);

CREATE TABLE Branches (
  BranchID INT PRIMARY KEY,
  BranchName VARCHAR(50),
  City VARCHAR(30)
);

CREATE TABLE Accounts (
  AccountID INT PRIMARY KEY,
  CustomerID INT,
  BranchID INT,
  AccountType VARCHAR(20),
  Balance DECIMAL(12,2),
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
  FOREIGN KEY (BranchID) REFERENCES Branches(BranchID)
);

CREATE TABLE Transactions (
  TransactionID INT PRIMARY KEY,
  AccountID INT,
  Date DATE,
  Type VARCHAR(10),
  Amount DECIMAL(10,2),
  FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);
INSERT INTO Customers VALUES
(1, 'Amit Sharma', 'M', 32, 'Delhi', '9990011122'),
(2, 'Priya Singh', 'F', 28, 'Mumbai', '8880033344'),
(3, 'Rahul Verma', 'M', 45, 'Chandigarh', '7770022211');

INSERT INTO Branches VALUES
(101, 'Connaught Branch', 'Delhi'),
(102, 'Andheri Branch', 'Mumbai'),
(103, 'Sector 17 Branch', 'Chandigarh');

INSERT INTO Accounts VALUES
(201, 1, 101, 'Savings', 55000.00),
(202, 2, 102, 'Current', 125000.00),
(203, 3, 103, 'Savings', 87000.00);

INSERT INTO Transactions VALUES
(1001, 201, '2025-10-01', 'Deposit', 10000.00),
(1002, 201, '2025-10-15', 'Withdraw', 2000.00),
(1003, 202, '2025-10-10', 'Deposit', 15000.00),
(1004, 203, '2025-10-20', 'Deposit', 25000.00),
(1005, 203, '2025-10-22', 'Withdraw', 5000.00);


-- a) Total Transactions per Customer
SELECT c.Name, COUNT(t.TransactionID) AS TotalTransactions
FROM Customers c
JOIN Accounts a ON c.CustomerID = a.CustomerID
JOIN Transactions t ON a.AccountID = t.AccountID
GROUP BY c.Name;

-- b) Total Deposit and Withdrawal Amounts by Branch
SELECT b.BranchName,
       SUM(CASE WHEN t.Type='Deposit' THEN t.Amount ELSE 0 END) AS TotalDeposits,
       SUM(CASE WHEN t.Type='Withdraw' THEN t.Amount ELSE 0 END) AS TotalWithdrawals
FROM Branches b
JOIN Accounts a ON b.BranchID = a.BranchID
JOIN Transactions t ON a.AccountID = t.AccountID
GROUP BY b.BranchName;

-- c) Top Customer by Transaction Volume
SELECT TOP 1 c.Name, SUM(t.Amount) AS TotalAmount
FROM Customers c
JOIN Accounts a ON c.CustomerID = a.CustomerID
JOIN Transactions t ON a.AccountID = t.AccountID
GROUP BY c.Name
ORDER BY TotalAmount DESC;


-- d) Average Account Balance per Branch
SELECT b.BranchName, AVG(a.Balance) AS AvgBalance
FROM Branches b
JOIN Accounts a ON b.BranchID = a.BranchID
GROUP BY b.BranchName;

-- e) Identify Suspicious Transactions (Amount > ₹20,000)
SELECT t.TransactionID, c.Name, t.Type, t.Amount, t.Date
FROM Transactions t
JOIN Accounts a ON t.AccountID = a.AccountID
JOIN Customers c ON a.CustomerID = c.CustomerID
WHERE t.Amount > 20000;