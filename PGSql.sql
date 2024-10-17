CREATE TABLE Accounts (
    AccountName        varchar(40),
    AccountNumber      char(8) primary key,
    AccountValue       DECIMAL(10, 2),
    LastRebalanceDate   date,
    DaysSinceLastRebalance        integer,
    TotalSecurityDriftValue         DECIMAL(10, 2),
	AccountClass		varchar(20),
	RepID				char(4)
)

insert into Accounts values('Test Account','12345678',  1500.00, '09/27/2024', 9, 100.00, 'Advisory retirement', 'ABCD');
insert into Accounts values('Dummy Account','85545566',  2500.00, '09/27/2024', 5, 200.00, 'Brokerage retirement', 'ABCD');
insert into Accounts values('some name','44445588',  150.00, '09/27/2024', 2, 300.00, 'Advisory retirement', 'PQRS');
insert into Accounts values('Saty account','11225566',  500.00, '09/27/2024', 9, 400.00, 'Bokerage non-retirement', 'MNOP');
insert into Accounts values('Another Account','98987878',  1900.00, '09/27/2024', 78, 500.00, 'Advisory retirement', 'MMAA');
